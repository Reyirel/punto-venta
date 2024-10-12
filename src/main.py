from login import login
from models.database import create_tables

def main():
    create_tables()  # Crear tablas si no existen
    login()

if __name__ == '__main__':
    main()
