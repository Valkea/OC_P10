from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import User


class UsersTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")
        cls.signup_url = reverse("user_signup")
        cls.users_list_url = reverse("users_list")
        cls.user1_details_url = reverse("user_details", args=[1])
        cls.user2_details_url = reverse("user_details", args=[2])
        cls.user999_details_url = reverse("user_details", args=[999])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        u1 = User.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )

        u2 = User.objects.create_user(
            username="second_user", email="second_user@foo.com", password="demopass2"
        )

        u1.save()
        u2.save()

    def tearDown(self):
        pass

    # --- HELPERS FUNCTIONS ---

    def login(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user", "password": "demopass"},
            format="json",
        )
        self.token = resp.data["access"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

    # --- LOGIN / LOGOUT ---

    def test_happy_login(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user", "password": "demopass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in resp.data)
        self.assertTrue("access" in resp.data)
        # token = resp.data["access"]
        # print(token)

    def test_sad_login_wrong_username(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_login_wrong_password(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_login_missing_username(self):
        resp = self.client.post(
            self.login_url, {"password": "wrongpass"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_login_missing_password(self):
        resp = self.client.post(
            self.login_url, {"username": "demo_user"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_login_no_data(self):
        resp = self.client.post(self.login_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- SIGNUP ---

    def test_happy_signup_full(self):
        resp = self.client.post(
            self.signup_url,
            {
                "username": "new_user",
                "password": "new_user_pass",
                "first_name": "first name",
                "last_name": "last name",
                "email": "user@email.com",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_signup_min(self):
        resp = self.client.post(
            self.signup_url,
            {"username": "new_user", "password": "new_user_pass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_signup_not_an_email(self):
        resp = self.client.post(
            self.signup_url,
            {
                "username": "new_user",
                "password": "new_user_pass",
                "email": "noAnEmail.com",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_signup_missing_username(self):
        resp = self.client.post(
            self.signup_url, {"password": "new_user_pass"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_signup_missing_password(self):
        resp = self.client.post(
            self.signup_url, {"username": "new_user"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_signup_no_data(self):
        resp = self.client.post(self.signup_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- LIST USERS ---

    def test_happy_users_list(self):
        self.login()
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_users_list_no_auth(self):
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- FETCH USER ---

    def test_happy_user_fetch(self):
        self.login()
        resp = self.client.get(self.user1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_users_fetch_no_auth(self):
        resp = self.client.get(self.user1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE USER ---

    def test_happy_user_update_full(self):
        self.login()
        resp = self.client.put(
            self.user1_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
                "email": "updated@email.com",
                "first_name": "first name",
                "last_name:": "last name",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_user_update_min(self):
        self.login()
        resp = self.client.put(
            self.user1_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_user_update_not_an_email(self):
        self.login()
        resp = self.client.put(
            self.user1_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
                "email": "updatedemail.com",
                "first_name": "first name",
                "last_name:": "last name",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_user_update_no_password(self):
        self.login()
        resp = self.client.put(
            self.user1_details_url,
            {
                "username": "updated_user",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_user_update_no_username(self):
        self.login()
        resp = self.client.put(
            self.user1_details_url,
            {
                "password": "updated_password",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_user_update_no_data(self):
        self.login()
        resp = self.client.put(self.user1_details_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sad_user_update_no_auth(self):
        resp = self.client.put(
            self.user1_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- DELETE USER ---

    def test_happy_user_delete(self):
        self.login()
        resp = self.client.delete(self.user1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_sad_users_delete_no_auth(self):
        resp = self.client.delete(self.user1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- ACT ON SOMEONE ELSE PROFILE ---

    # FETCH
    def test_happy_user_fetch_not_current_user(self):
        self.login()
        resp = self.client.get(self.user2_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # UPDATE
    def test_sad_user_update_not_current_user(self):
        resp = self.client.put(
            self.user2_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_sad_user_delete_not_current_user(self):
        self.login()
        resp = self.client.delete(self.user2_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # --- ACT ON NON EXISTING PROFILE ---

    # FETCH
    def test_sad_user_fetch_not_in_db(self):
        self.login()
        resp = self.client.get(self.user999_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    def test_sad_user_update_not_in_db(self):
        resp = self.client.put(
            self.user999_details_url,
            {
                "username": "updated_user",
                "password": "updated_password",
            },
            format="json",
        )
        self.assertEqual(
            resp.status_code, status.HTTP_401_UNAUTHORIZED
        )  # NOTE not 404 ?

    # DELETE
    def test_sad_user_delete_not_in_db(self):
        self.login()
        resp = self.client.delete(self.user999_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class JwtTests(APITestCase):
    def test_api_jwt(self):

        url = reverse("token_obtain_pair")
        u = User.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )
        u.is_active = False
        u.save()

        resp = self.client.post(
            url, {"username": "demo_user", "password": "wrongpass"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        u.is_active = True
        u.save()

        resp = self.client.post(
            url, {"username": "demo_user", "password": "demopass"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in resp.data)
        self.assertTrue("access" in resp.data)
        token = resp.data["access"]
        # print(token)

        verification_url = reverse("token_verify")

        resp = self.client.post(verification_url, {"token": token}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(verification_url, {"token": "abc"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION="JWT " + "abc")
        resp = client.get("/projects/", data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        resp = client.get("/projects/", data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
