from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from account.mixins import LoginRequiredMixin

from lemmatized_text.models import LemmatizedText

from .models import Group


class GroupListView(LoginRequiredMixin, ListView):

    model = Group
    template_name = "groups/groups.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(teachers=self.request.user) | Q(students=self.request.user)
        )
        for group in queryset:
            group.is_teacher = group.teachers.filter(pk=self.request.user.pk).exists()
            group.is_student = group.students.filter(pk=self.request.user.pk).exists()
        return queryset


class GroupDetailView(LoginRequiredMixin, DetailView):

    model = Group
    slug_field = "class_key"
    template_name = "groups/group.html"

    def get_object(self, queryset=None):
        group = super().get_object(queryset)
        group.is_teacher = group.teachers.filter(pk=self.request.user.pk).exists()
        group.is_student = group.students.filter(pk=self.request.user.pk).exists()
        return group


class GroupJoinView(LoginRequiredMixin, DetailView):

    model = Group
    template_name = "groups/join.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if queryset is None:
            queryset = self.get_queryset()
        group = queryset.filter(student_invite_key=slug).first()
        if group is not None:
            group.student_invite = True
            group.teacher_invite = False
        else:
            group = queryset.filter(teacher_invite_key=slug).first()
            if group is not None:
                group.student_invite = False
                group.teacher_invite = True
        if group is None:
            raise Http404
        return group

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        if group.teacher_invite:
            group.teachers.add(request.user)
        elif group.student_invite:
            group.students.add(request.user)
        return HttpResponseRedirect(reverse("groups_list"))


class GroupCreateView(LoginRequiredMixin, CreateView):

    model = Group
    fields = ["title", "description"]

    def form_valid(self, form):
        group = form.save()
        group.teachers.add(self.request.user)
        return HttpResponseRedirect(group.get_absolute_url())


class GroupUpdateBaseView(LoginRequiredMixin, UpdateView):
    model = Group
    slug_field = "class_key"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(teachers__pk=self.request.user.pk)
        return queryset


class GroupUpdateView(GroupUpdateBaseView):

    fields = ["title", "description"]


class GroupUpdateTextsView(GroupUpdateBaseView):

    template_name = "groups/texts.html"
    fields = ["texts"]
    ## Limit texts that can be added to only "yours"
    ## Allow removal of any text
    def get_context_data(self):
        data = super().get_context_data()
        all_avail_texts = LemmatizedText.objects.filter(
            Q(public=True) | Q(created_by__in=self.object.teachers.all())
        ).exclude(
            pk__in=[t.pk for t in self.object.texts.all()]
        )
        data["avail_texts"] = all_avail_texts
        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        remove_texts = LemmatizedText.objects.filter(pk__in=request.POST.getlist("text-delete"))
        add_texts = LemmatizedText.objects.filter(pk__in=request.POST.getlist("text-add"))
        self.object.texts.remove(*remove_texts)
        self.object.texts.add(*add_texts)
        return HttpResponseRedirect(self.object.get_absolute_url())


class GroupUpdateVocabView(GroupUpdateBaseView):

    fields = ["vocab_lists"]

    ## Limit lists that can be added to only "yours"
    ## Allow removal of any list
    def get_context_data(self):
        data = super().get_context_data()
        return data
