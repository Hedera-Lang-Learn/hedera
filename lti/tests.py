from django.test import RequestFactory, TestCase, override_settings

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from account.models import Account

from groups.models import Group

from .views import (
    LtiInitializerException,
    LtiInitializerView,
    LtiRegistrationView
)


@override_settings(
    AUTHENTICATION_BACKENDS=[
        "account.auth_backends.UsernameAuthenticationBackend"
    ]
)
class LtiInitializerViewTests(TestCase):

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email=email, password=password)
        return user

    def setUp(self):
        self.created_user = self.create_user("user1", "user1@example.com", "password")

    def test_account_created(self):
        found_user = Account.objects.get(user=self.created_user)
        self.assertEqual(self.created_user.pk, found_user.user.pk)

    def test_login_existing_user_success(self):
        """Using the user1 which has already been created"""
        self.client.post(
            "/lti/lti_initializer/",
            {
                "lis_person_contact_email_primary": "user1@example.com",
                "custom_canvas_course_id": "327",
                "context_title": "test title"
            }
        )
        user = User.objects.get(username="user1")
        self.assertTrue(user.is_authenticated)

    def test_login_existing_user_failure(self):
        """If it fails to find an existing user, it should redirect to LTI signup"""
        response = self.client.post("/lti/lti_initializer/", {"lis_person_contact_email_primary": "user2@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/lti/lti_registration")

    def test_get_or_create_group_doesnt_override_existing(self):
        Group.objects.create(class_key=1, title="Test title")
        existing_group = Group.objects.get(class_key=1)
        lti_initializer = LtiInitializerView()
        initializer_group = lti_initializer.get_or_create_group(course_id=1, title="Don't update")
        self.assertEqual(initializer_group, existing_group)

    def test_get_or_create_group_creates_new(self):
        lti_initializer = LtiInitializerView()
        lti_initializer.get_or_create_group(course_id=2, title="Newly created")
        created_group = Group.objects.get(class_key=2)
        self.assertEqual(created_group.title, "Newly created")

    def test_role_is_added(self):
        lti_initializer = LtiInitializerView()
        Group.objects.create(class_key=1, title="Test title")
        group = Group.objects.get(class_key=1)
        user = User.objects.get(username="user1")
        lti_initializer.update_roles(user=user, group=group, role="Student")
        self.assertTrue(user in group.students.all())

    def test_role_is_updated(self):
        lti_initializer = LtiInitializerView()
        Group.objects.create(class_key=1, title="Test title")
        group = Group.objects.get(class_key=1)
        user = User.objects.get(username="user1")
        lti_initializer.update_roles(user=user, group=group, role="Student")
        self.assertTrue(user in group.students.all())
        lti_initializer.update_roles(user=user, group=group, role="Teacher")
        self.assertFalse(user in group.students.all())
        self.assertTrue(user in group.teachers.all())

    def test_determine_role(self):
        lti_initializer = LtiInitializerView()
        teacher_role = "urn:something/something-else/Instructor,urn:something/something-else/Student"
        self.assertEqual(lti_initializer.determine_role(teacher_role), "Teacher")
        student_role = "urn:something/something-else/not-Instructor,urn:something/something-else/Student"
        self.assertEqual(lti_initializer.determine_role(student_role), "Student")
        # roles of None will also return "Student"
        self.assertEqual(lti_initializer.determine_role(None), "Student")

    def test_dispatch_throws_error(self):
        """ Test missing POST parameters will cause dispatch to throw custom error """
        with self.assertRaises(LtiInitializerException):
            self.client.post(
                "/lti/lti_initializer/",
                {
                    "lis_person_contact_email_primary": "user1@example.com"
                }
            )

    def test_dispatch(self):
        """ Test successful dispatch redirects to home """
        response = self.client.post(
            "/lti/lti_initializer/",
            {
                "lis_person_contact_email_primary": "user1@example.com",
                "custom_canvas_course_id": "327",
                "context_title": "test title",
                "ext_roles": "urn:something/something-else/Instructor,urn:something/something-else/Student"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class LtiRegistrationViewTests(TestCase):

    def test_get(self):
        rf = RequestFactory()
        request = rf.get("/lti/lti_registration")
        request.user = None
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["lti_email"] = "user2@example.com"
        request.session.save()
        response = LtiRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose a username")

    def test_get_lti_failure(self):
        """ If a user attempts to access registration without the session variables set """
        response = self.client.get("/lti/lti_registration")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your session has expired. Please, relaunch the tool via your canvas course."
        )

    def test_post_success(self):
        """ Test that successful form post redirects to LtiInitializerView """

        # RequestFactory is required, because I am messing with the session
        rf = RequestFactory()
        request = rf.post("/lti/lti_registration", data={"username": "new_username"})
        request.user = None
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["lti_email"] = "testEmail@test.org"
        request.session.save()
        response = LtiRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/lti/lti_initializer/")

    def test_post_form_error(self):
        """ Test that non-unique username does not redirect """
        User.objects.create_user("taken_username", email="test@test.com", password="1f2dDfv!")
        rf = RequestFactory()
        request = rf.post("/lti/lti_registration", data={"username": "taken_username"})
        request.user = None
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["lti_email"] = "user2@example.com"
        request.session.save()
        response = LtiRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, that username is taken.")
