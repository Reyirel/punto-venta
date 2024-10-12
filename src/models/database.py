import sqlite3

def connect():
    # Conectamos a la base de datos o la creamos si no existe
    conn = sqlite3.connect('src/data/punto_venta.db')
    return conn

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_default_users():
    conn = connect()
    cursor = conn.cursor()

    # Usuarios predeterminados (admin y vendedor)
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
