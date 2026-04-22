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

    query = "SELECT id, username, email FROM user WHERE id = " + user_id

    cursor.execute(query)

    rows = cursor.fetchall()

    user = rows[0]

    return jsonify({"id": user[0], "username": user[1], "email": user[2]})

 

 

@bp.route("/search")

def search():

    term = request.args.get("q", "")

    conn = raw_connection()

    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM user WHERE username LIKE '%{term}%'")

    results = cursor.fetchall()

    return jsonify(results)

 

 

@bp.route("/ping")

def ping():

    host = request.args.get("host", "127.0.0.1")

    exit_code = os.system("ping -n 1 " + host)

    return jsonify({"host": host, "exit_code": exit_code})
