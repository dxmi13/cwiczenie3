import sqlite3
import hashlib
import os

"""
  Tworzenie połączenia do bazy sqlite3 i tabeli users o polach:
  :id - klucz główny
  :username - nazwa użytkownika 
  :salt - sól
  :hash - hash
"""
conn = sqlite3.connect('cwiczenie3.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    hash TEXT NOT NULL
)
''')

"""
  Funkcja operująca zapisanie konta do bazy wraz z hashowaniem hasła + sól.
  Parametry:
    :param username - nazwa użytkownika
    :param password1 - hasło podane po raz pierwszy w rejestracji
    :param password2 - ponowne podanie hasła
  Zwraca:
    string
"""

def create_account(username, password1, password2) -> str:
    if password1 != password2:
        return "Wprowadzone hasła nie są identyczne."

    salt = os.urandom(16).hex()

    hash = hashlib.sha256((password1 + salt).encode()).hexdigest()

    try:
        cursor.execute('INSERT INTO users (username, salt, hash) VALUES (?, ?, ?)', (username, salt, hash))
        conn.commit()
        return "Konto zostało utworzone."
    except sqlite3.IntegrityError:
        return "Nazwa użytkownika jest już zajęta."

"""
  Funkcja weryfikująca hasło (jego hasz + sól).
  Parametry:
    :username - nazwa użytkownika
    :password - hasło użytkownika
  Zwraca:
    string
"""
def verify_password(username, password) -> str:
    cursor.execute('SELECT salt, hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        salt, correct_hash = result
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()

        if test_hash == correct_hash:
            return "Hasło poprawne."
        else:
            return "Niepoprawne hasło."
    else:
        return "Użytkownik nie istnieje."

"""
  Przykład użycia
"""
print(create_account('aaa', 'haslo123', 'haslo123'))
print(verify_password('aaa', 'haslo123'))