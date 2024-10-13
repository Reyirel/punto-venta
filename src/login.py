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

    # Establecer el tamaño de la ventana
    window.geometry("1000x500")

    # Centrar la ventana en la pantalla
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Crear un frame para centrar los widgets de login
    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(frame, text="Usuario").grid(row=0, column=0, pady=5)
    entry_user = tk.Entry(frame)
    entry_user.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Contraseña").grid(row=1, column=0, pady=5)
    entry_pass = tk.Entry(frame, show="*")
    entry_pass.grid(row=1, column=1, pady=5)

    login_btn = tk.Button(frame, text="Iniciar sesión", command=verify_login)
    login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    window.mainloop()