from django.test import TestCase
from django.urls import reverse
from iha.models import IHA, IHACategory
from django.contrib.auth.models import User


class URLTests(TestCase):
    print("test checking page urls")

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_iha_add(self):
        response = self.client.get("/iha/add/")
        self.assertEqual(response.status_code, 200)

    def test_iha_list(self):
        response = self.client.get("/iha/list/")
        self.assertEqual(response.status_code, 200)


class ModelTests(TestCase):
    print("test database creation")

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='testpassword!')
        self.category = IHACategory.objects.create(name='Test Category')
        self.iha = IHA.objects.create(creator=self.user,
                                 mark='Test Mark',
                                 model='Test Model',
                                 weight=145,
                                 category=self.category)

    def test_category_model(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_iha_model(self):
        self.assertEqual(str(self.iha), "john-Test Mark-Test Model-145")


class APITest(TestCase):
    print("test rest api")

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='testpassword!')
        self.category = IHACategory.objects.create(name='Test Category')
        self.iha = IHA.objects.create(creator=self.user,
                                 mark='Test Mark',
                                 model='Test Model',
                                 weight=145,
                                 category=self.category)

    def test_get_iha_list(self):
        url = reverse("api-iha-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_iha_detail(self):

        url = reverse("api-iha-detail", kwargs={'pk': self.iha.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_iha(self):
        url = reverse("api-iha-list")

        data = {
            "mark": "Test Mark",
            "model": "Test Model",
            "weight": 123.5,
            "status": False,
            "creator": self.user.id,
            "category": self.category.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_delete_iha(self):

        url = reverse("api-iha-detail", kwargs={'pk': self.iha.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_get_category_list(self):
        url = reverse("api-iha-category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        url = reverse("api-iha-category-list")
        data = {
            "name": "Test Category",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

