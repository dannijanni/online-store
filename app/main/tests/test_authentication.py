from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)  # Assuming it redirects back to the login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Assuming logout redirects to the home page
        self.assertFalse("_auth_user_id" in self.client.session)
