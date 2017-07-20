from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from ae_reflex.models import User, Project


class CountQueryTestCase(TestCase):

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
        self.project = Project.objects.get(external_id=external_id)

    def test_count_all_event(self):
        count_all_url = reverse('count_query', kwargs={"external_id": self.external_id})
        data = {"time": "all"}
        response = self.client.post(count_all_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)

    def test_count_last_7_days(self):
        count_last_7_days_url = reverse('count_query', kwargs={"external_id": self.external_id})
        data = {"time": "last_7_days"}
        response = self.client.post(count_last_7_days_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)

    def test_count_last_7_weeks(self):
        count_last_7_weeks_url = reverse('count_query', kwargs={"external_id": self.external_id})
        data = {"time": "last_7_weeks"}
        response = self.client.post(count_last_7_weeks_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)

    def test_count_last_7_months(self):
        count_last_7_months_url = reverse('count_query', kwargs={"external_id": self.external_id})
        data = {"time": "last_7_months"}
        response = self.client.post(count_last_7_months_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)