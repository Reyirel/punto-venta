import sqlite3

def connect():
    return sqlite3.connect('src/data/punto_venta.db')

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Tabla de usuarios (ya existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Tabla de productos (ya existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Nueva tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total REAL NOT NULL
        )
    ''')

    # Nueva tabla de detalles de venta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_default_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES 
        ('admin', 'admin123', 'admin'),
        ('vendedor', 'vendedor123', 'vendedor')
    ''')

    conn.commit()
    conn.close()

# Llamamos a la creación de tablas y usuarios predeterminados
create_tables()
add_default_users()