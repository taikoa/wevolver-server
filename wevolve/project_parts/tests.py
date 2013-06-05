import json

from tastypie.test import ResourceTestCase, TestApiClient
from tastypie.serializers import Serializer

from wevolve.projects.models import ProjectPart
from wevolve.project_parts.models import Post, Comment, Document


class PostResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json', 'project_part.json',
                'project.json', 'profile.json',
                'post.json', 'comment.json']

    def setUp(self):
        # Generic
        self.api_client = TestApiClient()
        self.serializer = Serializer()

        # API List data
        self.list_url = '/api/v1/post/'

        # API requests data
        self.project_part_id = 1
        self.post_id = 1
        self.detail_url = '/api/v1/post/{0}/'.format(self.post_id)
        self.project_part_query = '='.join(['?project_part', str(self.project_part_id)])
        self.post_data = {'content': 'My post', 'project_part': {'pk': self.project_part_id}}

        # Open API request data
        self.open_project_part_id = 2
        self.open_post_id = 2
        self.open_detail_url = '/api/v1/post/{0}/'.format(self.open_post_id)
        self.open_project_part_query = '='.join(['?project_part', str(self.open_project_part_id)])
        self.open_post_data = {'content': 'My post', 'project_part': {'pk': self.open_project_part_id}}

    def get_credentials(self):
        result = self.api_client.client.login(email='javaguirre@wadobo.com',
                                              password='django')

    def test_post_list(self):
        self.get_credentials()
        self.assertIn('_auth_user_id', self.api_client.client.session)
        self.assertEqual(self.api_client.client.session['_auth_user_id'], 1)
        self.assertEqual(Post.objects.count(), 2)
        self.assertHttpCreated(self.api_client.post(self.list_url,
                                                    format='json',
                                                    data=self.post_data))
        self.assertEqual(Post.objects.count(), 3)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get(self.list_url,
                                                        format='json'))

    def test_get_list(self):
        self.get_credentials()
        resp = self.api_client.get(''.join([self.list_url, self.project_part_query]),
                                   format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(json.loads(resp.content)['objects']), 1)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    def test_get_detail(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['content'], 'hola')

    # def test_post_list_unauthenticated(self):
    #     self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json',
    #                                                      data=self.post_data))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    def test_put_detail(self):
        self.get_credentials()
        original_data = json.loads(self.api_client.get(self.detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'

        self.assertEqual(Post.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Post.objects.count(), 2)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(Post.objects.count(), 2)
        resp = self.api_client.delete(self.detail_url, format='json')
        self.assertHttpAccepted(resp)
        self.assertEqual(Post.objects.count(), 1)

    # Open Projects
    # FIXME It fails because tastypie is not accessing authorization
    # before calling obj_create
    # def test_post_list_open(self):
    #     self.assertEqual(Post.objects.count(), 2)
    #     resp = self.api_client.post(self.list_url,
    #                                 format='json',
    #                                 data=self.open_post_data)
    #     self.assertHttpUnauthorized(resp)

    def test_get_detail_open(self):
        resp = self.api_client.get(self.open_detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['content'], 'hola')

    def test_delete_detail_open(self):
        self.assertEqual(Post.objects.count(), 2)
        resp = self.api_client.delete(self.open_detail_url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_put_detail_open(self):
        original_data = json.loads(self.api_client.get(self.open_detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'

        self.assertEqual(Post.objects.count(), 2)
        resp = self.api_client.put(self.open_detail_url, format='json', data=new_data)
        self.assertHttpUnauthorized(resp)


class DocumentResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json', 'project_part.json',
                'project.json', 'profile.json',
                'document.json']

    def setUp(self):
        self.api_client = TestApiClient()
        self.project_part_id = 1
        self.document_data = {'text': 'My document', 'project_part': {'pk': self.project_part_id}}
        self.document_id = 1
        self.project_part_query = '='.join(['?project_part', str(self.project_part_id)])
        self.detail_url = '/api/v1/document/{0}/'.format(self.document_id)
        self.list_url = '/api/v1/document/'
        self.serializer = Serializer()

    def get_credentials(self):
        result = self.api_client.client.login(email='javaguirre@wadobo.com',
                                              password='django')

    def test_document_list(self):
        self.get_credentials()
        self.assertIn('_auth_user_id', self.api_client.client.session)
        self.assertEqual(self.api_client.client.session['_auth_user_id'], 1)
        self.assertEqual(Document.objects.count(), 2)
        self.assertHttpCreated(self.api_client.post(self.list_url,
                                                    format='json',
                                                    data=self.document_data))
        self.assertEqual(Document.objects.count(), 3)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get(self.list_url,
                                                        format='json'))

    def test_get_list(self):
        self.get_credentials()
        resp = self.api_client.get(''.join([self.list_url, self.project_part_query]),
                                   format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(json.loads(resp.content)['objects']), 1)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    def test_get_detail(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(json.loads(resp.content)['text'], '<h1>hola</h1>')

    # def test_post_list_unauthenticated(self):
    #     self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json',
    #                                                      data=self.document_data))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={'text': 'data'}))

    def test_put_detail(self):
        self.get_credentials()
        original_data = json.loads(self.api_client.get(self.detail_url, format='json').content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Document'

        self.assertEqual(Document.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Document.objects.count(), 2)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(Document.objects.count(), 2)
        resp = self.api_client.delete(self.detail_url, format='json')
        self.assertHttpAccepted(resp)
        self.assertEqual(Document.objects.count(), 1)


class CommentResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'user_project.json', 'project_part.json',
                'project.json', 'profile.json',
                'post.json', 'comment.json']

    def setUp(self):
        self.api_client = TestApiClient()
        self.post_id = 1
        self.post_data = {'post': {'pk': self.post_id,
                          'text': 'New comment'}}
        self.detail_url = '/api/v1/comment/{0}/'.format(self.post_id)
        self.list_url = '/api/v1/comment/'
        self.serializer = Serializer()

    def get_credentials(self):
        result = self.api_client.client.login(email='javaguirre@wadobo.com',
                                              password='django')

    # def test_post_list(self):
    #     self.get_credentials()
    #     self.assertIn('_auth_user_id', self.api_client.client.session)
    #     self.assertEqual(self.api_client.client.session['_auth_user_id'], 1)
    #     self.assertEqual(Comment.objects.count(), 1)
    #     self.assertHttpCreated(self.api_client.post(self.list_url,
    #                                                 format='json',
    #                                                 data=self.post_data))
    #     self.assertEqual(Comment.objects.count(), 2)

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.list_url,
                                                        format='json'))

    def test_get_list(self):
        self.get_credentials()
        resp = self.api_client.get(self.list_url,
                                   format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(json.loads(resp.content)['objects']), 1)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    # def test_get_detail(self):
    #     self.get_credentials()
    #     resp = self.api_client.get(self.detail_url, format='json')
    #     self.assertValidJSONResponse(resp)
    #     self.assertEqual(json.loads(resp.content)['comment'], '')

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json',
                                                         data=self.post_data))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    def test_put_detail(self):
        self.get_credentials()
        resp = self.api_client.get(self.detail_url, format='json')
        original_data = json.loads(resp.content)
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Comment'

        self.assertEqual(Comment.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data))
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.get_credentials()
        self.assertEqual(Comment.objects.count(), 1)
        resp = self.api_client.delete(self.detail_url, format='json')
        self.assertHttpAccepted(resp)
        self.assertEqual(Comment.objects.count(), 0)
