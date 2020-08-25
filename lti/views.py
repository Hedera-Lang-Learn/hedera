import random
import string

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.views.generic.edit import FormView

from django.contrib.auth import get_user_model, login

from account.models import EmailAddress
from lti_provider.lti import LTI
from pylti.common import LTIException

from groups.models import Group

from .forms import LtiUsernameForm
from .utils import login_existing_user


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class LtiInitializerView(RedirectView):

    url = "/"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """ Handle LTI verification and user authentication """
        lti = LTI(request_type='any', role_type='any')
        try:
            lti.verify(request)
        except LTIException:
            return render(request, "lti_failure.html")
            
        if not request.user.is_authenticated:
            try:
                lti_user = login_existing_user(request)
            except EmailAddress.DoesNotExist:
                request.session['lti_email'] = request.POST.get("lis_person_contact_email_primary", None)
                if request.session['lti_email'] is None:
                    return render(request, "lti_failure.html")
                return HttpResponseRedirect(reverse('lti_registration'))
            if lti_user is False:
                return render(request, "lti_failure.html")
    
        return super(LtiInitializerView, self).dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        """ Handle the redirection coming from username registration """
        
        lti_params = {
            'course_id': request.session.get("custom_canvas_course_id", None),
            'roles': request.session.get("ext_roles", None),
            'title': request.session.get("context_title", None)
        }
        
        if None in lti_params.values():
            return render(request, "lti_failure.html")

        self.initialize_group(
            lti_params['course_id'],
            lti_params['title'],
            lti_params['roles'],
            request.user
        )
        
        return super(LtiInitializerView, self).get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        """ Handle the POST coming directly from Canvas """
        
        lti_params = {
            'course_id': request.POST.get("custom_canvas_course_id", None),
            'roles': request.POST.get("ext_roles", None),
            'title': request.POST.get("context_title", None)
        }
        
        if None in lti_params.values():
            return render(request, "lti_failure.html")
        
        self.initialize_group(
            lti_params['course_id'],
            lti_params['title'],
            lti_params['roles'],
            request.user
        )
        
        return super(LtiInitializerView, self).post(request, *args, **kwargs)
        
    def initialize_group(self, course_id, title, roles, user):
        """ Make some sort of comment """
        if course_id is not None:
            group = self.get_or_create_group(course_id=int(course_id), title=title, user=user)
        else:
            return render(request, "lti_failure.html")
        
        # Determine if the user is a Teacher or Student
        role = self.determine_role(roles)
        # Update the roles at each launch
        self.update_roles(user=user, group=group, role=role)
        return None

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

    def get_or_create_group(self, course_id=None, title="Empty", user=None):
        """ takes (int) course_id, and (str) title and returns a Group"""
        try:
            group = Group.objects.get(class_key=course_id)
        except Group.DoesNotExist:
            group = Group.objects.create(
                class_key=course_id,
                title=title,
                created_by=user
            )
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

        new_user = get_user_model().objects.create_user(username, email=email, password=password)
        login(self.request, new_user, backend="hedera.backends.UsernameAuthenticationBackend")

        return super().form_valid(form)
