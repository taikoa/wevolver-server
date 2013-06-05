import json

import mock
from tastypie.test import ResourceTestCase, TestApiClient
from tastypie.serializers import Serializer

from wevolve.home.models import Category
from wevolve.projects.models import Project, ProjectPart


class ProjectResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json',
                'project.json', 'profile.json',
                'oauth_client.json', 'oauth_token.json']

    def setUp(self):
        self.api_client = TestApiClient()
        self.token = 'd3d81362dd46f415f17e15211875e1d38bf75898'
        self.category = Category(name='New category')
        self.category.save()
        self.post_data = {'title': 'My project',
                          'description': 'my description',
                          'category': self.category}
        self.project_id = 3
        self.open_project_id = 1
        self.open_detail_url = '/api/v1/project/{0}/'.format(self.open_project_id)
        self.detail_url = '/api/v1/project/{0}/'.format(self.project_id)
        self.list_url = '/api/v1/project/'
        self.serializer = Serializer()

    def get_credentials(self, type_user=None):
        if type_user is 'user':
            self.api_client.client.login(email='django@javaguirre.net',
                                         password='django')
        else:
            self.api_client.client.login(email='javaguirre@wadobo.com',
                                         password='django')

    def test_post_list(self):
        self.get_credentials()
        self.assertIn('_auth_user_id', self.api_client.client.session)
        self.assertEqual(self.api_client.client.session['_auth_user_id'], 1)
        self.assertEqual(Project.objects.count(), 2)
        resp = self.api_client.post(self.list_url,
                                    format='json',
                                    data=self.post_data)
        self.assertHttpCreated(resp)
        self.assertEqual(Project.objects.count(), 3)

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.list_url,
                                                        format='json'))

    def test_get_list_unauthorized_open(self):
        resp = self.api_client.get('?'.join([self.list_url, 'open=true']),
                                                        format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(json.loads(resp.content)['objects']), 1)

    def test_get_list(self):
        self.get_credentials()
        resp = self.api_client.get(self.list_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(json.loads(resp.content)['objects']), 2)

    def test_get_list_oauth(self):
        resp = self.api_client.client.get(self.list_url,
                                          format='json',
                                          **{'HTTP_AUTHORIZATION': 'OAuth %s' % self.token})
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(json.loads(resp.content)['objects']), 2)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    def test_get_detail(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['title'], 'Test Project')

    # FIXME Tastypie is not calling authorization before obj_create call
    # def test_post_list_unauthenticated(self):
    #     self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json',
    #                                                      data=self.post_data))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    @mock.patch('wevolve.projects.api.update_drive_folder')
    def test_put_detail(self, method):
        self.get_credentials()
        original_data = json.loads(self.api_client.get(self.detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'

        self.assertEqual(Project.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data))
        self.assertEqual(Project.objects.count(), 2)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(Project.objects.count(), 2)
        resp = self.api_client.delete(self.detail_url, format='json')
        self.assertHttpAccepted(resp)
        self.assertEqual(Project.objects.count(), 1)

    def test_delete_detail_with_user_perm(self):
        self.get_credentials('user')
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_get_detail_open(self):
        resp = self.api_client.get(self.open_detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['title'], 'OPEN project')

    def test_put_detail_open(self):
        original_data = json.loads(self.api_client.get(self.open_detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Project Open'

        self.assertEqual(Project.objects.count(), 2)
        resp = self.api_client.put(self.open_detail_url, format='json', data=new_data)
        self.assertHttpUnauthorized(resp)

    def test_delete_detail_open(self):
        self.assertEqual(Project.objects.count(), 2)
        resp = self.api_client.delete(self.open_detail_url, format='json')
        self.assertHttpUnauthorized(resp)


class ProjectPartResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json', 'project_part.json',
                'project.json', 'profile.json']

    def setUp(self):
        self.api_client = TestApiClient()
        self.post_data = {'title': 'new part',
                          'project_id': {'pk': 3},
                          'project_part_id': {'pk': 1},
                          'order': 0,
                          'weight': 20
                          }
        self.project_part_id = 1
        self.open_project_part_id = 2
        self.detail_base_url =  '/api/v1/project_part/{0}/'
        self.open_detail_url = self.detail_base_url.format(self.open_project_part_id)
        self.detail_url = self.detail_base_url.format(self.project_part_id)
        self.list_url = '/api/v1/project_part/'
        self.serializer = Serializer()

    def get_credentials(self):
        self.api_client.client.login(email='javaguirre@wadobo.com',
                                     password='django')

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.list_url,
                                                        format='json'))

    def test_get_list(self):
        self.get_credentials()
        self.assertHttpUnauthorized(self.api_client.get(self.list_url, format='json'))

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    def test_get_detail(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(json.loads(resp.content)['title'], 'Project Part 1')

    # FIXME Idem from above
    # def test_post_list_unauthenticated(self):
    #     self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))

    def test_post_list(self):
        self.get_credentials()
        self.assertEqual(ProjectPart.objects.count(), 2)
        resp = self.api_client.post(self.list_url, format='json',
                                    data=self.post_data)
        self.assertHttpCreated(resp)
        self.assertEqual(ProjectPart.objects.count(), 3)

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    @mock.patch('wevolve.projects.api.update_drive_folder')
    def test_put_detail(self, method):
        self.get_credentials()
        content = self.api_client.get(self.detail_url, format='json').content
        original_data = json.loads(content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated First Post'

        self.assertEqual(ProjectPart.objects.count(), 2)
        resp = self.api_client.put(self.detail_url, format='json', data=new_data)
        self.assertHttpAccepted(resp)
        self.assertEqual(ProjectPart.objects.count(), 2)
        self.assertEqual(ProjectPart.objects.get(pk=self.project_part_id).title, 'Updated First Post')

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(ProjectPart.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json'))
        self.assertEqual(ProjectPart.objects.count(), 1)

    # Project parts in open projects
    def test_get_detail_open(self):
        resp = self.api_client.get(self.open_detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['title'], 'Project Part 2')

    def test_put_detail_open(self):
        content = self.api_client.get(self.open_detail_url, format='json').content
        original_data = json.loads(content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated First Post'

        self.assertEqual(ProjectPart.objects.count(), 2)
        resp = self.api_client.put(self.detail_url, format='json', data=new_data)
        self.assertHttpUnauthorized(resp)

    def test_delete_detail_open(self):
        self.assertEqual(ProjectPart.objects.count(), 2)
        resp = self.api_client.delete(self.open_detail_url, format='json')
        self.assertHttpUnauthorized(resp)
