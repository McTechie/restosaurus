from django.test import TestCase
from django.contrib.auth.models import User


class MenuTestUnauthenticated(TestCase):
    def test_list_menu_items_unauthenticated(self):
        response = self.client.get("/api/menu/items/")
        self.assertEqual(response.status_code, 401)

class MenuTestAuthenticated(TestCase):    
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # authenticate user
        res = self.client.post("/api/auth/login/", {"username": "testuser", "password": "testpass"})
        # get the token
        self.token = res.data["access"]

    def test_list_menu_items_authenticated(self):
        response = self.client.get("/api/menu/items/", HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, 200)
    
