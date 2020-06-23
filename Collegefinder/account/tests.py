from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
class TestModels(TestCase):
    def test_user_model(self):
        test_user1 = User.objects.create_user(username='testuser', password='12345')
        test_user1.save()
        login = self.client.login(username='testuser', password='12345')
        print("User created and logged in")