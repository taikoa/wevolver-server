import json

from tastypie.test import ResourceTestCase, TestApiClient
from tastypie.serializers import Serializer

from wevolve.projects.models import ProjectPart
from wevolve.tasks.models import Task


class TaskResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json', 'project_part.json',
                'project.json', 'profile.json',
                'task.json']

    def setUp(self):
        self.api_client = TestApiClient()
        self.task_id = 1
        self.project_part_id = 1
        self.task = {'description': 'new Task',
                     'project_part': {'pk': self.project_part_id},
                     'flag_finished': 0,
                     'weight': 20
                     }
        self.detail_url = '/api/v1/task/{0}/'.format(self.task_id)
        self.project_part_query = '='.join(['?project_part', str(self.project_part_id)])
        self.list_url = '/api/v1/task/'
        self.serializer = Serializer()

    def get_credentials(self):
        result = self.api_client.client.login(email='javaguirre@wadobo.com',
                                              password='django')

    def test_post_list(self):
        self.get_credentials()
        self.assertIn('_auth_user_id', self.api_client.client.session)
        self.assertEqual(self.api_client.client.session['_auth_user_id'], 1)
        self.assertEqual(Task.objects.count(), 2)
        resp = self.api_client.post(self.list_url,
                                    format='json',
                                    data=self.task)
        self.assertHttpCreated(resp)
        self.assertEqual(Task.objects.count(), 3)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(''.join([self.list_url, self.project_part_query]),
                                            format='json'))

    def test_get_list_json(self):
        self.get_credentials()
        resp = self.api_client.get(''.join([self.list_url, self.project_part_query]),
                                   format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(json.loads(resp.content)['objects']), 2)

    def test_get_detail_unauthenticated(self):
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_detail_json(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['description'], 'new task')

    # def test_post_list_unauthenticated(self):
    #     self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json',
    #                                                      data=self.task))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    def test_put_detail(self):
        self.get_credentials()
        original_data = json.loads(self.api_client.get(self.detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Task'

        self.assertEqual(Task.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data))
        self.assertEqual(Task.objects.count(), 2)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(Task.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json'))
        self.assertEqual(Task.objects.count(), 1)

    # TODO Tests with open projects
