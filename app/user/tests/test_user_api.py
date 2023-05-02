# Test for the user API

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Reverse() allows us to get the url of the view we pass as a param
CREATE_USER_URL = reverse("user:create")

TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")

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
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        # Makes a post request to the URL to create a new user
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_create_user_with_email_exists_error(self):
        # Test create email fails if user email exists
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "User One",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short_error(self):
        # Test an error thrown if password less than 5 chars

        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(
            res.status_code, status.HTTP_REQUEST_400_BAD_REQUEST
        )  # noqa: E501
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )  # noqa: E501
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Tests token created on valid credentials
        user_details = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {"email": user_details["email"], "password": user_details["password"]}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_error_if_bad_credentials(self):
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "goodpass",
        }

        create_user(**user_details)

        payload = {"email": "test@example.com", "password": "badpass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_for_no_password(self):
        # Test posting black password results in error

        payload = {"email": "test@example.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_unauthorized(self):
        # Test auth is required for users
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Private Tests (Auth Req.)
class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@example.com", password="testpass234", name="Test Name"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_poast_me_not_allowed(self):
        # Test post not allowed for the me endpoint
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        # Test updating user for auth user
        payload = {"name": "Updated name", "password": "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
