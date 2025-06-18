from config import MYSQL_CONFIG
from utils.db import get_db_connection, init_db, seed_dummy_data
from routes import auth_bp, dashboard_bp, menu_bp, tables_bp, orders_bp, public_bp, init_bp
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, flash, abort
from flask_session import Session
from functools import wraps
import os
import json
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(tables_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(public_bp)
app.register_blueprint(init_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.context_processor
def inject_user():
    return dict(current_user=session.get('user'))