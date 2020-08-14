import random
import string

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.views.generic.edit import FormView

from django.contrib.auth import login
from django.contrib.auth.models import User

from groups.models import Group

from .forms import LtiUsernameForm


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class LtiInitializerException(Exception):
    pass


class LtiInitializerView(RedirectView):

    pattern_name = "home"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):

        course_id = request.POST.get("custom_canvas_course_id", None)
        roles = request.POST.get("ext_roles", None)
        title = request.POST.get("context_title", None)

        if course_id is None:
            try:
                course_id = self.request.session["course_id"]
                roles = self.request.session["roles"]
                title = self.request.session["title"]
            except KeyError:
                # This should already be caught in middleware.py
                raise LtiInitializerException("The required lti initialization parameters have not been provided.")

        # Get an existing group, or create a new one
        if course_id is not None:
            group = self.get_or_create_group(course_id=int(course_id), title=title)
        else:
            raise LtiInitializerException("The required lti initialization parameters have not been provided.")

        # Determine if the user is a Teacher or Student
        role = self.determine_role(roles)
        # Update the roles at each launch
        self.update_roles(user=request.user, group=group, role=role)

        return super(LtiInitializerView, self).dispatch(request, *args, **kwargs)

    def update_roles(self, user, group, role):
        """
        Takes a user, group, and roles list.
        Will update group's teachers or students sets
        Returns None
        """
        if role == "Teacher":
            group.teachers.add(user)
            if user in group.students.all():
                group.students.remove(user)
        else:
            group.students.add(user)
            if user in group.teachers.all():
                group.teachers.remove(user)
        return None

    def determine_role(self, roles):
        """ Takes (list) roles or None, returns (str) role  """
        if roles:
            roles = [role.rsplit("/")[-1] for role in roles.split(",")]
            if "Instructor" in roles:
                return "Teacher"
        # If roles is None, then I am returning "Student", although it is actually
        # indicative on an LTI failure.
        return "Student"

    def get_or_create_group(self, course_id=None, title="Empty"):
        """ takes (int) course_id, and (str) title and returns a Group"""
        try:
            group = Group.objects.get(class_key=course_id)
        except Group.DoesNotExist:
            group = Group.objects.create(class_key=course_id, title=title)
        return group


class LtiRegistrationView(FormView):

    template_name = "lti_registration.html"
    form_class = LtiUsernameForm
    success_url = "/lti/lti_initializer/"

    def dispatch(self, request, *args, **kwargs):
        try:
            request.session["lti_email"]
        except KeyError:
            return render(request, "lti_failure.html")
        return super(LtiRegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        username = form.cleaned_data["username"]
        unique_username = form.unique_username(username)
        if unique_username is False:
            msg = "Sorry, that username is taken."
            form.add_error("username", msg)
            return super().form_invalid(form)
        email = self.request.session["lti_email"]
        password = get_random_alphanumeric_string(10)

        new_user = User.objects.create_user(username, email=email, password=password)
        login(self.request, new_user, backend="hedera.backends.UsernameAuthenticationBackend")

        return super().form_valid(form)
