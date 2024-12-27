from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Contact
import base64

class ContactAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Generate Basic Auth headers
        credentials = f"testuser:testpassword"
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode(credentials.encode()).decode()}'
        }

        # Sample contacts
        self.contact_1 = Contact.objects.create(name="John Doe", email="johndoe@example.com")
        self.contact_2 = Contact.objects.create(name="Jane Doe", email="janedoe@example.com")
        self.contact_3 = Contact.objects.create(name="Jake Smith", email="jakesmith@example.com")

        # Valid payloads
        self.valid_payload = {
            "name": "Jan Doe",
            "email": "jdoe@example.com",
        }
        self.invalid_payload = {
            "name": "",
            "email": "invalid-email",
        }

    def test_create_contact(self):
        response = self.client.post("/api/contacts/", self.valid_payload, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_contact(self):
        response = self.client.get(f"/api/contacts/{self.contact_1.id}/", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact(self):
        payload = {
            "name": "Updated Name",
            "email": self.contact_1.email,  # Use the existing email for the contact
        }
        response = self.client.put(f"/api/contacts/{self.contact_1.id}/", payload, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contact(self):
        response = self.client.delete(f"/api/contacts/{self.contact_1.id}/", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_by_name(self):
        response = self.client.get("/api/contacts/?search=Jane", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the correct contact is returned
        self.assertEqual(len(response.data['results']), 1)  # Only 1 result should be found
        self.assertEqual(response.data['results'][0]['name'], "Jane Doe")

    def test_search_by_email(self):
        response = self.client.get("/api/contacts/?search=johndoe@example.com", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the correct contact is returned
        self.assertEqual(len(response.data['results']), 1)  # Only 1 result should be found
        self.assertEqual(response.data['results'][0]['email'], "johndoe@example.com")

    def test_search_pagination(self):
        # Create more contacts to test pagination
        Contact.objects.create(name="Emily Davis", email="emilydavis@example.com")
        Contact.objects.create(name="Chris Lee", email="chrislee@example.com")
        Contact.objects.create(name="Michael Brown", email="michaelbrown@example.com")

        response = self.client.get("/api/contacts/?search=Jane", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination (by default it should return 10 items per page, so here we just check if paginated results are returned)
        self.assertIn('next', response.data)  # Check for pagination info

