from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "poc_user"),
    "password": os.getenv("DB_PASS", "poc_password"),
    "database": os.getenv("DB_NAME", "poc_db"),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (content) VALUES (%s)", (content,))
    conn.commit()
    entry_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"success": True, "id": entry_id})

@app.route("/entries/json")
def entries_json():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, content, created_at FROM entries ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        row["created_at"] = row["created_at"].isoformat()
    return jsonify(rows)

@app.route("/clear", methods=["POST"])
def clear_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries")
    deleted = cursor.rowcount
    cursor.execute("ALTER TABLE entries AUTO_INCREMENT = 1")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "deleted": deleted})

@app.route("/entries/html")
def entries_html():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, content, created_at FROM entries ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("entries.html", entries=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
