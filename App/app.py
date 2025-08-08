from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)
DB_CONN = DB_CONN = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DB_CONN)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="POST":
        message = request.form["message"]
        date = datetime.now().date()
        time = datetime.now().strftime("%H:%M")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (message, date, time) VALUES (%s, %s, %s)", (message, date, time)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    # For GET, fetch last 20 messages
    
    if request.method == "GET":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT message, date, time FROM messages ORDER BY id DESC LIMIT 20"
        )
        messages = cur.fetchall()
        cur.close()
        conn.close()

    return render_template("index.html", messages=messages)

@app.route("/api/messages", methods=["GET"])
def get_api_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, message, date, time FROM messages ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = []
    for row in rows:
        messages.append({
            "id": row[0],
            "message": row[1],
            "date": row[2].isoformat(),
            "time": row[3].strftime("%H:%M")
        })
    
    return jsonify(messages)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)