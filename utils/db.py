# utils/db.py

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import MYSQL_CONFIG

def get_db_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('admin','staff','manager') DEFAULT 'staff',
        avatar VARCHAR(255) DEFAULT '',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME DEFAULT NULL
    ) ENGINE=INNODB;
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        capacity INT NOT NULL,
        status ENUM('available','occupied','reserved') DEFAULT 'available',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=INNODB;
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(100),
        price DECIMAL(10,2) NOT NULL,
        description TEXT,
        is_available BOOLEAN DEFAULT TRUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=INNODB;
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
       id INT AUTO_INCREMENT PRIMARY KEY,
       table_id INT NOT NULL,
       user_id INT NULL,  -- Change this line to allow NULL values
       status ENUM('pending','preparing','served','paid','cancelled') DEFAULT 'pending',
       total DECIMAL(10,2) DEFAULT 0,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       FOREIGN KEY (table_id) REFERENCES tables(id) ON DELETE CASCADE,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    ) ENGINE=INNODB;
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        menu_item_id INT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        price DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    ) ENGINE=INNODB;
    """)
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Dummy Data Loader
def seed_dummy_data():
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor(buffered=True)

    # Create admin user if none exists
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]
    if count == 0:
        password_hash = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (email, name, password_hash, role) VALUES (%s, %s, %s, %s)", 
                       ("admin@restaurant.com", "Administrator", password_hash, "admin"))

    # Populate tables if none exist
    cursor.execute("SELECT COUNT(*) FROM tables;")
    count = cursor.fetchone()[0]
    if count == 0:
        tables = [
            ("Table 1", 4),
            ("Table 2", 2),
            ("Table 3", 6),
            ("Table 4", 4),
            ("Table 5", 8),
        ]
        cursor.executemany("INSERT INTO tables (name, capacity) VALUES (%s, %s)", tables)

    # Populate menu items if none exist
    cursor.execute("SELECT COUNT(*) FROM menu_items;")
    count = cursor.fetchone()[0]
    if count == 0:
        items = [
            ("Margherita Pizza", "Pizza", 8.99, "Classic pizza with tomato sauce, mozzarella, and basil.", True),
            ("Pepperoni Pizza", "Pizza", 9.99, "Pepperoni with tomato sauce and mozzarella.", True),
            ("Caesar Salad", "Salad", 7.49, "Romaine lettuce with Caesar dressing and croutons.", True),
            ("Grilled Chicken", "Main Course", 12.99, "Grilled chicken breast with herbs and spices.", True),
            ("Spaghetti Bolognese", "Pasta", 10.99, "Spaghetti with rich meat sauce.", True),
        ]
        cursor.executemany("INSERT INTO menu_items (name, category, price, description, is_available) VALUES (%s, %s, %s, %s, %s)", items)

    conn.commit()
    cursor.close()
    conn.close()
    return True