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

from .utils import login_existing_user



LTI_PROPERTY_COURSE_ID = "custom_canvas_course_id"
LTI_PROPERTY_COURSE_TITLE = "context_title"
LTI_PROPERTY_USER_EMAIL = "lis_person_contact_email_primary"
LTI_PROPERTY_USER_ROLES = "ext_roles"



def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class LtiInitializerView(RedirectView):

    url = "/"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """ Handle LTI verification and user authentication """
        lti = LTI(request_type="any", role_type="any")
        try:
            lti.verify(request)
        except LTIException:
            return render(request, "lti_failure.html")

        if not request.user.is_authenticated:
            try:
                lti_user = login_existing_user(request)
            except EmailAddress.DoesNotExist:
                lti_email = request.POST.get(LTI_PROPERTY_USER_EMAIL, None)
                if not lti_email:
                    return render(request, "lti_failure.html")
                self.create_lti_user(lti_email)
                try:
                    lti_user = login_existing_user(request)
                except EmailAddress.DoesNotExist:
                    return render(request, "lti_failure.html")
            if lti_user is False:
                return render(request, "lti_failure.html")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle the POST coming directly from Canvas """

        lti_params = {
            "course_id": request.POST.get(LTI_PROPERTY_COURSE_ID, None),
            "roles": request.POST.get(LTI_PROPERTY_USER_ROLES, None),
            "title": request.POST.get(LTI_PROPERTY_COURSE_TITLE, None)
        }
        
        if None in lti_params.values():
            return render(request, "lti_failure.html")

        self.initialize_group(
            lti_params["course_id"],
            lti_params["title"],
            lti_params["roles"],
            request.user
        )

        return super().post(request, *args, **kwargs)
        
    def create_lti_user(self, email):
        """
        takes (str)email and creates a User, returns None.
        Sets the user's profile display_name to the username portion of the lti email
        """
        display_name = email.split("@")[0]
        password = get_random_alphanumeric_string(10)
        new_user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password=password
        )
        profile = new_user.profile
        profile.display_name = display_name
        profile.save()
        return None

    def initialize_group(self, course_id, title, roles, user):
        """
        Takes in (str)course_id (str)title (str)roles, and (obj)user.
        Gets or creates group, and updates the user's role in that group.
        The parameters cannot be None
        Returns None
        """
        group, created = Group.objects.get_or_create(
            class_key=int(course_id),
            defaults=dict(
                title=title,
                created_by=user
            )
        )
        # Determine if the user is a Teacher or Student
        role = self.determine_role(roles)
        # Update the roles at each launch
        self.update_roles(user=user, group=group, role=role)
        return None

    def determine_role(self, roles):
        """ Takes (list) roles or None, returns (str) role  """
        if roles:
            roles = [role.rsplit("/")[-1] for role in roles.split(",")]
            if "Instructor" in roles or "TeachingAssistant" in roles:
                return "Teacher"
        # If roles is None, then I am returning "Student", although it is actually
        # indicative on an LTI failure.
        return "Student"

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
