from rest_framework.test import APITestCase
from rest_framework import status
from .models import Contact

class ContactAPITestCase(APITestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="John Doe", email="johndoe@example.com")
        self.valid_payload = {
            "name": "Jane Doe",
            "email": "janedoe@example.com",
        }
        self.invalid_payload = {
            "name": "",
            "email": "invalid-email",
        }

    def test_create_contact(self):
        response = self.client.post("/api/contacts/", self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_contact(self):
        response = self.client.get(f"/api/contacts/{self.contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact(self):
        response = self.client.put(f"/api/contacts/{self.contact.id}/", {"name": "Updated Name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contact(self):
        response = self.client.delete(f"/api/contacts/{self.contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
