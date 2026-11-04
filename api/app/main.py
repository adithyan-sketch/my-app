from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM students")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id": s[0], "name": s[1]}
        for s in students
    ])

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"message": "Name is required"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name) VALUES (%s)",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student added successfully!"})

@app.route("/health")
def health():
    return jsonify({"status": "API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
