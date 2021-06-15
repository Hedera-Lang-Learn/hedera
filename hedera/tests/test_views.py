from django.test import TestCase

from django.contrib.auth.models import User
from account.models import Account

class DashboardViewTest(TestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(
                username="test_user1",
                email="test_user1@test.com",
                password="password"
            )
    
    def test_dashboard_correct_template(self):
        self.client.login( username="test_user1", email="test_user1@test.com", password="password")
        dash_response = self.client.get('/account/dashboard/')
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Dashboard")
        self.assertTemplateUsed(dash_response, "dashboard.html")
    # docs for redirect_chain https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
    def test_login_redirect_to_dashboard(self):
        dash_response = self.client.get('/account/dashboard/', follow=True)
        self.assertEqual(dash_response.redirect_chain[0][0], "/account/login/?next=/account/dashboard/")
        self.assertEqual(dash_response.redirect_chain[0][1], 302)