from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestLogin(TestCase):
    def setUp(self):
        User = get_user_model()
        self.username = 'test_user'
        self.password = '1234'
        user = User.objects.create_user(username=self.username, password=self.password)
        self.protected_view = reverse('account_management')
    
    def test_login_redirect(self):
        response = self.client.get(self.protected_view)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/users/login?next={self.protected_view}")

    def test_login_success(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.protected_view)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, self.username)