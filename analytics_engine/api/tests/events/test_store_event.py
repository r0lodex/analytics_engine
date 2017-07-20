from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from ae_reflex.models import User, Project


class SendEventTestCase(TestCase):

    def setUp(self):
        self.client = client = APIClient()
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get('/')
        register_url = reverse('register')
        data = {"username": "userA", "password": "123456"}
        client.post(register_url, data)
        self.user = User.objects.get(username=data['username'])
        client.force_authenticate(self.user)
        create_project_url = reverse('create_project')
        data = {"name": "Page Views"}
        response = client.post(create_project_url, data)
        self.external_id = external_id = response.data['external_id']
        self.source_keys = response.data['source_keys']

    def test_send_event(self):
        data = {"product_id": "1", "merchant_id": "1"}
        send_event_url = reverse('store_event', kwargs={"external_id": self.external_id})
        response = self.client.post(send_event_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['source'], 'Unknown')

    def test_send_event_backend_key(self):
        backend_key = self.source_keys['backend_key']
        data = {"product_id": "1", "merchant_id": "1"}
        send_event_url = reverse('store_event', kwargs={"external_id": self.external_id})
        response = self.client.post(send_event_url, data, **{'HTTP_SOURCE_KEY': backend_key})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['source'], 'Backend')

    def test_send_event_web_key(self):
        web_key = self.source_keys['web_key']
        data = {"product_id": "1", "merchant_id": "1"}
        send_event_url = reverse('store_event', kwargs={"external_id": self.external_id})
        response = self.client.post(send_event_url, data, **{'HTTP_SOURCE_KEY': web_key})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['source'], 'Web')

    def test_send_event_key(self):
        mobile_app_key = self.source_keys['mobile_app_key']
        data = {"product_id": "1", "merchant_id": "1"}
        send_event_url = reverse('store_event', kwargs={"external_id": self.external_id})
        response = self.client.post(send_event_url, data, **{'HTTP_SOURCE_KEY': mobile_app_key})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['source'], 'Mobile App')