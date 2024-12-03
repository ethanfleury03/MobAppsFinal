import sqlite3
import bcrypt

# Initialize SQLite database
def initialize_database():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # Create users table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a new user
def add_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert into users table
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User added successfully.")
        return True
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
        return False
    finally:
        conn.close()

# Check login credentials
def check_login(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        # Retrieve the stored password for the username
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cur.fetchone()

        if result:
            stored_password = result[0]
            # Compare the provided password with the stored hashed password
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                print("Login successful.")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("User not found.")
            return False
    finally:
        conn.close()
