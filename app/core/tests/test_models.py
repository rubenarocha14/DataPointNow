# Test for Models

from django.test import TestCase

# Imports models
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    # Test models

    def test_create_user_with_email_successful(self):
        # Testing create a user w/ email successful

        email = "test@example.com"
        password = "testpass123"
        # objects is a reference to the obj manager we will create
        # create_user is a method we will later define
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Checks email is the same
        self.assertEqual(user.email, email)
        # Checks that a password works, cannot use assertEqual because
        # the password will be hased and not equal to the saved password
        self.assertTrue(user.check_password(password))

    def test_for_new_email_normalized(self):
        # est email is normalized
        sameple_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sameple_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        # Test new user w/o email raises error

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        # Test creating superuser
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
