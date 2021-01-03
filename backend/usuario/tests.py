from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from tabelas.models import Usuario


class TestCreateUserView(APITestCase):
    def setUp(self):
        url = reverse_lazy('user-add')
        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "test",
            "first_name": "Jose",
            "last_name": "Pedro",
            "is_staff": True,
            "is_superuser": True
        }
        self.response = self.client.post(url, data=data)

    def test_status_code_returns_201(self):
        self.assertEquals(status.HTTP_201_CREATED, self.response.status_code)

    def test_data_is_returned_without_password(self):
        self.assertNotIn('password', self.response.data)

    def test_data_is_returned(self):
        campos = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active'
        )
        for campo in campos:
            with self.subTest():
                self.assertIn(campo, self.response.data.keys())


class TestLoginView(APITestCase):
    def setUp(self):
        user = Usuario.objects.create(
            email="test@example.com",
            username="test",
            is_superuser=True,
            is_active=True,
        )
        user.set_password('test')
        user.save()

        url = reverse_lazy('token_obtain_pair')
        self.response = self.client.post(url, {'username':'test', 'password':'test'})

    def test_status_code_returns_200(self):
        self.assertEquals(status.HTTP_200_OK, self.response.status_code)

    def test_token_is_in_response(self):
        keys = (
            'access', 'refresh'
        )
        for key in keys:
            with self.subTest():
                self.assertIn(key, self.response.data.keys())


class TestChangePasswordView(APITestCase):
    def setUp(self):
        self.url = reverse_lazy('user-password-change')
        user = Usuario.objects.create(
            email="test@example.com",
            username="test",
            is_superuser=True,
            is_active=True,
        )
        user.set_password('test')
        user.save()
        self.token = self.client.post(
            reverse_lazy('token_obtain_pair'), 
            {'username':'test', 'password':'test'}
        ).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_password_has_change(self):
        self.client.put(
            self.url, 
            {'password':'alo mundo'},
        )
        response = self.client.post(
            reverse_lazy('token_obtain_pair'), 
            {'username':'test', 'password':'alo mundo'}
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)
    
    def test_view_return_success_message(self):
        response = self.client.put(
            self.url, 
            {'password':'alo mundo'},
        )
        self.assertIn("Password updated successfully", response.data.values())

    def test_view_return_error_with_data(self):
        response = self.client.put(
            self.url, 
            {'passwrd':'alo mundo'},
        )
        self.assertIn("error", response.data.keys())

#Ajustar Envio do Token para testes    
class TestUserListView(APITestCase):
    def setUp(self):
        url = reverse_lazy('user-list')
        user = Usuario.objects.create(
            email="test@example.com",
            username="test",
            is_staff=False,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('test')
        user.save()
        self.token = self.client.post(
            reverse_lazy('token_obtain_pair'), 
            {'username':'test', 'password':'test'}
        ).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.response = self.client.get(url)

    def test_status_code_returns_200(self):
        self.assertEquals(status.HTTP_200_OK, self.response.status_code)

    def test_data_return_is_array(self):
        self.assertTrue(isinstance(self.response.data, list))

    def test_data_is_returned(self):
        campos = (
            "email",
            "username",
            "first_name",
            "last_name",
            "is_superuser",
            "is_active",
        )
        for campo in campos:
            with self.subTest():
                self.assertIn(campo, self.response.data[0].keys())

    def test_data_is_not_returning_password(self):
        for data in self.response.data:
            with self.subTest():
                self.assertNotIn('password', data.keys())
        