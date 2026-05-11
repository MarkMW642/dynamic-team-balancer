from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.
class AccountTests(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('login'))
        
    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertAlmostEqual(response.status_code, 302)