from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings, Client

from account.models import Account, EmailAddress

from .utils import login_existing_user


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
        self.factory = RequestFactory()
        self.client = Client()
        self.created_user = self.create_user("user1", "user1@example.com", "password")
        
    def test_account_created(self):
        found_user = Account.objects.get(user=self.created_user)
        email_found = EmailAddress.objects.get(user=self.created_user)
        self.assertEqual(self.created_user.pk, found_user.user.pk)
        
    def test_login_existing_user_success(self):
        """Using the user1 which has already been created"""
        c = Client()
        response = self.client.post('/lti/lti_initializer/', {'lis_person_contact_email_primary': 'user1@example.com'})
        user = User.objects.get(username='user1')
        self.assertTrue(user.is_authenticated)
        
    def test_login_existing_user_failure(self):
        """If it fails to find an existing user, it should redirect to LTI signup"""
        c = Client()
        response = self.client.post('/lti/lti_initializer/', {'lis_person_contact_email_primary': 'user2@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/lti/lti_registration")
        
        
class LtiRegistrationViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_can_get_form(self):
        response = self.client.get('/lti/lti_registration', {'lis_person_contact_email_primary': 'user2@example.com'})
        print(response)
        
        
        
        
        
        

# test user authentication via lti
#
# --> user does not have email in backend, create user and authenticate
#
# --> user has email in backend, authenticate


# test class management via lti
#
# --> if class exists, update roles
#
# --> if class does not exist, create it and update roles
