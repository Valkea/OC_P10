from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import User
from apps.api_issue_tracking.models import Project, Issue, Comment, Contributor


class CommentsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")
        cls.comment_list_url = reverse("project_issue_comments", args=[1, 1])
        cls.comment2_1_url = reverse("project_issue_comment", args=[2, 1, 1])
        cls.comment1_url = reverse("project_issue_comment", args=[1, 1, 1])
        cls.comment2_url = reverse("project_issue_comment", args=[1, 1, 2])
        cls.comment999_url = reverse("project_issue_comment", args=[1, 1, 999])

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

        # Issue

        i1 = Issue.objects.create(
            title="Issue 1",
            description="l'issue 1",
            project=p1,
            author_user=u1,
        )

        i2 = Issue.objects.create(
            title="Issue 1",
            description="l'issue 1",
            project=p2,
            author_user=u2,
        )

        i1.save()
        i2.save()

        # Comments

        co1 = Comment.objects.create(
            description="comment 1",
            issue=i1,
            author_user=u1,
        )

        co2 = Comment.objects.create(
            description="comment 2",
            issue=i1,
            author_user=u2,
        )

        co1.save()
        co2.save()

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

    # --- LIST COMMENTS ---

    def test_happy_comments_list(self):
        self.login()
        resp = self.client.get(self.comment_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_comments_list_no_auth(self):
        resp = self.client.get(self.comment_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE COMMENT ---

    def test_happy_comment_new(self):
        self.login()
        resp = self.client.post(
            self.comment_list_url,
            {
                "description": "Description de l'comment",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_comment_no_auth(self):
        resp = self.client.post(
            self.comment_list_url,
            {
                "description": "Description de l'comment",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_comment_mising_desc(self):
        self.login()
        resp = self.client.post(
            self.comment_list_url,
            {
                "title": "New Comment...",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_comment_no_data(self):

        self.login()
        resp = self.client.post(
            self.comment_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH COMMENT ---

    def test_happy_comment_fetch(self):
        self.login()
        resp = self.client.get(self.comment1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_comments_fetch_no_auth(self):
        resp = self.client.get(self.comment1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_comment_fetch_other_comment_same_project(self):
        self.login()
        resp = self.client.get(self.comment2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_comment_fetch_other_project_comment(self):
        self.login()
        resp = self.client.get(self.comment2_1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_comment_fetch_not_in_db(self):
        self.login()
        resp = self.client.get(self.comment999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- UPDATE COMMENT ---

    def test_happy_comment_update(self):
        self.login()
        resp = self.client.put(
            self.comment1_url,
            {"description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_comment_update_no_data(self):
        self.login()
        resp = self.client.put(self.comment1_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_comment_update_no_auth(self):
        resp = self.client.put(
            self.comment1_url,
            {"description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_comment_update_not_contrib(self):
        self.login()
        resp = self.client.put(
            self.comment2_url,
            {"description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_happy_comment_update_non_existing_comment(self):
        self.login()
        resp = self.client.put(
            self.comment999_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- DELETE USER ---

    def test_happy_comment_delete(self):
        self.login()
        resp = self.client.delete(self.comment1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_sad_comment_delete_no_auth(self):
        resp = self.client.delete(self.comment1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_comment_delete_not_creator(self):
        self.login()
        resp = self.client.delete(self.comment2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_comment_delete_not_in_db(self):
        self.login()
        resp = self.client.delete(self.comment999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
