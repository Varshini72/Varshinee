# create_tables.py
from db_config import connect_db

def create_tables():
    conn = connect_db()
    if conn is None:
        print("❌ Unable to connect to database.")
        return
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Traveler (
            traveler_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            email VARCHAR(50) UNIQUE,
            total_budget DECIMAL(10,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Destination (
            dest_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            country VARCHAR(50),
            avg_cost DECIMAL(10,2),
            category VARCHAR(30)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TripPlan (
            plan_id INT PRIMARY KEY AUTO_INCREMENT,
            traveler_id INT,
            dest_id INT,
            days INT,
            est_cost DECIMAL(10,2),
            FOREIGN KEY (traveler_id) REFERENCES Traveler(traveler_id),
            FOREIGN KEY (dest_id) REFERENCES Destination(dest_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expense (
            expense_id INT PRIMARY KEY AUTO_INCREMENT,
            plan_id INT,
            category VARCHAR(30),
            amount DECIMAL(10,2),
            FOREIGN KEY (plan_id) REFERENCES TripPlan(plan_id)
        )
    """)

    conn.commit()
    print("✅ All tables created successfully!")
    conn.close()
