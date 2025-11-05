from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash
from db_config import connect_db
import mysql.connector, math

app = Flask(__name__)

@app.route("/explore")
def explore():
    return render_template("explore.html")

# --- keep your existing API routes here ---
# e.g.
@app.route("/api/signup", methods=["POST"])
def signup():
    # your code...
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(debug=True)

# ---------- Helpers ----------
def row_to_destination(row):
    avg = float(row[3] or 0)
    min_cost = max(1000, math.floor(avg * 0.7))
    max_cost = max(min_cost + 1, math.floor(avg * 1.3))
    return {
        "id": row[0],
        "name": row[1],
        "country": row[2],
        "avg_cost": avg,
        "category": row[4],
        "min": min_cost,
        "max": max_cost,
        "info": f"{row[4]} • Typical ₹{min_cost:,}–₹{max_cost:,}"
    }

# ---------- Serve Frontend ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- API: Signup ----------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    if not name or not email:
        return jsonify({"ok": False, "error": "name and email required"}), 400

    conn = connect_db()
    cur = conn.cursor()
    password_hash = generate_password_hash(password) if password else None

    try:
        if password_hash:
            cur.execute("""
                INSERT INTO Traveler (name, email, total_budget, password_hash)
                VALUES (%s,%s,%s,%s)
            """, (name, email, 0, password_hash))
        else:
            cur.execute("""
                INSERT INTO Traveler (name, email, total_budget)
                VALUES (%s,%s,%s)
            """, (name, email, 0))
        conn.commit()
        traveler_id = cur.lastrowid
        return jsonify({"ok": True, "traveler_id": traveler_id})
    except mysql.connector.Error as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# ---------- API: Destinations ----------
@app.route("/api/destinations", methods=["GET"])
def api_destinations():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT dest_id, name, country, avg_cost, category FROM Destination")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row_to_destination(r) for r in rows])

# ---------- API: Recommendations ----------
@app.route("/api/recommendations", methods=["GET"])
def api_recommendations():
    try:
        budget = int(request.args.get("budget", "0"))
    except:
        return jsonify({"ok": False, "error": "invalid budget"}), 400

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT dest_id, name, country, avg_cost, category FROM Destination")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    dests = [row_to_destination(r) for r in rows]
    matched = [d for d in dests if d["min"] <= budget <= d["max"]]
    return jsonify({"ok": True, "budget": budget, "results": matched})

# ---------- API: Book Trip ----------
@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.get_json(force=True)
    traveler_name = (data.get("name") or "").strip()
    traveler_email = (data.get("email") or "").strip()
    destination = (data.get("destination") or "").strip()
    days = int(data.get("days") or 0)
    est_cost = float(data.get("est_cost") or 0)

    if not traveler_name or not destination or not days or not est_cost:
        return jsonify({"ok": False, "error": "missing fields"}), 400

    conn = connect_db()
    cur = conn.cursor()

    # ensure traveler exists
    traveler_id = None
    if traveler_email:
        cur.execute("SELECT traveler_id FROM Traveler WHERE email=%s", (traveler_email,))
        row = cur.fetchone()
        if row: traveler_id = row[0]

    if traveler_id is None:
        cur.execute("INSERT INTO Traveler (name,email,total_budget) VALUES (%s,%s,%s)",
                    (traveler_name, traveler_email, 0))
        conn.commit()
        traveler_id = cur.lastrowid

    # destination id
    cur.execute("SELECT dest_id FROM Destination WHERE name=%s", (destination,))
    drow = cur.fetchone()
    if not drow:
        return jsonify({"ok": False, "error": "destination not found"}), 400
    dest_id = drow[0]

    cur.execute("INSERT INTO TripPlan (traveler_id,dest_id,days,est_cost) VALUES (%s,%s,%s,%s)",
                (traveler_id, dest_id, days, est_cost))
    conn.commit()
    plan_id = cur.lastrowid

    cur.execute("INSERT INTO Expense (plan_id,category,amount) VALUES (%s,%s,%s)",
                (plan_id, "Advance", 1000))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"ok": True, "plan_id": plan_id})

if __name__ == "__main__":
    app.run(debug=True)
