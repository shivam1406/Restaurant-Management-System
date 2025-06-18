from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.db import get_db_connection
from werkzeug.security import check_password_hash

public_bp = Blueprint('public', __name__)

@public_bp.route('/public/order', methods=['GET', 'POST'], endpoint='public_order_endpoint')
def public_order():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch tables and available menu items for the form
    cursor.execute("SELECT * FROM tables ORDER BY name")
    tables = cursor.fetchall()
    cursor.execute("SELECT * FROM menu_items WHERE is_available = TRUE ORDER BY name")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        data = request.get_json()
        table_id = data.get("table_id")
        items = data.get("items", [])

        # Basic validation
        if not table_id or not items or not isinstance(items, list):
            return jsonify({"status": "error", "message": "Invalid order data"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        total = 0
        for item in items:
            if "menu_item_id" not in item or "quantity" not in item:
                continue
            cursor.execute("SELECT price FROM menu_items WHERE id = %s AND is_available = TRUE", (item["menu_item_id"],))
            row = cursor.fetchone()
            if row:
                price = row[0]
                total += price * item["quantity"]

        try:
            # Insert order with user_id as NULL to indicate guest
            cursor.execute(
                "INSERT INTO orders (table_id, user_id, total, status) VALUES (%s, NULL, %s, %s)",
                (table_id, total, "pending"),
            )
            order_id = cursor.lastrowid

            for item in items:
                menu_item_id = item["menu_item_id"]
                quantity = item["quantity"]
                cursor.execute("SELECT price FROM menu_items WHERE id = %s", (menu_item_id,))
                row = cursor.fetchone()
                if not row:
                    continue
                price = row[0]
                cursor.execute(
                    "INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, menu_item_id, quantity, price),
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": f"Failed to add order: {str(e)}"}), 500

        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Order placed successfully", "order_id": order_id})

    # For GET request render the public order form
    return render_template("public_order.html", tables=tables, menu_items=menu_items)