# Test for the Django Admin mods

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    # Test Django admin

    def setUp(self):
        # Create user and client

        # Allows us to make requests
        self.client = Client()
        # Creates a test superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='test123',
        )
        # Forces the client to auth as superuser
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        # Test that users are listed on page

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        # Test user edit page works
        # assigns url to the user change page for the speced user
        url = reverse('admin:core_user_change', args=[self.user.id])
        # gets the url using superuser auth
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        # Test to create user page works

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
