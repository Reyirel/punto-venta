import tkinter as tk
from tkinter import messagebox
import sqlite3
from models.database import connect

def login():
    def verify_login():
        username = entry_user.get()
        password = entry_pass.get()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute('SELECT role FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()

        if result:
            role = result[0]
            window.destroy()
            if role == 'admin':
                import admin_panel
                admin_panel.show()
            elif role == 'vendedor':
                import vendedor_panel
                vendedor_panel.show()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        conn.close()

    window = tk.Tk()
    window.title("Login - Punto de Venta")

    tk.Label(window, text="Usuario").grid(row=0, column=0)
    entry_user = tk.Entry(window)
    entry_user.grid(row=0, column=1)

    tk.Label(window, text="Contraseña").grid(row=1, column=0)
    entry_pass = tk.Entry(window, show="*")
    entry_pass.grid(row=1, column=1)

    login_btn = tk.Button(window, text="Iniciar sesión", command=verify_login)
    login_btn.grid(row=2, column=0, columnspan=2)

    window.mainloop()
