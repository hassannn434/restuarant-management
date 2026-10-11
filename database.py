import sqlite3
import hashlib

DB_NAME = "restaurant.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Menu Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_no TEXT NOT NULL,
            items_summary TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL,
            order_time TEXT NOT NULL,
            served_by TEXT
        )
    """)

    # Migration check: add served_by if missing in older database files
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN served_by TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Seed default users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("admin", hash_password("admin123"), "Admin"),
            ("waiter1", hash_password("waiter123"), "Staff")
        ]
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", default_users)
        conn.commit()

    # Seed default menu
    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] == 0:
        default_menu = [
            ("Margherita Pizza", "Main Course", 12.50, 50),
            ("Classic Cheeseburger", "Main Course", 9.00, 40),
            ("Caesar Salad", "Appetizer", 7.50, 30),
            ("Garlic Bread", "Appetizer", 5.00, 60),
            ("Chocolate Lava Cake", "Dessert", 6.50, 25),
            ("Iced Lemon Tea", "Beverages", 3.50, 100)
        ]
        cursor.executemany("INSERT INTO menu (name, category, price, stock) VALUES (?, ?, ?, ?)", default_menu)
        conn.commit()
    
    conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    cursor.execute("SELECT username, role FROM users WHERE username = ? AND password = ?", (username, hashed_pwd))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pwd = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pwd, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def fetch_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, name, category, price, stock FROM menu")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_menu_item(name, category, price, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, category, price, stock) VALUES (?, ?, ?, ?)", (name, category, price, stock))
    conn.commit()
    conn.close()

def save_order(table_no, items_summary, total, status, order_time, served_by):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (table_no, items_summary, total, status, order_time, served_by) VALUES (?, ?, ?, ?, ?, ?)", 
                   (table_no, items_summary, total, status, order_time, served_by))
    conn.commit()
    conn.close()

def fetch_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, table_no, items_summary, total, status, order_time, served_by FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
    conn.commit()
    conn.close()