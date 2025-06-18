from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import get_db_connection
from utils.auth import login_required
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user'] = {"id": user['id'], "email": user['email'], "name": user['name'], "role": user['role'], "avatar": user['avatar']}
            # Update last_login
            cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid credentials", "error")
        cursor.close()
        conn.close()
    return render_template("login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))