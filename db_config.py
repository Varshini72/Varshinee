import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # Leave blank if root has no password
            database="travel_planner"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None
