from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from ae_reflex.models import User


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get('/')

    def test_valid_user_registration(self):
        client = APIClient()

        register_url = reverse('register')
        data = {"username": "userA", "password": "123456"}
        response = client.post(register_url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email_domain_user_registration(self):
        client = APIClient()

        register_url = reverse('register')
        data = {"username": "testuser"}
        response = client.post(register_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.client = client = APIClient()
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get('/')
        register_url = reverse('register')
        data = {"username": "userA", "password": "123456"}
        client.post(register_url, data)
        self.user = User.objects.get(username=data['username'])
        client.force_authenticate(self.user)

    def test_get_user_profile(self):
        user_profile_url = reverse('user_profile')
        response = self.client.get(user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('url', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_put_user_profile(self):
        user_profile_url = reverse('user_profile')
        data = {"email": "test@user.com"}
        response = self.client.put(user_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])






