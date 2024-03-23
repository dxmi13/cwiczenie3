import unittest
import os
from pkt2 import connect_db, create_account, verify_password

"""
  Testy jednostkowe.
"""
class TestPasswordLibrary(unittest.TestCase):

    """Metoda ustawiająca środowisko testowe."""
    @classmethod
    def setUpClass(cls):
        cls.db_path = 'test_users.db'
        cls.conn, cls.cursor = connect_db(cls.db_path)
    
    """Metoda sprzątająca po testach."""
    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        os.remove(cls.db_path)
    
    """Test tworzenia nowego konta."""
    def test_create_account(self):
        result = create_account(self.cursor, 'testuser', 'testpassword')
        self.assertEqual(result, "Konto zostało utworzone.")
    
    """Test próby utworzenia konta z istniejącą już nazwą użytkownika."""
    def test_create_account_with_existing_username(self):
        create_account(self.cursor, 'existinguser', 'password1')
        result = create_account(self.cursor, 'existinguser', 'password2')
        self.assertEqual(result, "Nazwa użytkownika jest już zajęta.")

    """Test weryfikacji poprawnego hasła."""
    def test_verify_password_correct(self):
        username = 'user_correct'
        password = 'correct_password'
        create_account(self.cursor, username, password)
        self.assertTrue(verify_password(self.cursor, username, password))
    
    """Test weryfikacji niepoprawnego hasła."""
    def test_verify_password_incorrect(self):
        username = 'user_incorrect'
        password = 'real_password'
        create_account(self.cursor, username, password)
        self.assertFalse(verify_password(self.cursor, username, 'fake_password'))

    """Test weryfikacji dla nieistniejącego użytkownika."""
    def test_user_not_exist(self):
        self.assertFalse(verify_password(self.cursor, 'nonexistent_user', 'any_password'))

# Uruchomienie testów jednostkowych.
if __name__ == '__main__':
    unittest.main()