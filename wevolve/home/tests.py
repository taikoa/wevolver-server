from tastypie.test import ResourceTestCase, TestApiClient


class CategoryResourceTest(ResourceTestCase):
    fixtures = ['category.json']

    def setUp(self):
        self.category = {'name': 'My category'}
        self.api_client = TestApiClient()

    # def test_get_category(self):
    #     self.assertHttpOK(self.api_client.get('/api/v1/category/',
    #                       format='json'))

    # def test_post_category(self):
    #     self.assertHttpUnauthorized(self.api_client.post('/api/v1/category/',
    #                                 format='json',
    #                                 data=self.category))
