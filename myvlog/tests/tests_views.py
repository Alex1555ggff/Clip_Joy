from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestIndex(TestCase):
    def setUp(self):
        User = get_user_model()
        self.username = 'test_user'
        self.password = '1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)


    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    
    def test_index_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, self.username)
        
        self.assertEqual(response.context['user'].logo.url, self.user.logo.url)