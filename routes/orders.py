from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.db import get_db_connection
from utils.auth import login_required
from werkzeug.security import check_password_hash

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/orders")
@login_required
def orders_management():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT o.id, o.status, o.total, o.created_at, o.updated_at,
                      t.name AS table_name,
                      COALESCE(u.name, 'Guest') AS user_name
                      FROM orders o
                      LEFT JOIN tables t ON o.table_id = t.id
                      LEFT JOIN users u ON o.user_id = u.id
                      ORDER BY o.created_at DESC""")
    orders = cursor.fetchall() 

    for order in orders:
        order["created_at_str"] = order["created_at"].strftime('%Y-%m-%d %H:%M')
        print(f"[DEBUG] Shown: {order['created_at_str']} | Raw: {order['created_at']}")

    # For order items, will fetch on demand in detail view if added
    cursor.execute("SELECT * FROM tables ORDER BY name;")
    tables = cursor.fetchall()
    cursor.execute("SELECT * FROM menu_items WHERE is_available = TRUE ORDER BY name;")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("orders.html", orders=orders, tables=tables, menu_items=menu_items)

@orders_bp.route("/orders/add", methods=["POST"])
@login_required
def add_order():
    data = request.json
    table_id = data.get("table_id")
    user_id = session.get("user_id")
    items = data.get("items", [])  # List of dicts {menu_item_id, quantity}
    if not table_id or not items or not isinstance(items, list):
        return jsonify({"status": "error", "message": "Invalid order data"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Calculate total price
    total = 0
    for item in items:
        if "menu_item_id" not in item or "quantity" not in item:
            continue
        cursor.execute("SELECT price FROM menu_items WHERE id = %s AND is_available = TRUE", (item["menu_item_id"],))
        row = cursor.fetchone()
        if row:
            price = row[0]
            total += price * item["quantity"]
        else:
            # Ignore unavailable items
            pass
    try:
        cursor.execute(
            "INSERT INTO orders (table_id, user_id, total, status) VALUES (%s, %s, %s, %s)",
            (table_id, user_id, total, "Pending"),
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
    return jsonify({"status": "success", "message": "Order added", "order_id": order_id})

@orders_bp.route("/orders/delete/<int:order_id>", methods=["POST"])
@login_required
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Order deleted"})

@orders_bp.route('/orders/<int:order_id>/items')
@login_required
def order_items(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT oi.quantity, oi.price, mi.name FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

@orders_bp.route('/orders/list')
@login_required
def orders_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, o.status, o.total, o.created_at,
               t.name AS table_name,
               COALESCE(u.name, 'Guest') AS user_name
        FROM orders o
        LEFT JOIN tables t ON o.table_id = t.id
        LEFT JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    for order in orders:
        order["created_at_str"] = order["created_at"].strftime('%Y-%m-%d %H:%M')
    return jsonify(orders)

@orders_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@login_required
def update_order_status(order_id):
    new_status = request.json.get("status")
    allowed = ['pending', 'preparing', 'served', 'paid', 'cancelled']
    if new_status not in allowed:
        return jsonify({"status": "error", "message": "Invalid status."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
        conn.commit()
        return jsonify({"status": "success", "message": f"Order updated to '{new_status}'."})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()
