import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("accounts:list")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "email":"test@vicky.com",
			"username":"vickyz",
			"first_name":"vicky",
			"last_name":"kumar",
			"password":"1234567",
			"confirm_password":"MISMATCH",
			"bio":"My Life",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """

        user_data = {
            "email":"test@vicky.com",
			"username":"vickyz",
			"first_name":"vicky",
			"last_name":"kumar",
			"password":"1234567",
			"confirm_password":"1234567",
			"bio":"My Life",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "email":"test@vicky.com",
			"username":"vickyz",
			"first_name":"vicky",
			"last_name":"kumar",
			"password":"1234567",
			"confirm_password":"1234567",
			"bio":"My Life",
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "email":"test@vicky.com",
			"username":"vickyz",
			"first_name":"vicky",
			"last_name":"kumar",
			"password":"1234567",
			"confirm_password":"1234567",
			"bio":"My Life",
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("accounts:login")

    def setUp(self):
        self.username = "mister"
        self.email = "mister@vicky.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "vicky"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "mylife"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("auth_token" in json.loads(response.content))
