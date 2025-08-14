# Create a simple script to check your data
# File: check_data.py

from database import FinanceDB

db = FinanceDB()
conn = db.get_connection()
cursor = conn.cursor()

# Check users
cursor.execute("SELECT id, username, email, created_at FROM users")
users = cursor.fetchall()

print("=== USERS ===")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")

conn.close()