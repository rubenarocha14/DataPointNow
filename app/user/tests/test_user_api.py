# Test for the user API

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Reverse() allows us to get the url of the view we pass as a param
CREATE_USER_URL = reverse('user:create')

# Helper function that will create a user for testing
# **params allows us to pass any params/dictionary in
def create_user(**params):
    # Create and return a new user
    return get_user_model().objects.create_user(**params)

# Public Tests (Auth not required)
class PublicUserApiTests(TestCase):
    # Test the public features of the user API
    def setUp(self):
        # Establishes a client to make requests
        self.client = APIClient()

    def test_create_user_successful(self):
        # Test create user successful
        payload = {
            'email' : 'test@example.com',
            'password' : 'testpass123',
            'name': 'Test Name'
        }
        # Makes a post request to the URL to create a new user
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_create_user_with_email_exists_error(self):
        # Test create email fails if user email exists
        payload = {
            'email' : 'test@example.com',
            'password' : 'testpass123',
            'name' : 'User One',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short_error(self):
        # Test an error thrown if password less than 5 chars

        payload = {
            'email' : 'test@example.com',
            'password' : 'pw',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_REQUEST_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)





# Private Tests (Auth Req.)