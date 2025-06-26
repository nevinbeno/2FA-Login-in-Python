import unittest
from unittest.mock import patch
from source_code import validate_phone, validate_password, check_if_registered, check_for_password, validate_name
import bcrypt

# Generate the hash for "password123"
hashed_sample_password = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()

class TestAuthenticationSystem(unittest.TestCase):

    def test_validate_phone_valid(self):
        self.assertTrue(validate_phone("9876543210"))
    
    def test_validate_phone_invalid(self):
        self.assertFalse(validate_phone("12345"))
        self.assertFalse(validate_phone("abcde67890"))

    def test_validate_name_valid(self):
        self.assertTrue(validate_name("Piyush Chaula"))
        self.assertTrue(validate_name("K. T. Ummer"))
        self.assertTrue(validate_name("John V. Mathew"))
        self.assertTrue(validate_name("John George Mathew"))
    def test_validate_name_invalid(self):
        self.assertFalse(validate_name("John V. Mathew.."))
        self.assertFalse(validate_name("John 876"))
        self.assertFalse(validate_name(""))

    def test_validate_password_valid(self):
        self.assertTrue(validate_password("secret235!"))
    def test_validate_password_invalid(self):
        self.assertFalse(validate_password(""))

    @patch('source_code.sqlite3.connect')
    def test_check_if_registered_existing_user(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = ("TestUser",)
        self.assertTrue(check_if_registered("9876543210"))
    
    @patch('source_code.sqlite3.connect')
    def test_check_if_registered_nonexistent_user(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = None
        self.assertFalse(check_if_registered("9876543210"))

    @patch('source_code.sqlite3.connect')
    def test_password_correct(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (hashed_sample_password,)  # Use the correct hash
        self.assertTrue(check_for_password("9876543210", "password123"))

    @patch('source_code.sqlite3.connect')
    def test_password_incorrect(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (hashed_sample_password,)  # Use the same correct hash
        self.assertFalse(check_for_password("9876543210", "wrongpassword"))