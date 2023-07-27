from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.login_url = reverse("acc_app:login")
        self.register_url = reverse("acc_app:register")
        self.profile_url = reverse("acc_app:profile")
        self.home_url = reverse("main_app:home")

        self.test_user = get_user_model().objects.create_user(
            email="test@test.com", password="testpw",
        )

    def test_user_home_view(self):
        self.client.login(email="test@test.com", password="testpw")

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_staff_home_view(self):
        self.test_user.is_staff = True
        self.test_user.save()

        self.client.login(email="test@test.com", password="testpw")

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_superuser_home_view(self):
        self.test_user.is_staff = True
        self.test_user.is_superuser = True
        self.test_user.save()

        self.client.login(email="test@test.com", password="testpw")

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)


class LoginRedirectsTestCase(TestCase):
    def setUp(self):
        self.login_url = reverse("acc_app:login")
        self.search_url = reverse("main_app:search")
        self.library_url = reverse("main_app:library")
        self.profile_url = reverse("acc_app:profile")
        self.library_redirect = "/login?next=/library/"
        self.profile_redirect = "/login?next=/profile/"

        self.test_user = get_user_model().objects.create_user(
            email="test@test.com", password="testpw",
        )

    def test_login_redirect(self):
        response = self.client.post(
            self.login_url, {"email": "test@test.com", "password": "testpw"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.search_url)

    def test_unauth_login_library(self):
        response = self.client.get(self.library_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.library_redirect)

    def test_unauth_login_profile(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_redirect)



class HeaderNavigationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.guest_login = "Login"
        self.guest_register = "Register"
        self.user_profile = "Profile"
        self.user_library = "Library"
        self.home_url = reverse("main_app:home")

        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpw",
        )

    def test_guest_header_navigation(self):
        response = self.client.get(self.home_url)

        self.assertContains(response, self.guest_login)
        self.assertContains(response, self.guest_register)
        self.assertNotContains(response, self.user_profile)
        self.assertNotContains(response, self.user_library)

    def test_user_header_navigation(self):
        self.client.login(email="test@test.com", password="testpw")

        response = self.client.get(self.home_url)

        self.assertNotContains(response, self.guest_login)
        self.assertNotContains(response, self.guest_register)
        self.assertContains(response, self.user_profile)
        self.assertContains(response, self.user_library)

    def test_logout(self):
        self.client.login(email="test@test.com", password="testpw")

        response = self.client.get(reverse("acc_app:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse("_auth_user_id" in self.client.session)
        self.assertRedirects(response, self.home_url)

        response = self.client.get(self.home_url)
        self.assertContains(response, self.guest_login)
        self.assertContains(response, self.guest_register)
