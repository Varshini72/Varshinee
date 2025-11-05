import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # or your actual password
        database="travel_planner"
    )
    if conn.is_connected():
        print("✅ Connected successfully to MySQL!")
except mysql.connector.Error as e:
    print(f"❌ Error: {e}")
