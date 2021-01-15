from http import HTTPStatus

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from users.models import Employee


class UserCreationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_should_render_view(self):
        response = self.client.get(reverse('users:signup_manager'))

        self.assertEqual(response.status_code, HTTPStatus.OK)

        templates = map(lambda template: template.name, response.templates)
        self.assertIn('signup.html', templates)

    def test_should_create_manager(self):
        old_count = Employee.objects.filter(is_staff=True).count()
        data = {
            'username': 'test_user',
            'password1': 'Very_secure123$',
            'password2': 'Very_secure123$',
            'first_name': 'Test name',
            'last_name': 'Test last name'
        }

        response = self.client.post(reverse('users:signup_manager'), data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        new_count = Employee.objects.filter(is_staff=True).count()
        self.assertEqual(new_count, old_count + 1)

    def test_should_create_employee(self):
        old_count = Employee.objects.filter(is_staff=False).count()
        data = {
            'username': 'test_user',
            'password1': 'Very_secure123$',
            'password2': 'Very_secure123$',
            'first_name': 'Test name',
            'last_name': 'Test last name'
        }

        response = self.client.post(reverse('users:signup_employee'), data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        new_count = Employee.objects.filter(is_staff=False).count()
        self.assertEqual(new_count, old_count + 1)
