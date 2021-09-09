import json
import re

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from lattices.models import LatticeNode, LemmaNode
# from lattices.utils import get_or_create_nodes_for_form_and_lemmas
from lemmatized_text.models import LemmatizedText, LemmatizedTextBookmark
from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry,
    PersonalVocabularyStats,
    VocabularyList,
    VocabularyListEntry
)

from .models import Profile


class JsonResponseAuthError(JsonResponse):

    status_code = 401


class AuthedView(View):

    auth_required = True

    @property
    def user(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if self.auth_required and not request.user.is_authenticated:
            return JsonResponseAuthError(data={"error": "Authentication required"})
        return super().dispatch(request, *args, **kwargs)


class APIView(AuthedView):

    def get_data(self):
        return {}

    def render_to_response(self):
        return JsonResponse({"data": self.get_data()})

    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class MeAPI(APIView):

    def get_data(self):
        return self.request.user.profile.data()

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)
        if(data["lang"] in (x[0] for x in settings.SUPPORTED_LANGUAGES)):
            profile.lang = data["lang"]
            profile.save()
            return JsonResponse({"data": profile.data()})
        return HttpResponseBadRequest("language not supported")


class BookmarksListAPI(APIView):
    def get_data(self):
        qs = LemmatizedTextBookmark.objects.filter(Q(user=self.request.user)).order_by("-created_at")
        return [bookmark.api_data() for bookmark in qs]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        textId = int(data["textId"])

        # ensure user has access to the text
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=textId)

        bookmark, _ = LemmatizedTextBookmark.objects.get_or_create(
            user=self.request.user,
            text=text
        )
        return JsonResponse(dict(data=bookmark.api_data()))


class BookmarksDetailAPI(APIView):
    def get_data(self):
        qs = LemmatizedTextBookmark.objects.filter(user=self.request.user)
        bookmark = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        return bookmark.api_data()

    def delete(self, request, *args, **kwargs):
        qs = LemmatizedTextBookmark.objects.filter(user=self.request.user)
        try:
            bookmark = qs.filter(pk=self.kwargs.get("pk")).get()
            bookmark.delete()
        except LemmatizedTextBookmark.DoesNotExist:
            pass
        return JsonResponse({})


class LemmatizedTextListAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user)).order_by("created_at")
        return [
            dict(text=text.api_data(), stats=text.stats_for_user(self.request.user))
            for text in qs
        ]


class LemmatizedTextStatusAPI(APIView):

    @property
    def text(self):
        if not hasattr(self, "_text"):
            qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
            self._text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        return self._text

    def get_data(self, new_text=None):
        if new_text is None:
            new_text = self.text
        return dict(
            completed=new_text.completed,
            tokenCount=new_text.token_count() if new_text.completed == 100 else None,
            lemmatizationStatus=new_text.lemmatization_status(),
            detailUrl=reverse("lemmatized_texts_detail", args=[new_text.id]),
            textId=new_text.id
        )

    def post(self, request, *args, **kwargs):
        if self.kwargs.get("action") == "retry" and self.text.can_retry():
            self.text.retry_lemmatization()
        elif self.kwargs.get("action") == "cancel" and self.text.can_cancel():
            self.text.cancel_lemmatization()
        elif self.kwargs.get("action") == "clone":
            # @@@ self.text can only be fetched if public or you own it, probably need to expand for teachers
            cloned = self.text.clone(cloned_by=request.user)
        return JsonResponse(data=dict(data=self.get_data(cloned)))


class LemmatizedTextDetailAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.filter(
            Q(public=True) |
            Q(created_by=self.request.user) |
            Q(classes__students=self.request.user) |
            Q(classes__teachers=self.request.user)
        ).distinct()
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        return text.api_data()


class LemmatizationAPI(APIView):

    def decorate_token_data(self, text):
        data = text.data
        nodes = LatticeNode.objects.filter(pk__in=[token["node"] for token in data])
        nodes_cache = {
            node.pk: node
            for node in nodes
        }
        vocablist_id = self.request.GET.get("vocablist", None)
        if vocablist_id is not None:
            if vocablist_id == "personal":
                vl = get_object_or_404(PersonalVocabularyList, user=self.request.user, lang=text.lang)
            else:
                vl = get_object_or_404(VocabularyList, pk=vocablist_id)
            node_ids = vl.entries.values_list("node__pk", flat=True)
            related_node_cache = dict()
            for token in data:
                node = nodes_cache.get(token["node"])
                if node is not None:
                    if related_node_cache.get(node.pk) is None:
                        related_node_cache[node.pk] = [n.pk for n in node.related_nodes()]
                    related_node_ids = related_node_cache[node.pk]
                    token["inVocabList"] = token["resolved"] and any(item in related_node_ids for item in node_ids)
                else:
                    token["inVocabList"] = False

        if self.request.GET.get("personalvocablist", None) is not None:
            vl = get_object_or_404(PersonalVocabularyList, pk=self.request.GET.get("personalvocablist"))
            for token in data:
                token["inVocabList"] = token["resolved"] and vl.entries.filter(node__pk=token["node"]).exists()
                token["familiarity"] = token["resolved"] and vl.node_familiarity(token["node"])

        for index, token in enumerate(data):
            token["tokenIndex"] = index
            node = nodes_cache.get(token["node"])
            if node is not None:
                token.update(node.gloss_data())

        return data

    def get_data(self):
        qs = LemmatizedText.objects.filter(
            Q(public=True) |
            Q(created_by=self.request.user) |
            Q(classes__students=self.request.user) |
            Q(classes__teachers=self.request.user)
        ).distinct()
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        data = self.decorate_token_data(text)
        return data

    def post(self, request, *args, **kwargs):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        data = json.loads(request.body)
        token_index = data["tokenIndex"]
        node_id = data["nodeId"]
        resolved = data["resolved"]

        text.update_token(self.request.user, token_index, node_id, resolved)

        text.refresh_from_db()
        data = self.decorate_token_data(text)
        history = [h.data() for h in text.logs.filter(token_index=token_index).order_by("created_at")]
        return JsonResponse({"data": dict(tokens=data, tokenHistory=history)})


class TokenHistoryAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        token_index = self.kwargs.get("token_index")
        history = [h.data() for h in text.logs.filter(token_index=token_index).order_by("created_at")]
        return dict(tokenHistory=history)


class VocabularyListAPI(APIView):

    def get_data(self):
        return [
            v.data()
            for v in VocabularyList.objects.filter(
                lang=self.request.GET.get("lang")
            ).filter(
                Q(owner__isnull=True) | Q(owner=self.request.user)
            )
        ]


class VocabularyListEntriesAPI(APIView):

    def get_data(self):
        vocab_list = get_object_or_404(VocabularyList, pk=self.kwargs.get("pk"))
        return dict(
            canEdit=vocab_list.owner == self.request.user,
            entries=[v.data() for v in vocab_list.entries.all().order_by("headword")]
        )


class VocabularyListEntryAPI(APIView):

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(VocabularyListEntry, pk=self.kwargs.get("pk"), vocabulary_list__owner=request.user)
        action = kwargs.get("action")

        if action == "link":
            data = json.loads(request.body)
            node = get_object_or_404(LatticeNode, pk=data["node"])
            entry.node = node
            entry.save()
            return_data = entry.data()
        elif action == "delete":
            entry.delete()
            return_data = {}
        elif action == "edit":
            data = json.loads(request.body)
            entry.headword = data["headword"]
            entry.gloss = data["gloss"]
            entry.save()
            return_data = entry.data()

        return JsonResponse(return_data)


class PersonalVocabularyListAPI(APIView):

    @property
    def text(self):
        if self.request.GET.get("text") is None:
            return
        if getattr(self, "_text", None) is None:
            qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
            self._text = get_object_or_404(qs, pk=self.request.GET.get("text"))
        return self._text

    def get_object(self):
        if self.text:
            lang = self.text.lang
        else:
            lang = self.request.GET.get("lang")
        vl, _ = PersonalVocabularyList.objects.get_or_create(
            user=self.request.user,
            lang=lang,
        )
        return vl

    def get_data(self):
        page_number = self.request.GET.get("page") or 1
        vl = self.get_object()
        vl_data_copy = vl.data()
        paginator = Paginator(vl_data_copy["entries"], 100)
        page_obj = paginator.get_page(page_number)
        vl_data_copy["entries"] = page_obj.object_list
        vl_data_copy["pageNumber"] = page_number
        vl_data_copy["totalPages"] = paginator.num_pages
        return dict(
            personalVocabList=vl_data_copy,
            unknownGlosses=None
        )

    def post(self, request, *args, **kwargs):
        vl = self.get_object()

        data = json.loads(request.body)
        familiarity = int(data["familiarity"])

        pk = kwargs.get("pk", None)
        if pk is not None:
            entry = get_object_or_404(PersonalVocabularyListEntry, pk=pk)
            entry.familiarity = familiarity
            entry.save()
        else:
            node = get_object_or_404(LatticeNode, pk=data["nodeId"])
            headword = data["headword"]
            gloss = data["gloss"]
            vl.entries.create(
                headword=headword,
                gloss=gloss,
                familiarity=familiarity,
                node=node,
            )

        if self.text:
            stats, _ = PersonalVocabularyStats.objects.get_or_create(text=self.text, vocab_list=vl)
            stats.update()

        vl.refresh_from_db()

        return JsonResponse({"data": vl.data()})

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if "id" in data:
            count, _ = PersonalVocabularyListEntry.objects.filter(id=data["id"]).delete()
            if(count != 0):
                return JsonResponse({"data": True, "id": data["id"]})
            return HttpResponseNotFound(f"could not find vocab with id={data['id']}")
        return HttpResponseBadRequest(f"missing 'id'")


class PersonalVocabularyQuickAddAPI(APIView):

    def get_data(self):
        qs = PersonalVocabularyList.objects.filter(user=self.request.user)
        lang_list = []
        for lang_data in qs:
            lang_list.append({
                "lang": lang_data.lang,
                "id": lang_data.id
            })
        return lang_list

    def check_data(self, data):
        keys = ["familiarity", "headword", "gloss", "vocabulary_list_id"]
        for key in keys:
            if key not in data:
                return False
        return True

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        checked_data = self.check_data(data)
        if checked_data is not True:
            return JsonResponseBadRequest(data={"error": "Missing required fields"})
        if "node" in data and data["node"] is not None:
            data["node"] = get_object_or_404(LatticeNode, pk=data["node"])
        new_entry = PersonalVocabularyListEntry.objects.create(**data)
        return JsonResponse({"data": {"created": True, "data": new_entry.data()}})


class LatticeNodesAPI(APIView):

    def get_data(self):
        headword = self.request.GET.get("headword")
        filtered_headword_iterable = filter(str.isalnum, headword)
        filtered_headword_string = "".join(filtered_headword_iterable)
        # [0-9]* includes headword matches with trailing numbers 0 - 9 eg 20 or 2
        lemmas = LemmaNode.objects.filter(lemma__iregex=rf"\y{re.escape(filtered_headword_string)}[0-9]*\y")
        lattice_nodes = [lemma.to_dict()["node"] for lemma in lemmas]
        return self.filter_lattice_nodes(lattice_nodes, filtered_headword_string)

    def filter_lattice_nodes(self, lattice_nodes, headword):
        lattice_node_list = []
        for node in lattice_nodes:
            gloss = node["gloss"]
            if gloss != "from morpheus" and gloss != "morpheus ambiguity":
                lattice_node_list.append(node)
            elif len(node["children"]):
                # checks child nodes appends them to the result
                for child_node in node["children"]:
                    if child_node["gloss"] != "from morpheus" and child_node["gloss"] != "morpheus ambiguity":
                        lattice_node_list.append(child_node)
        # checks for duplicates lattice nodes
        seen = set()
        filtered_results = []
        for dic in lattice_node_list:
            key = (dic["pk"])
            if key in seen:
                continue
            filtered_results.append(dic)
            seen.add(key)

        return filtered_results


class JsonResponseBadRequest(JsonResponse):
    status_code = 400
