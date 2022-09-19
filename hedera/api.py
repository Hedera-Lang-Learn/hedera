import json
import re

from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from lattices.models import LatticeNode, LemmaNode
from lemmatization.models import FormToLemma, Lemma
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
from .supported_languages import SUPPORTED_LANGUAGES


LANGUAGES = [[lang.code, lang.verbose_name] for lang in SUPPORTED_LANGUAGES.values()]


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
        if(data["lang"] in (x[0] for x in LANGUAGES)):
            profile.lang = data["lang"]
            profile.save()
            return JsonResponse({"data": profile.data()})
        return JsonResponseBadRequest({"error": "language not supported"})


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
        cloned = None
        if self.kwargs.get("action") == "retry" and self.text.can_retry():
            self.text.retry_lemmatization()
        elif self.kwargs.get("action") == "cancel" and self.text.can_cancel():
            self.text.cancel_lemmatization()
        elif self.kwargs.get("action") == "clone":
            # @@@ self.text can only be fetched if public or you own it, probably need to expand for teachers
            cloned = self.text.clone(cloned_by=request.user)
        return JsonResponse(data=dict(data=self.get_data(new_text=cloned)))


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


class LemmatizationLemmaAPI(APIView):
    def get_data(self):
        lemma_id = self.kwargs.get("lemma_id")
        lemma = get_object_or_404(Lemma, pk=lemma_id)
        return lemma.to_dict()


class LemmatizationFormLookupAPI(APIView):
    def get_data(self):
        form = self.kwargs.get("form")
        lang = self.kwargs.get("lang")
        # gets list of forms
        forms = FormToLemma.objects.filter(lang=lang, form=form)
        if not forms:
            forms = FormToLemma.objects.filter(lang=lang, form=form.lower())
        lemma_list = [form.get_lemma() for form in forms]
        sorted_lemma_list = (sorted(lemma_list, key=lambda i: i["rank"]))
        data = {
            "lang": lang,
            "form": form,
            "lemmas": sorted_lemma_list
        }
        return data


class LemmatizationAPI(APIView):

    def decorate_token_data(self, text):
        data = text.data

        lemmas = Lemma.objects.filter(pk__in=[token["lemma_id"] for token in data])
        lemmas_cache = {
            lemma.pk: lemma
            for lemma in lemmas
        }

        # this is checking to see if the token is in the user's personal vocab list
        # it annotates the token with inVocabList=True|False
        vocablist_id = self.request.GET.get("vocablist_id", None)
        vocablist = None
        if vocablist_id is not None:
            vocablist = get_any_vocablist_by_id(self.request.user.id, text.lang, vocablist_id)
        for index, token in enumerate(data):
            token["tokenIndex"] = index
            lemma = lemmas_cache.get(token["lemma_id"])
            if lemma is not None:
                token.update(lemma.gloss_data())
            if vocablist_id is not None:
                vocab_entry = vocablist.entries.filter(lemma_id=token["lemma_id"])
                if vocablist_id == "personal":
                    # Note: assumes that the vocab can successfully link to a lemma - not accounting for NULL Values
                    familarity = list(vocab_entry.values_list("familiarity", flat=True))
                    token["familiarity"] = token["resolved"] and familarity[0]
                token["inVocabList"] = token["resolved"] and vocab_entry.exists()
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
        lemma_id = data["lemmaId"]
        resolved = data["resolved"]
        # list of gloss ids
        gloss_ids = data["glossIds"]

        text.update_token(self.request.user, token_index, lemma_id, gloss_ids, resolved)

        text.refresh_from_db()
        data = self.decorate_token_data(text)
        history = [h.data() for h in text.logs.filter(token_index=token_index).order_by("created_at")]
        return JsonResponse({"data": dict(tokens=data, tokenHistory=history)})


class TokenHistoryAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.all()
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        is_valid_user = text.is_valid_user(self.request.user)
        if is_valid_user:
            token_index = self.kwargs.get("token_index")
            history = [h.data() for h in text.logs.filter(token_index=token_index).order_by("created_at")]
            return dict(tokenHistory=history)
        raise Http404()


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
            lemma = get_object_or_404(Lemma, pk=data["lemma"])
            entry.lemma = lemma
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
        vl = self.get_object()
        return dict(
            personalVocabList=vl.data(),
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
            return JsonResponseBadRequest({"error": f"could not find vocab with id={data['id']}"}, status=404)
        return JsonResponseBadRequest({"error": f"missing 'id'"})


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
        keys = ["familiarity", "headword", "definition", "vocabulary_list_id"]
        for key in keys:
            if key not in data:
                return False
        return True

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        checked_data = self.check_data(data)
        if checked_data is not True:
            return JsonResponseBadRequest({"error": "Missing required fields"})
        if "lemma" in data and data["lemma"] is not None:
            data["lemma"] = get_object_or_404(Lemma, pk=data["lemma"])
        try:
            # to handle new quick add when list doesnt exist create using lang if
            if data["vocabulary_list_id"] is None:
                if "lang" not in data:
                    raise KeyError("lang field not provided")
                new_vocab_list, _ = PersonalVocabularyList.objects.get_or_create(user=self.request.user, lang=data["lang"])
                data["vocabulary_list_id"] = new_vocab_list.data()["id"]
            # removes lang key before creating the entry
            if "lang" in data:
                del data["lang"]
            new_entry = PersonalVocabularyListEntry.objects.create(**data)
            return JsonResponse({"data": {"created": True, "data": new_entry.data()}})

        except Exception as e:
            return JsonResponseBadRequest(data={"error": f"{e}"})


class LatticeNodesAPI(APIView):

    def get(self, request):
        try:
            headword = self.request.GET.get("headword")
            if len(headword) == 0:
                return JsonResponse({"data": []})
            filtered_headword_iterable = filter(str.isalnum, headword)
            filtered_headword_string = "".join(filtered_headword_iterable)
            # [0-9]* includes headword matches with trailing numbers 0 - 9 eg 20 or 2
            lemmas = LemmaNode.objects.filter(lemma__iregex=rf"\y{re.escape(filtered_headword_string)}[0-9]*\y")
            lattice_nodes = [lemma.to_dict()["node"] for lemma in lemmas]
            return JsonResponse({"data": self.filter_lattice_nodes(lattice_nodes)})
        except TypeError:
            return JsonResponseBadRequest({"error": "Missing headword"})

    def filter_lattice_nodes(self, lattice_nodes):
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


class SupportedLanguagesAPI(APIView):

    def get_data(self):
        return LANGUAGES


def get_any_vocablist_by_id(user_id, lang, vocablist_id):
    if vocablist_id == "personal":
        return get_object_or_404(PersonalVocabularyList, user=user_id, lang=lang)
    return get_object_or_404(VocabularyList, pk=vocablist_id)
