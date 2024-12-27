from django.test import TestCase
from CB.models import Contact
from django.db.utils import IntegrityError

class ContactModelTest(TestCase):
    def setUp(self):
        # Create a sample contact for reuse in tests
        self.contact = Contact.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            address="123 Elm Street, Springfield",
        )

    def test_create_contact(self):
        # Test if a contact can be created successfully
        contact = Contact.objects.create(
            name="Jane Doe",
            email="janedoe@example.com",
            phone_number="0987654321",
            address="456 Oak Street, Shelbyville",
        )
        self.assertEqual(contact.name, "Jane Doe")
        self.assertEqual(contact.email, "janedoe@example.com")
        self.assertEqual(contact.phone_number, "0987654321")
        self.assertEqual(contact.address, "456 Oak Street, Shelbyville")

    def test_email_uniqueness(self):
        # Test that duplicate emails raise an IntegrityError
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                name="Duplicate Email",
                email="johndoe@example.com",  # Same email as self.contact
            )

    def test_optional_fields(self):
        # Test creation of a contact with optional fields omitted
        contact = Contact.objects.create(
            name="No Address",
            email="noaddress@example.com",
        )
        self.assertIsNone(contact.phone_number)
        self.assertIsNone(contact.address)

    def test_string_representation(self):
        # Test the __str__ method
        self.assertEqual(str(self.contact), "John Doe (johndoe@example.com)")

    def test_updated_at_auto_update(self):
        # Test that 'updated_at' changes when a record is updated
        original_updated_at = self.contact.updated_at
        self.contact.name = "John Updated"
        self.contact.save()
        self.contact.refresh_from_db()
        self.assertNotEqual(self.contact.updated_at, original_updated_at)
