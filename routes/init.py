from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import get_db_connection, init_db, seed_dummy_data
from werkzeug.security import check_password_hash

init_bp = Blueprint('init', __name__)

@init_bp.route("/init")
def initialize():
    """Initialize the database and seed dummy data"""
    success_db = init_db()
    success_seed = False
    if success_db:
        success_seed = seed_dummy_data()
    if success_db and success_seed:
        return "Database initialized and dummy data seeded."
    return "Failed to initialize database.", 500