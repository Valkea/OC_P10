from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import User
from apps.api_issue_tracking.models import Project, Contributor


class ContributorsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")

        cls.contributor_list_url = reverse("project_users", args=[1])
        cls.contributor_list_url2 = reverse("project_users", args=[2])

        cls.contributor1_url = reverse("project_user", args=[1, 1])
        cls.contributor2_url = reverse("project_user", args=[1, 2])
        cls.contributor999_url = reverse("project_user", args=[1, 999])

        cls.contributor2_1_url = reverse("project_user", args=[2, 1])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        # 'we' are u1
        #
        # p1 (u1, u2)
        # p2 (u3)

        u1 = User.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )

        u2 = User.objects.create_user(
            username="demo_user2", email="user2@foo.com", password="demopass2"
        )

        u3 = User.objects.create_user(
            username="demo_user3", email="user3@foo.com", password="demopass3"
        )

        u1.save()
        u2.save()
        u3.save()
        self.user = u1

        # Contributors

        p1 = Project.objects.create(title="projet 1", description="le projet 1")
        p2 = Project.objects.create(title="projet 2", description="le projet 2")

        p1.save()
        p2.save()

        # Contributors

        c1 = Contributor.objects.create(
            user=u1, project=p1, permission="ALL", role="ADMIN"
        )

        c2 = Contributor.objects.create(
            user=u2, project=p1, permission="ALL", role="ADMIN"
        )

        c3 = Contributor.objects.create(
            user=u3, project=p2, permission="ALL", role="ADMIN"
        )

        c1.save()
        c2.save()
        c3.save()

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

    # --- LIST CONTRIBUTORS ---

    def test_happy_contributors_list(self):
        self.login()
        resp = self.client.get(self.contributor_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_contributors_list_no_auth(self):
        resp = self.client.get(self.contributor_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE CONTRIBUTOR ---

    def test_happy_contributor_new_full(self):
        self.login()
        resp = self.client.post(
            self.contributor_list_url,
            {
                "user": 3,
                "permission": "READ",
                "role": "CONTRIB",
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_contributor_new_min(self):
        self.login()
        resp = self.client.post(
            self.contributor_list_url,
            {
                "user": 3,
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_contributor_no_auth(self):
        resp = self.client.post(
            self.contributor_list_url,
            {
                "user": 3,
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_contributor_missing_user(self):
        self.login()
        resp = self.client.post(
            self.contributor_list_url,
            {
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_contributor_missing_project(self):
        self.login()
        resp = self.client.post(
            self.contributor_list_url,
            {
                "user": 3,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_contributor_no_data(self):

        self.login()
        resp = self.client.post(
            self.contributor_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH CONTRIBUTOR ---

    def test_happy_contributor_fetch(self):
        self.login()
        resp = self.client.get(self.contributor1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_contributors_fetch_no_auth(self):
        resp = self.client.get(self.contributor1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE CONTRIBUTOR ---

    def test_happy_contributor_update_full(self):
        self.login()
        resp = self.client.put(
            self.contributor1_url,
            {
                "permission": "ALL",
                "role": "ADMIN",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_contributor_update_readonly_data(self):
        self.login()
        resp = self.client.put(
            self.contributor1_url,
            {
                "user": 3,
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_contributor_update_readonly_user(self):
        self.login()
        resp = self.client.put(
            self.contributor1_url,
            {
                "user": 2,
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_contributor_update_readonly_project(self):
        self.login()
        resp = self.client.put(
            self.contributor1_url,
            {
                "project": 2,
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_contributor_update_no_data(self):
        self.login()
        resp = self.client.put(self.contributor1_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- DELETE USER ---

    def test_happy_contributor_delete(self):
        self.login()
        resp = self.client.delete(self.contributor1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_sad_contributor_delete_no_auth(self):
        resp = self.client.delete(self.contributor1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- ACT ON A CONTRIBUTOR OF A PROJECT ON WHICH CURRENT USER IS NOT COLLABORATOR ---

    # LIST
    def test_sad_contributors_list_non_collab_contributor(self):
        self.login()
        resp = self.client.get(self.contributor_list_url2, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # CREATE
    def test_sad_contributor_new_non_collar_contributor(self):
        self.login()
        resp = self.client.post(
            self.contributor_list_url2,
            {
                "user": 2,
                "project": 2,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # FETCH
    def test_sad_contributor_fetch_non_collab_contributor(self):
        self.login()
        resp = self.client.get(self.contributor2_1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # UPDATE
    def test_happy_contributor_update_non_collab_contributor(self):
        self.login()
        resp = self.client.put(
            self.contributor2_1_url,
            {
                "user": 3,
                "project": 1,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE
    def test_sad_contributor_delete_non_collab_contributor(self):
        self.login()
        resp = self.client.delete(self.contributor2_1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # --- ACT ON NON EXISTING CONTRIBUTOR ---

    # FETCH
    def test_sad_contributor_fetch_not_in_db(self):
        self.login()
        resp = self.client.get(self.contributor999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    def test_happy_contributor_update_not_in_db(self):
        self.login()
        resp = self.client.put(
            self.contributor999_url,
            {
                "permission": "ALL",
                "role": "ADMIN",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE
    def test_sad_contributor_delete_not_in_db(self):
        self.login()
        resp = self.client.delete(self.contributor999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
