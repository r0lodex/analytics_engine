from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from ae_reflex.models import User, Project


class ProjectTestCase(TestCase):

    def setUp(self):
        self.client = client = APIClient()
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get('/')
        register_url = reverse('register')
        data = {"username": "userA", "password": "123456"}
        client.post(register_url, data)
        self.user = User.objects.get(username=data['username'])
        client.force_authenticate(self.user)

    def test_create_project(self):
        create_project_url = reverse('create_project')
        data = {"name": "Page Views"}
        response = self.client.post(create_project_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('url', response.data)
        self.assertIn('external_id', response.data)
        self.assertIn('user', response.data)
        self.assertIn('name', response.data)
        self.assertIn('event', response.data)
        self.assertIn('source_keys', response.data)

        self.assertIn('backend_key', response.data['source_keys'])
        self.assertIn('mobile_app_key', response.data['source_keys'])
        self.assertIn('web_key', response.data['source_keys'])

    def test_get_project_list(self):
        create_project_url = reverse('create_project')
        data = {"name": "Page Views"}
        response = self.client.post(create_project_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project_list_url = reverse('project-list')
        response = self.client.get(project_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_detail(self):
        create_project_url = reverse('create_project')
        data = {"name": "Page Views"}
        response = self.client.post(create_project_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project = Project.objects.get(external_id=response.data['external_id'])
        project_detail_url = reverse('project-detail', kwargs={"pk": project.id})
        response = self.client.get(project_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
