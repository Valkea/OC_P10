from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import User
from apps.api_issue_tracking.models import Project, Contributor


class ProjectsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")
        cls.project_list_url = reverse("projects")
        cls.project1_url = reverse("project", args=[1])
        cls.project2_url = reverse("project", args=[2])
        cls.project999_url = reverse("project", args=[999])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        u1 = User.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )

        u1.save()

        self.user = u1

        p1 = Project.objects.create(title="projet 1", description="le projet 1")

        p2 = Project.objects.create(title="projet 2", description="le projet 2")

        p1.save()
        p2.save()

        c1 = Contributor.objects.create(
            user=u1, project=p1, permission="ALL", role="ADMIN"
        )

        c1.save()

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

    # --- LIST PROJECTS ---

    def test_happy_projects_list(self):
        self.login()
        resp = self.client.get(self.project_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_projects_list_no_auth(self):
        resp = self.client.get(self.project_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE PROJECT ---

    def test_happy_project_new_has_owner_has_contributor(self):
        self.login()
        resp = self.client.post(
            self.project_list_url,
            {"title": "Titre", "description": "a project"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        contrib = Contributor.objects.filter(project=resp.data["id"]).all()
        self.assertEqual(len(contrib), 1)
        self.assertEqual(self.user, contrib[0].user)

    def test_happy_project_new_full(self):
        self.login()
        resp = self.client.post(
            self.project_list_url,
            {"title": "Titre", "description": "a project", "type": "FE"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_project_new_min(self):
        self.login()
        resp = self.client.post(
            self.project_list_url,
            {"title": "Titre", "description": "a project"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_happy_project_no_auth(self):
        resp = self.client.post(
            self.project_list_url,
            {"title": "Titre", "description": "a project", "type": "FE"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_project_missing_title(self):
        self.login()
        resp = self.client.post(
            self.project_list_url,
            {"description": "a project"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_project_mising_desc(self):
        self.login()
        resp = self.client.post(
            self.project_list_url,
            {"title": "Titre"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_project_no_data(self):

        self.login()
        resp = self.client.post(
            self.project_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH PROJECT ---

    def test_happy_project_fetch(self):
        self.login()
        resp = self.client.get(self.project1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_sad_projects_fetch_no_auth(self):
        resp = self.client.get(self.project1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_project_fetch_other_project(self):
        self.login()
        resp = self.client.get(self.project2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_project_fetch_not_in_db(self):
        self.login()
        resp = self.client.get(self.project999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)  # NOTE 404 ?

    # --- UPDATE PROJECT ---

    def test_happy_project_update_full(self):
        self.login()
        resp = self.client.put(
            self.project1_url,
            {
                "title": "Nouveau titre projet 1",
                "description": "Nouvelle description",
                "type": "AN",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_project_update_min(self):
        self.login()
        resp = self.client.put(
            self.project1_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_happy_project_update_no_title(self):
        self.login()
        resp = self.client.put(
            self.project1_url, {"description": "Nouvelle description"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_project_update_no_desc(self):
        self.login()
        resp = self.client.put(
            self.project1_url, {"title": "Nouveau titre projet 1"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_project_update_no_data(self):
        self.login()
        resp = self.client.put(self.project1_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_project_update_no_auth(self):
        resp = self.client.put(
            self.project1_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_happy_project_update_not_contrib(self):
        self.login()
        resp = self.client.put(
            self.project2_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_happy_project_update_non_existing_project(self):
        self.login()
        resp = self.client.put(
            self.project999_url,
            {"title": "Nouveau titre projet 1", "description": "Nouvelle description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)  # NOTE 404 ?

    # --- DELETE USER ---

    def test_happy_project_delete(self):
        self.login()
        resp = self.client.delete(self.project1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_sad_project_delete_no_auth(self):
        resp = self.client.delete(self.project1_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sad_project_delete_not_current_user(self):
        self.login()
        resp = self.client.delete(self.project2_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sad_project_delete_not_in_db(self):
        self.login()
        resp = self.client.delete(self.project999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)  # NOTE 404 ?
