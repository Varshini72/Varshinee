from flask import Flask, render_template, request, redirect
from db_config import connect_db

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# -------------------------
# TRAVELER ROUTES
# -------------------------
@app.route('/add_traveler', methods=['GET', 'POST'])
def add_traveler():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        budget = request.form['budget']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Traveler (name, email, total_budget) VALUES (%s, %s, %s)",
                       (name, email, budget))
        conn.commit()
        conn.close()
        return redirect('/view_travelers')

    return render_template('add_traveler.html')

@app.route('/view_travelers')
def view_travelers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Traveler")
    travelers = cursor.fetchall()
    conn.close()
    return render_template('view_travelers.html', travelers=travelers)

# -------------------------
# DESTINATION ROUTES
# -------------------------
@app.route('/add_destination', methods=['GET', 'POST'])
def add_destination():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        avg_cost = request.form['avg_cost']
        category = request.form['category']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Destination (name, country, avg_cost, category) VALUES (%s, %s, %s, %s)",
            (name, country, avg_cost, category)
        )
        conn.commit()
        conn.close()
        return redirect('/view_destinations')

    return render_template('add_destination.html')

@app.route('/view_destinations')
def view_destinations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination")
    destinations = cursor.fetchall()
    conn.close()
    return render_template('view_destinations.html', destinations=destinations)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
