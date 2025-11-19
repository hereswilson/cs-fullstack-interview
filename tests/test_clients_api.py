import unittest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ClientsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    # Ensures the route, validation, and service all wire together correctly.
    def test_patch_client_success(self):
        payload = {
            "firm_id": 1,
            "integration_type": "CSV_IMPORT",
            "field_names": {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "integration_id": "111",
                "phone_numbers": ["555-0001"]
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("client", response.json)
        self.assertEqual(response.json["client"]["email"], "jane@example.com")

    # Verifies schemas detect missing fields inside 'field_names'.
    def test_validation_missing_required_field(self):
        payload = {
            "firm_id": 1,
            "integration_type": "CSV_IMPORT",
            "field_names": {
                # Missing first_name and last_name
                "email": "incomplete@example.com",
                "integration_id": "112",
                "phone_numbers": []
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 400)
        # Verify strictly formatted error structure
        errors = response.json["errors"]
        self.assertTrue(any(e['field'] == 'field_names.first_name' for e in errors))


    # Verifies phone_numbers rejects strings (must be a list).
    def test_validation_invalid_data_type(self):
        payload = {
            "firm_id": 1,
            "integration_type": "CSV_IMPORT",
            "field_names": {
                "first_name": "Bad",
                "last_name": "Type",
                "email": "type@example.com",
                "integration_id": "113",
                "phone_numbers": "not-a-list"  # Invalid
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["errors"][0]["field"], "field_names.phone_numbers")

    # Verifies the Email field validator works.
    def test_validation_invalid_email(self):
        payload = {
            "firm_id": 1,
            "integration_type": "CSV_IMPORT",
            "field_names": {
                "first_name": "Bad",
                "last_name": "Email",
                "email": "not-an-email-address",  # Invalid
                "integration_id": "114",
                "phone_numbers": []
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a valid email address.", str(response.json["errors"]))


    # Verifies that DB constraints (128 chars) are enforced at the API level.
    def test_validation_field_too_long(self):
        long_string = "a" * 129
        payload = {
            "firm_id": 1,
            "integration_type": "CSV_IMPORT",
            "field_names": {
                "first_name": long_string, # Invalid
                "last_name": "Doe",
                "email": "long@example.com",
                "integration_id": "115",
                "phone_numbers": []
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any(e['field'] == 'field_names.first_name' for e in response.json["errors"]))


    # Verifies integration_type logic.
    def test_validation_invalid_integration_type(self):
        payload = {
            "firm_id": 1,
            "integration_type": "UNSUPPORTED_TYPE", # Invalid
            "field_names": {
                "first_name": "Enum",
                "last_name": "Test",
                "email": "enum@example.com",
                "integration_id": "116",
                "phone_numbers": []
            }
        }
        response = self.client.patch('/clients', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Must be one of", str(response.json["errors"]))


    def test_patch_empty_body(self):
        response = self.client.patch('/clients', json={})
        self.assertEqual(response.status_code, 400)
        self.assertGreater(len(response.json["errors"]), 0)