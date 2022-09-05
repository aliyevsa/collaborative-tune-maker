from django.urls import reverse
from rest_framework.test import APITestCase
from .model_factories import *
import json

class ProjectTest(APITestCase):
    def setUp(self):
        self.app_user_1 = UserFactory.create(
            pk=1,
        )
        self.app_user_2 = UserFactory.create(
            pk=2,
        )
        self.project_1 = ProjectFactory.create(
            pk=1,
            owner=self.app_user_1,
            collaborator=self.app_user_2
        )
        self.project_2 = ProjectFactory.create(
            pk=2,
            owner=self.app_user_2,
            collaborator=self.app_user_1
        )

    def test_ProjectGet(self):
        url = reverse('project_api', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_ProjectDelete(self):
        url = reverse('project_api', kwargs={'pk': 2})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
    
    def test_ProjectNotFound(self):
        url = reverse('project_api', kwargs={'pk': 3})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    
    def test_ProjectFields(self):
        url = reverse('project_api', kwargs={'pk': 1})
        response = self.client.get(url)
        content = json.loads(response.content)
        
        self.assertTrue(
            all(field in content for field in ['name', 'length', 'owner', 'collaborator'])
        )
