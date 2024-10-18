import tkinter as tk
from tkinter import ttk, messagebox
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
                admin_panel.show(username)
            elif role == 'vendedor':
                import vendedor_panel
                vendedor_panel.show(username)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        conn.close()

    # Configuración de la ventana principal
    window = tk.Tk()
    window.title("Sistema de Punto de Venta")
    window.configure(bg='#2d3436')  # Nuevo color de fondo oscuro

    # Configurar el tamaño y centrar la ventana
    window_width = 1000
    window_height = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    window.resizable(False, False)

    # Frame principal con efecto de tarjeta
    main_frame = tk.Frame(window, bg='white', relief='solid', bd=1)
    main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=450)

    # Título de la aplicación con nuevo color
    title_label = tk.Label(
        main_frame,
        text="Bienvenido",
        font=('Helvetica', 24, 'bold'),
        bg='white',
        fg='#00b894'  # Nuevo color del título
    )
    title_label.pack(pady=(40, 10))

    # Subtítulo
    subtitle_label = tk.Label(
        main_frame,
        text="Inicie sesión para continuar",
        font=('Helvetica', 12),
        bg='white',
        fg='#7f8c8d'
    )
    subtitle_label.pack(pady=(0, 30))

    # Frame para el formulario
    form_frame = tk.Frame(main_frame, bg='white')
    form_frame.pack(pady=20, padx=40)

    # Estilo para los entry
    style = ttk.Style()
    style.configure(
        'Custom.TEntry',
        fieldbackground='#f8f9fa',
        borderwidth=0
    )

    # Usuario
    username_frame = tk.Frame(form_frame, bg='white')
    username_frame.pack(fill='x', pady=(0, 15))
    
    username_label = tk.Label(
        username_frame,
        text="Usuario",
        font=('Helvetica', 10),
        bg='white',
        fg='#2c3e50'
    )
    username_label.pack(anchor='w')
    
    entry_user = ttk.Entry(
        username_frame,
        style='Custom.TEntry',
        width=35
    )
    entry_user.pack(fill='x', pady=(5, 0), ipady=8)

    # Contraseña
    password_frame = tk.Frame(form_frame, bg='white')
    password_frame.pack(fill='x', pady=(0, 25))
    
    password_label = tk.Label(
        password_frame,
        text="Contraseña",
        font=('Helvetica', 10),
        bg='white',
        fg='#2c3e50'
    )
    password_label.pack(anchor='w')
    
    entry_pass = ttk.Entry(
        password_frame,
        style='Custom.TEntry',
        width=35,
        show="●"
    )
    entry_pass.pack(fill='x', pady=(5, 0), ipady=8)

    # Botón de login con nuevo color
    login_btn = tk.Button(
        form_frame,
        text="Iniciar Sesión",
        font=('Helvetica', 11, 'bold'),
        bg='#009bc5',  # Nuevo color del botón
        fg='white',
        relief='flat',
        command=verify_login,
        cursor='hand2',
        width=20,
        height=2
    )
    login_btn.pack(pady=20)

    # Hover effect para el botón
    def on_enter(e):
        login_btn['bg'] = '#00b4e4'  # Un tono más claro del color del botón para hover

    def on_leave(e):
        login_btn['bg'] = '#009bc5'  # Volver al color original

    login_btn.bind('<Enter>', on_enter)
    login_btn.bind('<Leave>', on_leave)

    # Footer
    footer_label = tk.Label(
        main_frame,
        text="© 2024 Sistema de Punto de Venta",
        font=('Helvetica', 8),
        bg='white',
        fg='#95a5a6'
    )
    footer_label.pack(side='bottom', pady=20)

    # Bind Enter key to verify_login
    window.bind('<Return>', lambda event: verify_login())

    window.mainloop()