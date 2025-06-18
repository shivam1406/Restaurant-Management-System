from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import get_db_connection
from utils.auth import login_required
from werkzeug.security import check_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
def dashboard():
    # Fetch counts for dashboard stats
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM menu_items;")
    menu_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tables;")
    tables_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders;")
    orders_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return render_template("dashboard.html", menu_count=menu_count, tables_count=tables_count, orders_count=orders_count)
