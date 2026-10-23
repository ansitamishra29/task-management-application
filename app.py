import os
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Home / Dashboard
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# Test MySQL connection
@app.route("/test-db")
def test_db():
    connection = get_db_connection()
    connection.close()
    return "MySQL connected successfully!"


# Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or len(password) < 8:
            return (
                "Please enter valid details and a password "
                "of at least 8 characters.",
                400
            )

        password_hash = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """,
                (username, email, password_hash)
            )
            connection.commit()

        except mysql.connector.IntegrityError:
            connection.rollback()
            return (
                "This email is already registered. "
                "Please log in or use another email.",
                409
            )

        finally:
            cursor.close()
            connection.close()

        return redirect("/login")

    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT id, password_hash FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        if (
            user
            and "$" in user[1]
            and check_password_hash(user[1], password)
        ):
            session.clear()
            session["user_id"] = user[0]
            return redirect("/")

        return "Invalid email or password. Please try again.", 401

    return render_template("login.html")


# Get Tasks
@app.route("/get-tasks")
def get_tasks():
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, title, status
            FROM tasks
            WHERE user_id = %s
            """,
            (session["user_id"],)
        )
        tasks = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return jsonify(tasks)


# Add Task
@app.route("/add-task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tasks (user_id, title)
            VALUES (%s, %s)
            """,
            (session["user_id"], title)
        )
        connection.commit()
        task_id = cursor.lastrowid

    finally:
        cursor.close()
        connection.close()

    return jsonify({
        "id": task_id,
        "title": title,
        "status": "pending"
    }), 201


# Update Task
@app.route("/update-task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in ["pending", "completed"]:
        return jsonify({"error": "Invalid task status"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE tasks
            SET status = %s
            WHERE id = %s AND user_id = %s
            """,
            (status, task_id, session["user_id"])
        )
        connection.commit()
        updated = cursor.rowcount

    finally:
        cursor.close()
        connection.close()

    if updated == 0:
        return jsonify({
            "error": "Task not found or status unchanged"
        }), 404

    return jsonify({
        "message": "Task status updated",
        "status": status
    })


# Delete Task
@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s AND user_id = %s
            """,
            (task_id, session["user_id"])
        )
        connection.commit()
        deleted = cursor.rowcount

    finally:
        cursor.close()
        connection.close()

    if deleted == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
