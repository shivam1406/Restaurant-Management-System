from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.db import get_db_connection
from utils.auth import login_required
from werkzeug.security import check_password_hash

menu_bp = Blueprint('menu', __name__)

@menu_bp.route("/menu")
@login_required
def menu_management():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items ORDER BY category, name ASC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("menu.html", menu_items=items)

@menu_bp.route("/menu/add", methods=["POST"])
@login_required
def add_menu_item():
    data = request.json
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    price = data.get("price", 0.0)
    description = data.get("description", "").strip()
    is_available = bool(data.get("is_available", True))
    if not name or price <= 0:
        return jsonify({"status": "error", "message": "Invalid name or price"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu_items (name, category, price, description, is_available) VALUES (%s, %s, %s, %s, %s)",
                   (name, category, price, description, is_available))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Menu item added"})

@menu_bp.route("/menu/edit/<int:item_id>", methods=["POST"])
@login_required
def edit_menu_item(item_id):
    data = request.json
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    price = data.get("price", 0.0)
    description = data.get("description", "").strip()
    is_available = bool(data.get("is_available", True))
    if not name or price <= 0:
        return jsonify({"status": "error", "message": "Invalid name or price"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE menu_items SET name=%s, category=%s, price=%s, description=%s, is_available=%s WHERE id=%s
        """,
        (name, category, price, description, is_available, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Menu item updated"})

@menu_bp.route("/menu/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_menu_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Menu item deleted"})