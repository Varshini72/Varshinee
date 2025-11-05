# menu.py
from db_config import connect_db
from create_tables import create_tables

# ------------------------------
# TRAVELER OPERATIONS
# ------------------------------
def add_traveler():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Enter traveler name: ")
    email = input("Enter traveler email: ")
    budget = float(input("Enter total budget: "))
    cursor.execute("INSERT INTO Traveler (name, email, total_budget) VALUES (%s, %s, %s)",
                   (name, email, budget))
    conn.commit()
    print("✅ Traveler added successfully!")
    conn.close()

def view_travelers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Traveler")
    travelers = cursor.fetchall()
    print("\n📋 Traveler List:")
    for t in travelers:
        print(f"ID: {t[0]} | Name: {t[1]} | Email: {t[2]} | Budget: ₹{t[3]}")
    conn.close()

# ------------------------------
# DESTINATION OPERATIONS
# ------------------------------
def add_destination():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Enter destination name: ")
    country = input("Enter country: ")
    avg_cost = float(input("Enter average cost to visit: "))
    category = input("Enter category (Beach, City, Mountain, etc.): ")
    cursor.execute("INSERT INTO Destination (name, country, avg_cost, category) VALUES (%s, %s, %s, %s)",
                   (name, country, avg_cost, category))
    conn.commit()
    print("✅ Destination added successfully!")
    conn.close()

def view_destinations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination")
    destinations = cursor.fetchall()
    print("\n🌍 Destination List:")
    for d in destinations:
        print(f"ID: {d[0]} | Name: {d[1]} | Country: {d[2]} | Avg Cost: ₹{d[3]} | Category: {d[4]}")
    conn.close()

# ------------------------------
# TRIP PLAN OPERATIONS
# ------------------------------
def add_trip():
    conn = connect_db()
    cursor = conn.cursor()
    traveler_id = int(input("Enter traveler ID: "))
    dest_id = int(input("Enter destination ID: "))
    days = int(input("Enter number of days: "))
    est_cost = float(input("Enter estimated cost: "))
    cursor.execute("INSERT INTO TripPlan (traveler_id, dest_id, days, est_cost) VALUES (%s, %s, %s, %s)",
                   (traveler_id, dest_id, days, est_cost))
    conn.commit()
    print("✅ Trip plan added successfully!")
    conn.close()

def view_trips():
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT p.plan_id, t.name, d.name, p.days, p.est_cost
        FROM TripPlan p
        JOIN Traveler t ON p.traveler_id = t.traveler_id
        JOIN Destination d ON p.dest_id = d.dest_id
    """
    cursor.execute(query)
    trips = cursor.fetchall()
    print("\n🧳 Trip Plans:")
    for trip in trips:
        print(f"Trip ID: {trip[0]} | Traveler: {trip[1]} | Destination: {trip[2]} | Days: {trip[3]} | Cost: ₹{trip[4]}")
    conn.close()

# ------------------------------
# ANALYTICAL QUERIES
# ------------------------------
def cheapest_destination():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, country, avg_cost FROM Destination ORDER BY avg_cost ASC LIMIT 1")
    result = cursor.fetchone()
    print(f"\n💸 Cheapest Destination: {result[0]} in {result[1]} – ₹{result[2]}")
    conn.close()

def trips_exceeding_budget():
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT t.name, d.name, p.est_cost, t.total_budget
        FROM TripPlan p
        JOIN Traveler t ON p.traveler_id = t.traveler_id
        JOIN Destination d ON p.dest_id = d.dest_id
        WHERE p.est_cost > t.total_budget
    """
    cursor.execute(query)
    trips = cursor.fetchall()
    print("\n⚠️ Trips Exceeding Budget:")
    for trip in trips:
        print(f"Traveler: {trip[0]} | Destination: {trip[1]} | Estimated: ₹{trip[2]} | Budget: ₹{trip[3]}")
    conn.close()
# ------------------------------
# EXPENSE OPERATIONS
# ------------------------------
def add_expense():
    conn = connect_db()
    cursor = conn.cursor()
    plan_id = int(input("Enter Trip Plan ID: "))
    category = input("Enter expense category (Travel, Food, Stay, etc.): ")
    amount = float(input("Enter expense amount: "))

    cursor.execute(
        "INSERT INTO Expense (plan_id, category, amount) VALUES (%s, %s, %s)",
        (plan_id, category, amount)
    )
    conn.commit()
    print("✅ Expense added successfully!")
    conn.close()


def view_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    plan_id = int(input("Enter Trip Plan ID to view expenses: "))

    cursor.execute(
        "SELECT expense_id, category, amount FROM Expense WHERE plan_id = %s",
        (plan_id,)
    )
    expenses = cursor.fetchall()

    print(f"\n💰 Expenses for Trip ID {plan_id}:")
    total = 0
    for e in expenses:
        print(f"ID: {e[0]} | Category: {e[1]} | Amount: ₹{e[2]}")
        total += e[2]

    print(f"Total Spent: ₹{total}")
    conn.close()


import csv

def export_trips_to_csv():
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT p.plan_id, t.name AS traveler_name, d.name AS destination_name,
               p.days, p.est_cost
        FROM TripPlan p
        JOIN Traveler t ON p.traveler_id = t.traveler_id
        JOIN Destination d ON p.dest_id = d.dest_id
    """
    cursor.execute(query)
    trips = cursor.fetchall()

    with open("trip_report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Trip ID", "Traveler Name", "Destination", "Days", "Estimated Cost"])
        writer.writerows(trips)

    print("📁 Trip report exported successfully → trip_report.csv")
    conn.close()


# ------------------------------
# MAIN MENU
# ------------------------------
def main():
    create_tables()

    while True:
        print("\n=== 💰 Budget Travel Planner ===")
        print("1. Add Traveler")
        print("2. View Travelers")
        print("3. Add Destination")
        print("4. View Destinations")
        print("5. Add Trip Plan")
        print("6. View Trips")
        print("7. Show Cheapest Destination")
        print("8. Show Trips Exceeding Budget")
        print("9. Add Expense")
        print("10. View Expenses")
        print("11. Exit")


        choice = input("Enter your choice: ")

        if choice == '1':
            add_traveler()
        elif choice == '2':
            view_travelers()
        elif choice == '3':
            add_destination()
        elif choice == '4':
            view_destinations()
        elif choice == '5':
            add_trip()
        elif choice == '6':
            view_trips()
        elif choice == '7':
            cheapest_destination()
        elif choice == '8':
            trips_exceeding_budget()
        elif choice == '9':
            add_expense()
        elif choice == '10':
            view_expenses()
        
        elif choice == '11':
            print("👋 Goodbye!")
        elif choice == '12':
            export_trips_to_csv()
    
        break 
   
    else:
            print("❌ Invalid choice. Try again!")

if __name__ == "__main__":
    main()
