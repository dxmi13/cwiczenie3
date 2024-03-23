import sqlite3
import hashlib
import os
from hmac import compare_digest

"""
    Tworzy połączenie z bazą danych SQLite.
    :param path: ścieżka do pliku bazy danych.
"""
def connect_db(path='users.db'):
    
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        salt TEXT NOT NULL,
        hash TEXT NOT NULL
    )
    ''')
    return conn, cursor

"""
    Tworzy konto użytkownika z bezpiecznie zahashowanym hasłem.
    :param cursor: Kursor bazy danych.
    :param username: Nazwa użytkownika.
    :param password: Hasło użytkownika.
    Zwraca:
      string
"""
def create_account(cursor, username, password) -> str:
    
    salt = os.urandom(16)
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    try:
        cursor.execute('INSERT INTO users (username, salt, hash) VALUES (?, ?, ?)', 
                       (username, salt.hex(), hash.hex()))
        cursor.connection.commit()
        return "Konto zostało utworzone."
    except sqlite3.IntegrityError:
        return "Nazwa użytkownika jest już zajęta."

"""
    Weryfikuje hasło użytkownika.
    :param cursor: Kursor bazy danych.
    :param username: Nazwa użytkownika.
    :param password: Hasło do weryfikacji.
    Zwraca:
      True, jeśli hasło jest poprawne, w przeciwnym razie False.
    """
def verify_password(cursor, username, password) -> bool:
    
    cursor.execute('SELECT salt, hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        salt, correct_hash = bytes.fromhex(result[0]), bytes.fromhex(result[1])
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

        return compare_digest(test_hash, correct_hash)

    return False

"""
  Przykład użycia tworzenia konta i haszów.
"""

conn, cursor = connect_db()
print(create_account(cursor, 'aaa', 'haslo123'))
print(verify_password(cursor, 'aaa', 'haslo12'))

conn.close()

