from django.test import TestCase, override_settings

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware

from account.models import Account, EmailAddress

from groups.models import Group

from .views import LtiInitializerView


@override_settings(
    AUTHENTICATION_BACKENDS=[
        "account.auth_backends.EmailAuthenticationBackend"
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
        found_email = EmailAddress.objects.get(user=self.created_user)
        self.assertEqual(self.created_user.pk, found_user.user.pk)
        self.assertEqual(self.created_user.pk, found_email.user.pk)

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

    # until I can figure out how to mock a verified lti launch
    # def test_login_existing_user_failure(self):
    #     """If it fails to find an existing user, it should redirect to LTI signup"""
    #     response = self.client.post("/lti/lti_initializer/", {"lis_person_contact_email_primary": "user2@example.com"})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, "/lti/lti_registration")

    # def test_get_or_create_group_doesnt_override_existing(self):
    #     Group.objects.create(class_key=1, title="Test title", created_by=self.created_user)
    #     existing_group = Group.objects.get(class_key=1)
    #     lti_initializer = LtiInitializerView()
    #     initializer_group = lti_initializer.get_or_create_group(course_id=1, title="Don't update")
    #     self.assertEqual(initializer_group, existing_group)
    # 
    # def test_get_or_create_group_creates_new(self):
    #     lti_initializer = LtiInitializerView()
    #     lti_initializer.get_or_create_group(course_id=2, title="Newly created", user=self.created_user)
    #     created_group = Group.objects.get(class_key=2)
    #     self.assertEqual(created_group.title, "Newly created")
    
    def test_initialize_group_exists(self):
        """ The group should title and stuff shouldn't be overwritten if it already exists """
        Group.objects.create(class_key=1, title="Original title", created_by=self.created_user)
        lti_initializer = LtiInitializerView()
        teacher_role = "urn:something/something-else/Instructor,urn:something/something-else/Student"
        lti_initializer.initialize_group("1", "A different title", teacher_role, self.created_user)
        existing_group = Group.objects.get(class_key=1)
        self.assertEqual(existing_group.title, "Original title")
        
    def test_initialize_group_new(self):
        """ Creates a new group where one does not yet exist """
        lti_initializer = LtiInitializerView()
        teacher_role = "urn:something/something-else/Instructor,urn:something/something-else/Student"
        lti_initializer.initialize_group("2", "A different title", teacher_role, self.created_user)
        new_group = Group.objects.get(class_key=2)
        self.assertEqual(new_group.title, "A different title")

    def test_role_is_added(self):
        lti_initializer = LtiInitializerView()
        Group.objects.create(class_key=1, title="Test title", created_by=self.created_user)
        group = Group.objects.get(class_key=1)
        user = User.objects.get(username="user1")
        lti_initializer.update_roles(user=user, group=group, role="Student")
        self.assertTrue(user in group.students.all())

    def test_role_is_updated(self):
        lti_initializer = LtiInitializerView()
        Group.objects.create(class_key=1, title="Test title", created_by=self.created_user)
        group = Group.objects.get(class_key=1)
        user = User.objects.get(username="user1")
        lti_initializer.update_roles(user=user, group=group, role="Student")
        self.assertTrue(user in group.students.all())
        lti_initializer.update_roles(user=user, group=group, role="Teacher")
        self.assertFalse(user in group.students.all())
        self.assertTrue(user in group.teachers.all())
        
    def test_create_lti_user(self):
        lti_initializer = LtiInitializerView()
        email = "testMasterFlash@example.com"
        lti_initializer.create_lti_user(email)
        user = User.objects.get(email=email)
        self.assertEqual(user.username, email)
        self.assertEqual(user.profile.display_name, "testMasterFlash")

    def test_determine_role(self):
        lti_initializer = LtiInitializerView()
        teacher_role = "urn:something/something-else/Instructor,urn:something/something-else/Student"
        self.assertEqual(lti_initializer.determine_role(teacher_role), "Teacher")
        student_role = "urn:something/something-else/not-Instructor,urn:something/something-else/Student"
        self.assertEqual(lti_initializer.determine_role(student_role), "Student")
        # roles of None will also return "Student"
        self.assertEqual(lti_initializer.determine_role(None), "Student")

    def test_dispatch_advises_relaunch(self):
        """ Test missing POST parameters will advise user to relaunch """
        response = self.client.post(
            "/lti/lti_initializer/",
            {
                "lis_person_contact_email_primary": "user1@example.com"
            }
        )
        self.assertContains(response, "Your session has expired. Please, relaunch the tool via your canvas course.")

    # Until I can figure out how to mock a verified LTI launch
    # def test_dispatch(self):
    #     """ Test successful dispatch redirects to home """
    #     response = self.client.post(
    #         "/lti/lti_initializer/",
    #         {
    #             "lis_person_contact_email_primary": "user1@example.com",
    #             "custom_canvas_course_id": "327",
    #             "context_title": "test title",
    #             "ext_roles": "urn:something/something-else/Instructor,urn:something/something-else/Student"
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, "/")
