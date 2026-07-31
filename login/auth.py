import hashlib
import sqlite3
import re


DB_NAME = "users.db"


def hash_password(password: str) -> str:
    """Convert password to SHA256 hash"""
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


def signup(username: str, email: str, password: str):

    if not username.strip():
        return False, "Username is required."

    if not is_valid_email(email):
        return False, "Invalid email."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    if cursor.fetchone():
        conn.close()
        return False, "Email already registered."

    password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username, email, password_hash)
    )

    conn.commit()
    conn.close()

    return True, "Account created successfully."


def login(email: str, password: str):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE email=? AND password=?
        """,
        (email, password_hash)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return True, {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }

    return False, "Invalid email or password."

# -------------------------------
# FAVORITES
# -------------------------------

def add_favorite(user_email, movie_id, movie_title, poster_path):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM favorites
        WHERE user_email=? AND movie_id=?
    """, (user_email, movie_id))

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO favorites
        (user_email, movie_id, movie_title, poster_path)
        VALUES (?, ?, ?, ?)
    """, (
        user_email,
        movie_id,
        movie_title,
        poster_path
    ))

    conn.commit()
    conn.close()

    return True


def get_favorites(user_email):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT movie_id, movie_title, poster_path
        FROM favorites
        WHERE user_email=?
    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return data


def remove_favorite(user_email, movie_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorites
        WHERE user_email=? AND movie_id=?
    """, (
        user_email,
        movie_id
    ))

    conn.commit()
    conn.close()

def get_user(email):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, email, created_at
        FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user