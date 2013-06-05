from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient


class UserResourceTest(ResourceTestCase):
    fixtures = ['group.json', 'group_permission.json',
                'user_group.json', 'user.json',
                'project.json', 'project_part.json',
                'profile.json']

    def setUp(self):
        self.client = Client()
        result = self.client.login(email='django@javaguirre.net',
                                   password='django')
