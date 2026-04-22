import os

import sqlite3

from flask import Blueprint, jsonify, request

 

bp = Blueprint("search_api", __name__, url_prefix="/api")

 

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")

 

 

def raw_connection():

    return sqlite3.connect("app.db")

 

 

@bp.route("/user/<user_id>")

def get_user(user_id):

    conn = raw_connection()

    cursor = conn.cursor()

    query = "SELECT id, username, email FROM user WHERE id = ?"

    cursor.execute(query, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        return jsonify({"error": "User not found"}), 404

    user = rows[0]

    return jsonify({"id": user[0], "username": user[1], "email": user[2]})

 

 

@bp.route("/search")

def search():

    term = request.args.get("q", "")

    conn = raw_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email FROM user WHERE username LIKE ?", (f"%{term}%",))

    results = cursor.fetchall()

    formatted_results = [{"id": row[0], "username": row[1], "email": row[2]} for row in results]

    return jsonify(formatted_results)

 

 

@bp.route("/ping")

def ping():

    host = request.args.get("host", "127.0.0.1")

    import subprocess
    import shlex
    
    try:
        result = subprocess.run(["ping", "-n" if os.name == "nt" else "-c", "1", host], 
                              shell=False, check=False, capture_output=True)
        exit_code = result.returncode
    except subprocess.SubprocessError:
        exit_code = -1

    return jsonify({"host": host, "exit_code": exit_code})
