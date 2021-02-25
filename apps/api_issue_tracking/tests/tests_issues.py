from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import User
from apps.api_issue_tracking.models import Project, Issue, Contributor


class IssuesTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")
        cls.issue_list_url = reverse("project_issues", args=[1])
        cls.issue2_1_url = reverse("project_issue", args=[2, 1])
        cls.issue1_url = reverse("project_issue", args=[1, 1])
        cls.issue2_url = reverse("project_issue", args=[1, 2])
        cls.issue999_url = reverse("project_issue", args=[1, 999])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        u1 = User.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )
        u2 = User.objects.create_user(
            username="demo_user2", email="user@foo.com", password="demopass"
        )

        u1.save()
        u2.save()

        self.user = u1

        # Project & Contributor

        p1 = Project.objects.create(title="projet 1", description="le projet 1")
        p2 = Project.objects.create(title="projet 2", description="le projet 2 sans contrib")

        p1.save()
        p2.save()

        self.projet = p1

        c1 = Contributor.objects.create(
            user=u1, project=p1, permission="ALL", role="ADMIN"
        )

        c1.save()

        # Issues

        i1 = Issue.objects.create(
            title="Issue 1",
            description="l'issue 1",
            project=p1,
            author_user=u1,
        )

        i2 = Issue.objects.create(
            title="Issue 2",
            description="l'issue 2",
            project=p1,
            author_user=u2,
        )

        i1.save()
        i2.save()

    def tearDown(self):
        pass

    def login(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user", "password": "demopass"},
            format="json",
        )
        self.token = resp.data["access"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

    # --- LIST ISSUES ---

    def test_happy_issues_list(self):
        self.login()
        resp = self.client.get(self.issue_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_issues_list_no_auth(self):
        resp = self.client.get(self.issue_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE ISSUE ---

    def test_happy_issue_new_full(self):
        self.login()
        resp = self.client.post(
            self.issue_list_url,
            {
                "title": "New Issue...",
                "description": "Description de l'issue",
                "tag": "BUG",
                "priority": "L",
                "project": 36,
                "status": "TODO",
                # "assignee_user": 'null',
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_issue_new_min(self):
        self.login()
        resp = self.client.post(
            self.issue_list_url,
            {
                "title": "New Issue...",
                "description": "Description de l'issue",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_issue_no_auth(self):
        resp = self.client.post(
            self.issue_list_url,
            {
                "title": "New Issue...",
                "description": "Description de l'issue",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_issue_missing_title(self):
        self.login()
        resp = self.client.post(
            self.issue_list_url,
            {
                "description": "Description de l'issue",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_issue_mising_desc(self):
        self.login()
        resp = self.client.post(
            self.issue_list_url,
            {
                "title": "New Issue...",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_issue_no_data(self):

        self.login()
        resp = self.client.post(
            self.issue_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH ISSUE ---

    def test_happy_issue_fetch(self):
        self.login()
        resp = self.client.get(self.issue1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_issues_fetch_no_auth(self):
        resp = self.client.get(self.issue1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_issue_fetch_other_issue_same_project(self):
        self.login()
        resp = self.client.get(self.issue2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_issue_fetch_other_project_issue(self):
        self.login()
        resp = self.client.get(self.issue2_1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_issue_fetch_not_in_db(self):
        self.login()
        resp = self.client.get(self.issue999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- UPDATE ISSUE ---

    def test_happy_issue_update_full(self):
        self.login()
        resp = self.client.put(
            self.issue1_url,
            {
                "title": "Nouveau titre projet 1",
                "description": "Nouvelle description",
                "type": "AN",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_issue_update_min(self):
        self.login()
        resp = self.client.put(
            self.issue1_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_issue_update_no_title(self):
        self.login()
        resp = self.client.put(
            self.issue1_url, {"description": "Nouvelle description"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_issue_update_no_desc(self):
        self.login()
        resp = self.client.put(
            self.issue1_url, {"title": "Nouveau titre projet 1"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_issue_update_no_data(self):
        self.login()
        resp = self.client.put(self.issue1_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_issue_update_no_auth(self):
        resp = self.client.put(
            self.issue1_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_issue_update_not_contrib(self):
        self.login()
        resp = self.client.put(
            self.issue2_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_happy_issue_update_non_existing_issue(self):
        self.login()
        resp = self.client.put(
            self.issue999_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- DELETE USER ---

    def test_happy_issue_delete(self):
        self.login()
        resp = self.client.delete(self.issue1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_sad_issue_delete_no_auth(self):
        resp = self.client.delete(self.issue1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_issue_delete_not_creator(self):
        self.login()
        resp = self.client.delete(self.issue2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_issue_delete_not_in_db(self):
        self.login()
        resp = self.client.delete(self.issue999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
