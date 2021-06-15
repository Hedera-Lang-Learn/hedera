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