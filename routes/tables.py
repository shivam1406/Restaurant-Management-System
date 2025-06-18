from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.db import get_db_connection
from utils.auth import login_required
from werkzeug.security import check_password_hash

tables_bp = Blueprint('tables', __name__)

@tables_bp.route("/tables")
@login_required
def tables_management():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tables ORDER BY name ASC")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("tables.html", tables=tables)

@tables_bp.route("/tables/add", methods=["POST"])
@login_required
def add_table():
    data = request.json
    name = data.get("name", "").strip()
    capacity = int(data.get("capacity", 1))
    if not name or capacity <= 0:
        return jsonify({"status": "error", "message": "Invalid name or capacity"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tables (name, capacity) VALUES (%s, %s)", (name, capacity))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Table added"})

@tables_bp.route("/tables/edit/<int:table_id>", methods=["POST"])
@login_required
def edit_table(table_id):
    data = request.json
    name = data.get("name", "").strip()
    capacity = int(data.get("capacity", 1))
    if not name or capacity <= 0:
        return jsonify({"status": "error", "message": "Invalid name or capacity"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tables SET name = %s, capacity = %s WHERE id = %s", (name, capacity, table_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Table updated"})

@tables_bp.route("/tables/delete/<int:table_id>", methods=["POST"])
@login_required
def delete_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tables WHERE id = %s", (table_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Table deleted"})