from login import login
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from models.database import connect
from PIL import Image, ImageTk, ImageDraw

class AdminPanel:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Panel de Administración")
        self.master.state('zoomed')
        self.master.resizable(0, 0)

        # Paleta de colores moderna
        self.colors = {
            'primary': "#2D3436",       # Color principal oscuro para el fondo del menú
            'secondary': "#636E72",     # Color secundario para hover
            'accent': "#00B894",        # Color de acento para el botón activo
            'text': "#FFFFFF",          # Color del texto
            'text_disabled': "#B2BEC3",  # Color del texto desactivado
            'danger': "#e74c3c"         # Color rojo para el botón de cerrar sesión
        }

        # Frame principal con diseño moderno
        self.menu_frame = tk.Frame(
            self.master, 
            bg=self.colors['primary'],
            width=250  # Ancho fijo para el menú
        )
        self.menu_frame.pack_propagate(False)  # Mantener el ancho fijo
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Header del menú con el nombre de usuario
        header_frame = tk.Frame(self.menu_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X, padx=15, pady=(20,10))
        
        # Título "Panel Admin"
        tk.Label(
            header_frame,
            text="Panel Admin",
            font=("Helvetica", 14),
            bg=self.colors['primary'],
            fg=self.colors['text']
        ).pack(anchor="w")

        # Nombre de usuario con estilo
        tk.Label(
            header_frame,
            text=username,
            font=("Helvetica", 12),
            bg=self.colors['primary'],
            fg=self.colors['text_disabled']
        ).pack(anchor="w")

        # Separador
        ttk.Separator(self.menu_frame).pack(fill=tk.X, padx=15, pady=10)

        # Opciones del menú
        menu_options = [
            ("👥 Usuarios", self.show_add_user),
            ("👤 Clientes", self.show_add_client),
            ("📦 Productos", self.show_add_product),
            ("📋 Inventario", self.show_view_products),
            ("📈 Reportes", self.show_reports),
            ("💰 Ventas", self.show_sales)
        ]

        # Frame para los botones del menú
        buttons_frame = tk.Frame(self.menu_frame, bg=self.colors['primary'])
        buttons_frame.pack(fill=tk.X, pady=10)

        self.buttons = []
        self.current_section = None

        for text, command in menu_options:
            # Frame contenedor para cada botón
            btn_container = tk.Frame(buttons_frame, bg=self.colors['primary'])
            btn_container.pack(fill=tk.X, pady=2)

            button = tk.Button(
                btn_container,
                text=text,
                command=lambda cmd=command, btn_text=text: self.change_section(cmd, btn_text),
                bg=self.colors['primary'],
                fg=self.colors['text'],
                font=("Helvetica", 11),
                bd=0,
                relief=tk.FLAT,
                activebackground=self.colors['secondary'],
                activeforeground=self.colors['text'],
                anchor="w",
                padx=25,
                pady=12,
                width=25
            )
            button.pack(fill=tk.X)

            # Eventos para efectos hover
            button.bind("<Enter>", lambda e, b=button: self.on_enter(e, b))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
            self.buttons.append(button)

        # Agregar separador antes del botón de cerrar sesión

        # Botón de cerrar sesión al final del menú
        logout_container = tk.Frame(self.menu_frame, bg=self.colors['primary'])
        logout_container.pack(fill=tk.X, pady=2, side=tk.BOTTOM, padx=15)
        
        self.logout_button = tk.Button(
            logout_container,
            text="🚪 Cerrar Sesión",
            command=self.logout,
            bg=self.colors['danger'],
            fg=self.colors['text'],
            font=("Helvetica", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#c0392b",  # Un rojo más oscuro para el hover
            activeforeground=self.colors['text'],
            anchor="center",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.logout_button.pack(fill=tk.X)

        # Frame principal para el contenido
        self.main_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inicialmente mostramos la primera opción
        self.show_add_user()

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.master.destroy()
            login()
    
    def round_corners(self):
        # Crear una máscara con esquinas redondeadas
        radius = 40  # Radio de las esquinas redondeadas
        width = self.menu_frame.winfo_width()
        height = self.menu_frame.winfo_height()
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, width, height], radius, fill=1)

        # Aplicar la máscara al menú
        self.menu_frame.mask = ImageTk.PhotoImage(mask)
        self.menu_frame.create_image(0, 0, image=self.menu_frame.mask, anchor='nw')

        # Asegurarse de que los widgets hijos estén dentro del área redondeada
        for child in self.menu_frame.winfo_children():
            child.lift()
         
    def on_enter(self, e, button):
        if button.cget('text') != self.current_section:
            button.config(
                bg=self.colors['secondary'],
                cursor="hand2"
            )

    def on_leave(self, e, button):
        if button.cget('text') != self.current_section:
            button.config(
                bg=self.colors['primary'],
                cursor=""
            )

    def change_section(self, command, button_text):
        # Resetear el botón previamente seleccionado
        if self.current_section:
            for btn in self.buttons:
                if btn.cget('text') == self.current_section:
                    btn.config(
                        bg=self.colors['primary'],
                        fg=self.colors['text']
                    )
                    break

        # Actualizar la sección actual
        self.current_section = button_text

        # Resaltar el botón seleccionado
        for btn in self.buttons:
            if btn.cget('text') == button_text:
                btn.config(
                    bg=self.colors['accent'],
                    fg=self.colors['text']
                )
                break

        # Ejecutar el comando
        command()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# ----------------------------------------------------

# agregar usuario---------------------------------------
    def show_add_user(self):
        self.clear_frame()
        self.main_frame.configure(bg="#f0f0f0")  # Fondo del frame principal

        # Main container
        main_container = tk.Frame(self.main_frame, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_container, text="Agregar Usuario", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Left frame for input fields with LabelFrame (to add a border and title)
        input_frame = tk.LabelFrame(main_container, text="Formulario de Usuario", font=("Arial", 12, "bold"), padx=30, pady=30, bg="#f0f0f0")
        input_frame.grid(row=1, column=0, sticky="n", padx=(0, 20))

        # User input fields
        tk.Label(input_frame, text="Nombre de usuario:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.username_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=(0, 10))

        tk.Label(input_frame, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.password_entry = tk.Entry(input_frame, show="*", font=("Arial", 12), width=30)
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        tk.Label(input_frame, text="Rol:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.role_var = tk.StringVar(value="vendedor")
        role_frame = tk.Frame(input_frame, bg="#f0f0f0")
        role_frame.grid(row=2, column=1, sticky="w", pady=(0, 10))
        tk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="admin", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(role_frame, text="Vendedor", variable=self.role_var, value="vendedor", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)

        # Add User button
        add_button = tk.Button(input_frame, text="Agregar Usuario", command=self.add_user, font=("Arial", 12, "bold"), bg="#00B894", fg="white", padx=10, pady=5)
        add_button.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky="ew")

        # Right frame for user table
        table_frame = tk.Frame(main_container, bg="#f0f0f0")
        table_frame.grid(row=1, column=1, sticky="nsew")

        # User table
        self.user_tree = ttk.Treeview(table_frame, columns=("username", "password", "role"), show="headings", height=15)
        self.user_tree.heading("username", text="Nombre de Usuario")
        self.user_tree.heading("password", text="Contraseña")
        self.user_tree.heading("role", text="Rol")
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        # Load users into the table
        self.load_users()

        # Buttons for editing and deleting users
        button_frame = tk.Frame(main_container, bg="#f0f0f0")
        button_frame.grid(row=2, column=1, pady=(20, 0), sticky="e")

        edit_button = tk.Button(button_frame, text="Editar Usuario", command=self.edit_user, font=("Arial", 12), bg="#2196F3", fg="white")
        edit_button.pack(side=tk.LEFT, padx=(0, 10))

        delete_button = tk.Button(button_frame, text="Eliminar Usuario", command=self.delete_user, font=("Arial", 12), bg="#f44336", fg="white")
        delete_button.pack(side=tk.LEFT)

        # Configure grid weights
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

    def load_users(self):
        # Clear existing items
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)

        # Fetch users from the database
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, role FROM users')
        users = cursor.fetchall()
        conn.close()

        # Insert users into the table
        for user in users:
            self.user_tree.insert("", "end", values=user)

    def edit_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para editar")
            return

        user = self.user_tree.item(selected_item)['values']

        # Create a new window for editing the user
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Editar Usuario: {user[0]}")
        edit_window.geometry("400x335")
        edit_window.resizable(False, False)

        # Center the window on the screen
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create a frame to hold the content
        content_frame = tk.Frame(edit_window)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Username entry
        username_label = tk.Label(content_frame, text="Nombre de usuario:", font=("Helvetica", 12))
        username_label.pack(pady=(0, 5))
        username_entry = tk.Entry(content_frame, font=("Helvetica", 12))
        username_entry.insert(0, user[0])
        username_entry.pack(fill="x", pady=(0, 10))

        # Password entry
        password_label = tk.Label(content_frame, text="Contraseña:", font=("Helvetica", 12))
        password_label.pack(pady=(0, 5))
        password_entry = tk.Entry(content_frame, font=("Helvetica", 12), show="*")
        password_entry.insert(0, user[1])
        password_entry.pack(fill="x", pady=(0, 10))

        # Show/hide password checkbox
        def toggle_password():
            if password_entry.cget('show') == '*':
                password_entry.config(show='')
            else:
                password_entry.config(show='*')

        show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(content_frame, text="Mostrar contraseña", variable=show_password_var, command=toggle_password, font=("Helvetica", 10))
        show_password_check.pack(anchor="w", pady=(0, 10))

        # Role radio buttons
        role_label = tk.Label(content_frame, text="Rol:", font=("Helvetica", 12))
        role_label.pack(pady=(0, 5))
        role_var = tk.StringVar(value=user[2])
        role_frame = tk.Frame(content_frame)
        role_frame.pack(anchor="w", pady=(0, 10))
        tk.Radiobutton(role_frame, text="Administrador", variable=role_var, value="admin", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(role_frame, text="Vendedor", variable=role_var, value="vendedor", font=("Helvetica", 10)).pack(side=tk.LEFT)

        # Save changes button
        def save_changes():
            new_username = username_entry.get()
            new_password = password_entry.get()
            new_role = role_var.get()

            if new_username and new_password:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET username = ?, password = ?, role = ? WHERE username = ?', 
                            (new_username, new_password, new_role, user[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", f"Usuario {new_username} actualizado exitosamente")
                edit_window.destroy()
                self.load_users()  # Reload the user table
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos")

        save_button = tk.Button(content_frame, text="Guardar Cambios", command=save_changes, bg="#00b894", fg="white", font=("Helvetica", 12))
        save_button.pack(pady=5)
        
    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para eliminar")
            return

        user = self.user_tree.item(selected_item)['values']
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el usuario '{user[0]}'?")
        if confirm:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ?', (user[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Usuario '{user[0]}' eliminado exitosamente")
            self.load_users()  # Reload the user table
    
    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if username and password:
            conn = connect()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                            (username, password, role))
                conn.commit()
                messagebox.showinfo("Éxito", f"Usuario {username} agregado como {role}")
                self.load_users()  # Actualizar la tabla de usuarios
                # Limpiar los campos de entrada
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.role_var.set("vendedor")  # Restablecer el rol por defecto
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

# ----------------------------------------------------
# agregar cliente---------------------------------------
    def show_add_client(self):
        self.clear_frame()
        self.main_frame.configure(bg="#f0f0f0")

        # Título de la sección
        title_label = tk.Label(
            self.main_frame, 
            text="Gestión de Clientes", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#000"
        )
        title_label.pack(pady=20)

        # Frame para formulario de nuevo cliente
        add_client_frame = tk.LabelFrame(
            self.main_frame,
            text="Agregar Cliente",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#000",
            padx=15,
            pady=10
        )
        add_client_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Campo para ingresar el nombre del cliente
        tk.Label(
            add_client_frame,
            text="Nombre del Cliente:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        ).grid(row=0, column=0, padx=(5, 10), pady=5, sticky="w")

        self.client_name_entry = tk.Entry(
            add_client_frame,
            font=("Arial", 11),
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        self.client_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Campo para ingresar el saldo inicial del cliente
        tk.Label(
            add_client_frame,
            text="Saldo Inicial:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        ).grid(row=1, column=0, padx=(5, 10), pady=5, sticky="w")

        self.client_balance_entry = tk.Entry(
            add_client_frame,
            font=("Arial", 11),
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        self.client_balance_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botón para agregar cliente
        add_client_button = tk.Button(
            add_client_frame,
            text="Agregar Cliente",
            command=self.add_client,
            font=("Arial", 11, "bold"),
            bg="#00B894",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        add_client_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Tabla de clientes
        client_table_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        client_table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))

        self.client_tree = ttk.Treeview(
            client_table_frame,
            columns=("name", "balance"),
            show="headings",
            height=10
        )
        self.client_tree.heading("name", text="Nombre del Cliente")
        self.client_tree.heading("balance", text="Saldo")
        self.client_tree.column("name", width=200)
        self.client_tree.column("balance", width=100)
        self.client_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Botones para editar y eliminar cliente
        button_frame = tk.Frame(client_table_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)

        edit_button = tk.Button(
            button_frame,
            text="Editar Nombre",
            command=self.edit_client_name,
            font=("Arial", 11),
            bg="#3498DB",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Eliminar Cliente",
            command=self.delete_client,
            font=("Arial", 11),
            bg="#E74C3C",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        # Cargar clientes al iniciar la sección
        self.load_clients_data()

    def add_client(self):
        name = self.client_name_entry.get().strip()
        balance = self.client_balance_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return
        try:
            balance = float(balance)
        except ValueError:
            messagebox.showerror("Error", "Saldo inválido. Ingrese un número válido.")
            return

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name, balance) VALUES (?, ?)", (name, balance))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cliente agregado con éxito.")
        self.client_name_entry.delete(0, tk.END)
        self.client_balance_entry.delete(0, tk.END)
        self.load_clients_data()

    def load_clients_data(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, balance FROM clients")
        for client in cursor.fetchall():
            self.client_tree.insert("", tk.END, values=(client[0], f"${client[1]:.2f}"))
        conn.close()

    def edit_client_name(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un cliente para editar.")
            return

        item = self.client_tree.item(selected[0], "values")
        client_name = item[0]

        # Ventana para editar el nombre del cliente
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Editar Nombre de Cliente")
        edit_window.configure(bg="#f0f0f0")
        edit_window.geometry("300x180")

        # Centrado de la ventana
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f'{width}x{height}+{x}+{y}')

        # Contenedor para centrar los elementos
        content_frame = tk.Frame(edit_window, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(expand=True)

        tk.Label(
            content_frame,
            text="Nuevo Nombre:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        ).grid(row=0, column=0, sticky="w", pady=5)

        name_entry = tk.Entry(content_frame, font=("Arial", 11), width=25)
        name_entry.insert(0, client_name)
        name_entry.grid(row=1, column=0, padx=5, pady=5)

        def save_name_change():
            new_name = name_entry.get().strip()
            if new_name:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("UPDATE clients SET name = ? WHERE name = ?", (new_name, client_name))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Nombre del cliente actualizado.")
                edit_window.destroy()
                self.load_clients_data()
            else:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")

        save_button = tk.Button(
            content_frame,
            text="Guardar Cambios",
            command=save_name_change,
            font=("Arial", 11, "bold"),
            bg="#00b894",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        save_button.grid(row=2, column=0, pady=(15, 0))

        # Configuración de la columna para centrar el contenido
        content_frame.grid_columnconfigure(0, weight=1)

    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar.")
            return

        item = self.client_tree.item(selected[0], "values")
        client_name = item[0]

        if messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar a {client_name}?"):
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE name = ?", (client_name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
            self.load_clients_data()

# ----------------------------------------------------

# agregar producto-------------------------------------
    def show_add_product(self):
        self.clear_frame()
        self.main_frame.configure(bg="#f0f0f0")  # Fondo del frame principal
    
        # Título del formulario
        tk.Label(self.main_frame, text="Agregar Producto", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    
        # Formulario de datos del producto usando LabelFrame, centrado
        form_frame = tk.LabelFrame(self.main_frame, text="Datos del Producto", bg="#f0f0f0", font=("Arial", 12, "bold"))
        form_frame.pack(pady=20, padx=20, fill="x", expand=True)  # Centrando con padx y pady
    
        # Campo de entrada para el nombre del producto (centrado y más largo)
        tk.Label(form_frame, text="Nombre del Producto: ", bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
        self.product_name_entry = tk.Entry(form_frame, width=500)  # Haciendo el input más largo
        self.product_name_entry.pack(padx=10, pady=5, ipady=5)
    
        # Campo de entrada para el código de barras del producto (centrado y más largo)
        tk.Label(form_frame, text="Código de Barras: ", bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
        self.barcode_entry = tk.Entry(form_frame, width=500)
        self.barcode_entry.pack(padx=10, pady=5, ipady=5)
    
        # Campo de entrada para el precio del producto (centrado y más largo)
        tk.Label(form_frame, text="Precio: ", bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
        self.product_price_entry = tk.Entry(form_frame, width=500)
        self.product_price_entry.pack(padx=10, pady=5, ipady=5)
    
        # Campo de entrada para la cantidad del producto (centrado y más largo)
        tk.Label(form_frame, text="Cantidad: ", bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
        self.product_quantity_entry = tk.Entry(form_frame, width=500)
        self.product_quantity_entry.pack(padx=10, pady=5, ipady=5)
    
        # Botón para agregar el producto (centrado)
        tk.Button(form_frame, text="Agregar Producto", command=self.add_product, bg="#00B894", fg="white", font=("Arial", 10, "bold")).pack(padx=10, pady=20)
    
    def add_product(self):
        # Lógica para agregar el producto a la base de datos o lista
        name = self.product_name_entry.get()
        barcode = self.barcode_entry.get()
        price = self.product_price_entry.get()
        stock = self.product_quantity_entry.get()
    
        # Validar que los campos no estén vacíos
        if name and barcode and price and stock:
            try:
                # Validar que el precio y la cantidad sean números
                price = float(price)
                stock = int(stock)
                conn = connect()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO products (name, barcode, price, stock) VALUES (?, ?, ?, ?)', 
                               (name, barcode, price, stock))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", f"Producto '{name}' agregado exitosamente")
            except ValueError:
                messagebox.showerror("Error", "El precio y la cantidad deben ser números válidos")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El código de barras ya existe")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
    
    def show_view_products(self):
        self.clear_frame()

        # Título
        tk.Label(self.main_frame, text="Ver Productos", font=("Arial", 18, "bold")).pack(pady=20)

        # Filtro de búsqueda usando LabelFrame
        filter_frame = tk.LabelFrame(self.main_frame, text="Filtro de Búsqueda", bg="#f0f0f0", font=("Arial", 12, "bold"))
        filter_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(filter_frame, text="Busqueda:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5, pady=5)
        self.filter_entry = tk.Entry(filter_frame, font=("Arial", 12))
        self.filter_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.filter_entry.bind("<KeyRelease>", self.filter_products)

        # Tabla de productos
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Código de Barras", "Precio", "Stock"), 
                                show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones para modificar y eliminar productos
        action_button_frame = tk.Frame(self.main_frame)
        action_button_frame.pack(pady=10)

        tk.Button(action_button_frame, text="Modificar Producto Seleccionado", font=("Arial", 12), bg="#2196F3", fg="white",
                command=self.modify_product).pack(side=tk.LEFT, padx=10)

        tk.Button(action_button_frame, text="Eliminar Producto Seleccionado", font=("Arial", 12), bg="#f44336", fg="white",
                command=self.delete_product).pack(side=tk.LEFT, padx=10)

        self.load_products_to_tree()

    def load_products_to_tree(self, filter_text=""):
        # Limpiar la tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Obtener productos de la base de datos
        conn = connect()
        cursor = conn.cursor()
        if filter_text:
            cursor.execute('''
                SELECT * FROM products 
                WHERE id LIKE ? OR name LIKE ? OR barcode LIKE ? OR price LIKE ?
            ''', ('%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT * FROM products')
        
        for product in cursor.fetchall():
            self.tree.insert("", "end", values=product)
        
        conn.close()

    def filter_products(self, event=None):
        filter_text = self.filter_entry.get()
        self.load_products_to_tree(filter_text)

    def modify_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un producto para modificar")
            return

        product = self.tree.item(selected_item)['values']
        
        # Crear una nueva ventana para modificar el producto
        modify_window = tk.Toplevel(self.master)
        modify_window.title(f"Modificar Producto: {product[1]}")
        modify_window.geometry("450x350")
        modify_window.resizable(False, False)

        # Centrar la ventana en la pantalla
        modify_window.update_idletasks()
        width = modify_window.winfo_width()
        height = modify_window.winfo_height()
        x = (modify_window.winfo_screenwidth() // 2) - (width // 2)
        y = (modify_window.winfo_screenheight() // 2) - (height // 2)
        modify_window.geometry(f"{width}x{height}+{x}+{y}")

        # Frame principal para centrar elementos
        main_frame = tk.Frame(modify_window, padx=20, pady=20)
        main_frame.pack(expand=True)

        # Título
        title_label = tk.Label(main_frame, text="Modificar Producto", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Elementos de entrada organizados
        fields = {
            "Nombre": product[1],
            "Código de Barras": product[2],
            "Precio": product[3],
            "Stock": product[4]
        }
        
        entries = {}
        for i, (label_text, initial_value) in enumerate(fields.items(), start=1):
            label = tk.Label(main_frame, text=f"{label_text}:", font=("Arial", 12), anchor='w')
            label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
            
            entry = tk.Entry(main_frame, font=("Arial", 12))
            entry.insert(0, initial_value)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[label_text] = entry

        # Expandir las columnas para centrar los elementos horizontalmente
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Función para guardar cambios
        def save_changes():
            new_name = entries["Nombre"].get()
            new_barcode = entries["Código de Barras"].get()
            new_price = entries["Precio"].get()
            new_stock = entries["Stock"].get()

            if new_name and new_barcode and new_price and new_stock:
                try:
                    new_price = float(new_price)
                    new_stock = int(new_stock)
                    
                    conn = connect()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        UPDATE products 
                        SET name = ?, barcode = ?, price = ?, stock = ? 
                        WHERE id = ?
                    ''', (new_name, new_barcode, new_price, new_stock, product[0]))
                    
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Éxito", "Producto modificado exitosamente")
                    modify_window.destroy()
                    self.load_products_to_tree()
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese valores válidos")
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos")

        # Función para actualizar el stock
        def update_stock():
            new_stock = entries["Stock"].get()
            if new_stock:
                try:
                    new_stock = int(new_stock)
                    
                    conn = connect()
                    cursor = conn.cursor()
                    
                    cursor.execute('SELECT stock FROM products WHERE id = ?', (product[0],))
                    current_stock = cursor.fetchone()[0]
                    
                    updated_stock = current_stock + new_stock
                    
                    cursor.execute('''
                        UPDATE products 
                        SET stock = ? 
                        WHERE id = ?
                    ''', (updated_stock, product[0]))
                    
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Éxito", "Stock actualizado exitosamente")
                    modify_window.destroy()
                    self.load_products_to_tree()
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese un valor válido")
            else:
                messagebox.showerror("Error", "Por favor, ingrese una cantidad de stock")

        # Botones de acción
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=15)

        tk.Button(button_frame, text="Guardar Cambios", command=save_changes, bg="#00b894", fg="white", font=("Arial", 12), width=20).pack(side="left", padx=10)
        tk.Button(button_frame, text="Actualizar Stock", command=update_stock, bg="#3498db", fg="white", font=("Arial", 12), width=20).pack(side="left", padx=10)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar")
            return

        product = self.tree.item(selected_item)['values']
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el producto '{product[1]}'?")
        if confirm:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Producto '{product[1]}' eliminado exitosamente")
            self.load_products_to_tree()  # Recargar la tabla

# ----------------------------------------------------

# Reportes-----------------------------------
    def show_reports(self):
        self.clear_frame()
        self.main_frame.configure(bg="#f0f0f0")

        tk.Label(self.main_frame, text="Reporte de Ventas", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Frame para filtros
        filter_frame = tk.LabelFrame(self.main_frame, text="Filtro de Fecha", bg="#f0f0f0", font=("Arial", 12, "bold"))
        filter_frame.pack(pady=10, padx=10, fill="x")

        # Filtros de fecha
        tk.Label(filter_frame, text="Desde:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5, pady=5)
        self.start_date = tk.Entry(filter_frame, width=12)
        self.start_date.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(filter_frame, text="Hasta:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5, pady=5)
        self.end_date = tk.Entry(filter_frame, width=12)
        self.end_date.pack(side=tk.LEFT, padx=5, pady=5)

        # Botones de filtro
        tk.Button(filter_frame, 
            text="Filtrar",
            command=self.apply_filter,
            bg="#00B894",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(filter_frame,
            text="Restablecer",
            command=self.reset_filter,
            bg="#FF7675",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Establecer fecha actual por defecto
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.start_date.insert(0, current_date)
        self.end_date.insert(0, current_date)

        # Frame para la tabla
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear tabla
        self.sales_tree = ttk.Treeview(table_frame,
            columns=("ID", "Fecha", "Total", "Detalles"),
            show="headings",
            height=20)

        # Configurar columnas
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Fecha", text="Fecha")
        self.sales_tree.heading("Total", text="Total")
        self.sales_tree.heading("Detalles", text="Detalles de Venta")

        # Ajustar anchos
        self.sales_tree.column("ID", width=50)
        self.sales_tree.column("Fecha", width=150)
        self.sales_tree.column("Total", width=100)
        self.sales_tree.column("Detalles", width=300)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.sales_tree.xview)
        
        self.sales_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Posicionar elementos
        self.sales_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Botón exportar
        export_button = tk.Button(self.main_frame,
            text="Exportar a Excel",
            command=self.export_to_excel,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"))
        export_button.pack(pady=10)

        # Label total
        self.total_label = tk.Label(self.main_frame,
            text="Total de Ventas: $0.00",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0")
        self.total_label.pack(pady=10)

        # Variable para controlar el filtro
        self.filter_active = False
        
        # Iniciar actualización automática
        self.load_sales()
        self.schedule_auto_refresh()

    def load_sales(self):
        # Limpiar tabla
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        conn = connect()
        cursor = conn.cursor()
        
        try:
            if self.filter_active:
                # Consulta con filtro de fechas
                query = '''
                    SELECT 
                        s.id,
                        datetime(s.date) as fecha,
                        s.total,
                        GROUP_CONCAT(
                            p.name || ' x' || sd.quantity || ' ($' || sd.price || ')'
                        ) as detalles
                    FROM sales s
                    LEFT JOIN sale_details sd ON s.id = sd.sale_id
                    LEFT JOIN products p ON sd.product_id = p.id
                    WHERE date(s.date) BETWEEN date(?) AND date(?)
                    GROUP BY s.id
                    ORDER BY s.date DESC
                '''
                start_date = f"{self.start_date.get()} 00:00:00"
                end_date = f"{self.end_date.get()} 23:59:59"
                cursor.execute(query, (start_date, end_date))
            else:
                # Consulta sin filtro
                query = '''
                    SELECT 
                        s.id,
                        datetime(s.date) as fecha,
                        s.total,
                        GROUP_CONCAT(
                            p.name || ' x' || sd.quantity || ' ($' || sd.price || ')'
                        ) as detalles
                    FROM sales s
                    LEFT JOIN sale_details sd ON s.id = sd.sale_id
                    LEFT JOIN products p ON sd.product_id = p.id
                    GROUP BY s.id
                    ORDER BY s.date DESC
                '''
                cursor.execute(query)

            sales = cursor.fetchall()
            
            # Insertar datos y calcular total
            total_sales = 0
            for sale in sales:
                sale_id, fecha, total, detalles = sale
                fecha_formateada = fecha.split('.')[0]
                detalles = detalles if detalles else "Sin detalles"
                
                self.sales_tree.insert("", "end", values=(
                    sale_id,
                    fecha_formateada,
                    f"${total:.2f}",
                    detalles
                ))
                total_sales += total

            # Actualizar total
            self.total_label.config(text=f"Total de Ventas: ${total_sales:.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingresa fechas válidas en formato AAAA-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {str(e)}")
        finally:
            conn.close()

    def apply_filter(self):
        try:
            # Validar formato de fechas
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d')
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d')
            
            if start > end:
                messagebox.showerror("Error", "La fecha inicial no puede ser posterior a la fecha final")
                return
                
            self.filter_active = True
            self.load_sales()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa las fechas en formato AAAA-MM-DD")

    def reset_filter(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
        self.start_date.insert(0, current_date)
        self.end_date.insert(0, current_date)
        self.filter_active = False
        self.load_sales()

    def schedule_auto_refresh(self):
        self.load_sales()
        self.main_frame.after(5000, self.schedule_auto_refresh)

    def export_to_excel(self):
        try:
            data = []
            for item in self.sales_tree.get_children():
                data.append(self.sales_tree.item(item)['values'])

            df = pd.DataFrame(data, columns=["ID", "Fecha", "Total", "Detalles"])

            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"reporte_ventas_{current_datetime}.xlsx"

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=default_filename,
                filetypes=[("Excel files", "*.xlsx")]
            )

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
            try:
                # Obtener datos de la tabla
                data = []
                for item in self.sales_tree.get_children():
                    data.append(self.sales_tree.item(item)['values'])

                # Crear DataFrame
                df = pd.DataFrame(data, columns=["ID", "Fecha", "Total", "Detalles"])

                # Generar nombre de archivo
                current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_filename = f"reporte_ventas_{current_datetime}.xlsx"

                # Solicitar ubicación de guardado
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    initialfile=default_filename,
                    filetypes=[("Excel files", "*.xlsx")]
                )

                if file_path:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")

# ---------------------------------------------
    
# Realizar ventas-----------------------------------
    def show_sales(self):
        self.clear_frame()
        self.main_frame.configure(bg="#f0f0f0")

        # Título principal con estilo mejorado
        title_label = tk.Label(
            self.main_frame, 
            text="Sistema de Ventas", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#000"
        )
        title_label.pack(pady=20)

        # Frame para el filtro de búsqueda con estilo
        filter_frame = tk.LabelFrame(
            self.main_frame,
            text="Búsqueda de Productos",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#000",
            padx=15,
            pady=10
        )
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Campo de búsqueda mejorado
        search_label = tk.Label(
            filter_frame,
            text="Buscar producto:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        )
        search_label.pack(side=tk.LEFT, padx=(5, 10))
        
        self.product_filter_entry = tk.Entry(
            filter_frame,
            font=("Arial", 11),
            width=40,
            bd=2,
            relief=tk.GROOVE
        )
        self.product_filter_entry.pack(side=tk.LEFT, padx=5)
        self.product_filter_entry.bind("<KeyRelease>", self.filter_products_for_sale)

            # Añadir frame para selección de cliente
        client_frame = tk.LabelFrame(
            self.main_frame,
            text="Selección de Cliente (Opcional)",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#000",
            padx=15,
            pady=10
        )
        client_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Combobox para seleccionar cliente
        tk.Label(
            client_frame,
            text="Cliente:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        ).pack(side=tk.LEFT, padx=(5, 10))
        
        self.client_combobox = ttk.Combobox(
            client_frame,
            font=("Arial", 11),
            width=40,
            state="readonly"
        )
        self.client_combobox.pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar lista de clientes
        refresh_button = tk.Button(
            client_frame,
            text="↻",
            command=self.load_clients,
            font=("Arial", 11),
            bg="#3498DB",
            fg="white",
            padx=5,
            cursor="hand2"
        )
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Cargar clientes inicialmente
        self.load_clients()


        # Frame para las tablas y controles
        content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Frame izquierdo para productos disponibles
        left_frame = tk.LabelFrame(
            content_frame,
            text="Productos Disponibles",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#000",
            padx=15,
            pady=10
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Tabla de productos mejorada
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#000",
            fieldbackground="#ffffff",
            rowheight=25
        )
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.product_tree = ttk.Treeview(
            left_frame,
            columns=("name", "price"),
            show="headings",
            height=10
        )
        self.product_tree.heading("name", text="Nombre del Producto")
        self.product_tree.heading("price", text="Precio")
        self.product_tree.column("name", width=200)
        self.product_tree.column("price", width=100)
        self.product_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame para cantidad
        quantity_frame = tk.Frame(left_frame, bg="#f0f0f0")
        quantity_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            quantity_frame,
            text="Cantidad:",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#000"
        ).pack(side=tk.LEFT, padx=5)

        self.quantity_entry = tk.Entry(
            quantity_frame,
            font=("Arial", 11),
            width=40,
            bd=2,
            relief=tk.GROOVE
        )
        self.quantity_entry.pack(side=tk.LEFT, padx=5)

        # Botón agregar con estilo
        add_button = tk.Button(
            left_frame,
            text="Agregar a la Venta",
            command=self.add_to_sale,
            font=("Arial", 11, "bold"),
            bg="#00B894",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        add_button.pack(pady=10)

        # Frame derecho para la venta actual
        right_frame = tk.LabelFrame(
            content_frame,
            text="Venta Actual",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#000",
            padx=15,
            pady=10
        )
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tabla de venta actual mejorada
        self.sale_tree = ttk.Treeview(
            right_frame,
            columns=("name", "price", "quantity"),
            show="headings",
            height=10
        )
        self.sale_tree.heading("name", text="Producto")
        self.sale_tree.heading("price", text="Precio")
        self.sale_tree.heading("quantity", text="Cantidad")
        self.sale_tree.column("name", width=200)
        self.sale_tree.column("price", width=100)
        self.sale_tree.column("quantity", width=100)
        self.sale_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame para botones de acción
        button_frame = tk.Frame(right_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)

        # Botones con estilos mejorados
        modify_button = tk.Button(
            button_frame,
            text="Modificar Cantidad",
            command=self.modify_sale_item,
            font=("Arial", 11),
            bg="#3498DB",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        modify_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Eliminar Producto",
            command=self.delete_sale_item,
            font=("Arial", 11),
            bg="#E74C3C",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        # Botón finalizar venta
        finish_button = tk.Button(
            right_frame,
            text="FINALIZAR VENTA",
            command=self.finish_sale,
            font=("Arial", 12, "bold"),
            bg="#00B894",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        finish_button.pack(pady=15)

        # Cargar productos iniciales
        self.load_products()
    
    def load_clients(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, balance FROM clients")
        clients = cursor.fetchall()
        conn.close()
        
        # Añadir opción "Sin cliente" al inicio
        client_list = ["Sin cliente"] + [f"{client[0]} (Saldo: ${client[1]:.2f})" for client in clients]
        self.client_combobox['values'] = client_list
        self.client_combobox.set("Sin cliente")

    def filter_products_for_sale(self, event=None):
        filter_text = self.product_filter_entry.get()
        self.load_products(filter_text)

    def load_products(self, filter_text=""):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        conn = connect()
        cursor = conn.cursor()
        if filter_text:
            cursor.execute('SELECT name, price FROM products WHERE name LIKE ? OR barcode LIKE ?', ('%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT name, price FROM products')
        for product in cursor.fetchall():
            self.product_tree.insert("", tk.END, values=(product[0], f"${product[1]:.2f}"))
        conn.close()

    def add_to_sale(self):
        selected = self.product_tree.selection()
        if selected:
            product = self.product_tree.item(selected[0], "values")
            quantity = self.quantity_entry.get()
            if quantity.isdigit() and int(quantity) > 0:
                self.sale_tree.insert("", tk.END, values=(product[0], product[1], quantity))
            else:
                messagebox.showerror("Error", "Por favor, ingrese una cantidad válida")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto")

    def modify_sale_item(self):
        selected = self.sale_tree.selection()
        if selected:
            item = self.sale_tree.item(selected[0], "values")
            product_name, price, quantity = item

            # Ventana modal para modificar
            modify_window = tk.Toplevel(self.master)
            modify_window.title("Modificar Cantidad")
            modify_window.configure(bg="#f0f0f0")
            
            # Centrar la ventana
            window_width = 300
            window_height = 180
            screen_width = modify_window.winfo_screenwidth()
            screen_height = modify_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            modify_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Contenido de la ventana
            tk.Label(
                modify_window,
                text=f"Producto: {product_name}",
                font=("Arial", 11, "bold"),
                bg="#f0f0f0",
                fg="#000"
            ).pack(pady=10)

            tk.Label(
                modify_window,
                text="Nueva cantidad:",
                font=("Arial", 11),
                bg="#f0f0f0",
                fg="#000"
            ).pack(pady=5)

            quantity_entry = tk.Entry(
                modify_window,
                font=("Arial", 11),
                width=10,
                bd=2,
                relief=tk.GROOVE
            )
            quantity_entry.insert(0, quantity)
            quantity_entry.pack(pady=5)

            def save_changes():
                new_quantity = quantity_entry.get()
                if new_quantity.isdigit() and int(new_quantity) > 0:
                    self.sale_tree.item(selected[0], values=(product_name, price, new_quantity))
                    modify_window.destroy()
                else:
                    messagebox.showerror("Error", "Por favor, ingrese una cantidad válida")

            tk.Button(
                modify_window,
                text="Guardar",
                command=save_changes,
                font=("Arial", 11),
                bg="#00b894",
                fg="white",
                padx=20,
                pady=5,
                cursor="hand2"
            ).pack(pady=10)

    def delete_sale_item(self):
        selected = self.sale_tree.selection()
        if selected:
            self.sale_tree.delete(selected[0])
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar")

    def finish_sale(self):
        if not self.sale_tree.get_children():
            messagebox.showerror("Error", "No hay productos en la venta")
            return

        total = 0
        sale_items = []

        for item in self.sale_tree.get_children():
            product_name, price, quantity = self.sale_tree.item(item, "values")
            price = float(price.strip("$"))
            quantity = int(quantity)
            total += price * quantity
            sale_items.append((product_name, price, quantity))

        # Obtener cliente seleccionado
        selected_client = self.client_combobox.get()
        if selected_client != "Sin cliente":
            client_name = selected_client.split(" (Saldo:")[0]
            self.process_client_sale(client_name, total, sale_items)
        else:
            self.process_regular_sale(total, sale_items)

    def process_client_sale(self, client_name, total, sale_items):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM clients WHERE name = ?", (client_name,))
        current_balance = cursor.fetchone()[0]
        conn.close()
    
        # Ventana de opciones de pago
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Pago con Cliente")
        payment_window.configure(bg="#f0f0f0")
        payment_window.resizable(False, False)  # Evitar redimensionar
    
        # Configuración de la ventana
        window_width = 400
        window_height = 350  # Aumentar la altura
        screen_width = payment_window.winfo_screenwidth()
        screen_height = payment_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        payment_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        # Frame principal para organizar elementos
        main_frame = tk.Frame(payment_window, bg="#f0f0f0", pady=10, padx=20)
        main_frame.pack(expand=True, fill="both")
    
        # Información del cliente y total
        info_frame = tk.Frame(main_frame, bg="#f0f0f0")
        info_frame.pack(fill="x", pady=(0, 5))
    
        tk.Label(
            info_frame,
            text=f"Cliente: {client_name}",
            font=("Arial", 16, "bold"),  # Aumentar tamaño de fuente
            bg="#f0f0f0",
            fg="#333333"
        ).pack(anchor="center")  # Centrar
    
        balance_color = "#27AE60" if current_balance >= 0 else "#E74C3C"
        tk.Label(
            info_frame,
            text=f"Saldo Actual: ${current_balance:.2f}",
            font=("Arial", 14),  # Aumentar tamaño de fuente
            bg="#f0f0f0",
            fg=balance_color
        ).pack(anchor="center", pady=(5, 0))  # Centrar y reducir espacio
    
        tk.Label(
            info_frame,
            text=f"Total a Pagar: ${total:.2f}",
            font=("Arial", 14, "bold"),  # Aumentar tamaño de fuente
            bg="#f0f0f0",
            fg="#27AE60"
        ).pack(anchor="center", pady=(5, 0))  # Centrar y reducir espacio
    
        # Frame para opciones de pago
        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(fill="x", pady=10)  # Reducir espacio
    
        # Variable para el método de pago
        payment_method = tk.StringVar()
        
        # Frame para el pago en efectivo
        payment_entry_frame = tk.Frame(main_frame, bg="#f0f0f0")
        payment_entry_frame.pack(fill="x", pady=10)
        
        # Crear el label y entry una sola vez
        payment_label = tk.Label(
            payment_entry_frame,
            text="Monto en efectivo:",
            font=("Arial", 11),
            bg="#f0f0f0"
        )
        
        payment_entry = tk.Entry(
            payment_entry_frame,
            font=("Arial", 12),
            width=15,
            bd=2,
            relief=tk.GROOVE
        )
    
        def on_payment_method_change(*args):
            # Limpiar opciones existentes
            for widget in options_frame.winfo_children():
                widget.destroy()
            
            # Ocultar el label y entry de efectivo
            payment_label.pack_forget()
            payment_entry.pack_forget()
            
            # Mostrar opciones según el saldo
            if current_balance >= total:
                tk.Radiobutton(
                    options_frame,
                    text="Usar saldo",
                    variable=payment_method,
                    value="saldo",
                    bg="#f0f0f0",
                    font=("Arial", 11)
                ).pack(anchor="center", pady=2)  # Centrar y reducir espacio
            else:
                tk.Radiobutton(
                    options_frame,
                    text="Añadir a la deuda",
                    variable=payment_method,
                    value="deuda",
                    bg="#f0f0f0",
                    font=("Arial", 11)
                ).pack(anchor="center", pady=2)  # Centrar y reducir espacio
    
            # Siempre mostrar opción de efectivo
            tk.Radiobutton(
                options_frame,
                text="Pagar en efectivo",
                variable=payment_method,
                value="efectivo",
                bg="#f0f0f0",
                font=("Arial", 11)
            ).pack(anchor="center", pady=2)  # Centrar y reducir espacio
    
            # Mostrar entry solo cuando se selecciona efectivo
            if payment_method.get() == "efectivo":
                payment_label.pack(side="left", padx=(0, 10))
                payment_entry.pack(side="left")
    
        # Configurar el callback para el cambio de método de pago
        payment_method.trace_add("write", on_payment_method_change)
        
        # Establecer valor inicial según el saldo
        if current_balance >= total:
            payment_method.set("saldo")
        else:
            payment_method.set("deuda")
        
        def process_payment():
            method = payment_method.get()
            if method == "efectivo":
                try:
                    payment = float(payment_entry.get())
                    if payment >= total:
                        self.complete_sale(sale_items, total)
                        change = payment - total
                        messagebox.showinfo("Éxito", f"Venta completada. Cambio: ${change:.2f}")
                        payment_window.destroy()
                    else:
                        messagebox.showerror("Error", "Monto insuficiente")
                except ValueError:
                    messagebox.showerror("Error", "Monto inválido")
            
            elif method == "saldo":
                if current_balance >= total:
                    new_balance = current_balance - total
                    conn = connect()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE clients SET balance = ? WHERE name = ?", (new_balance, client_name))
                    conn.commit()
                    conn.close()
                    self.complete_sale(sale_items, total)
                    messagebox.showinfo("Éxito", f"Venta completada. Nuevo saldo: ${new_balance:.2f}")
                    payment_window.destroy()
                else:
                    messagebox.showerror("Error", "Saldo insuficiente")
            
            elif method == "deuda":
                new_balance = current_balance - total
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("UPDATE clients SET balance = ? WHERE name = ?", (new_balance, client_name))
                conn.commit()
                conn.close()
                self.complete_sale(sale_items, total)
                messagebox.showinfo("Éxito", f"Venta completada. Nueva deuda: ${abs(new_balance):.2f}")
                payment_window.destroy()
    
        # Botón de procesar pago
        tk.Button(
            main_frame,
            text="Procesar Pago",
            command=process_payment,
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground="#219A52"
        ).pack(pady=10)
            
    def process_regular_sale(self, total, sale_items):
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Pago en Efectivo")
        payment_window.configure(bg="#f0f0f0")
        
        window_width = 400
        window_height = 200
        screen_width = payment_window.winfo_screenwidth()
        screen_height = payment_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        payment_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        tk.Label(
            payment_window,
            text="Total a Pagar:",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#000"
        ).pack(pady=10)

        tk.Label(
            payment_window,
            text=f"${total:.2f}",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#27AE60"
        ).pack(pady=5)

        payment_entry = tk.Entry(
            payment_window,
            font=("Arial", 12),
            width=15,
            bd=2,
            relief=tk.GROOVE
        )
        payment_entry.pack(pady=10)

        def process_payment():
            try:
                payment = float(payment_entry.get())
                if payment >= total:
                    self.complete_sale(sale_items, total)
                    change = payment - total
                    messagebox.showinfo("Éxito", f"Venta completada. Cambio: ${change:.2f}")
                    payment_window.destroy()
                else:
                    messagebox.showerror("Error", "Monto insuficiente")
            except ValueError:
                messagebox.showerror("Error", "Monto inválido")

        tk.Button(
            payment_window,
            text="Procesar Pago",
            command=process_payment,
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(pady=20)


    def complete_sale(self, sale_items, total):
        conn = connect()
        cursor = conn.cursor()

        # Usando 'localtime' para guardar la hora local
        cursor.execute('INSERT INTO sales (date, total) VALUES (datetime("now", "localtime"), ?)', (total,))
        sale_id = cursor.lastrowid

        for product_name, price, quantity in sale_items:
            cursor.execute('SELECT id, stock FROM products WHERE name = ?', (product_name,))
            product = cursor.fetchone()
            if product:
                product_id, stock = product
                new_stock = stock - quantity
                cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
                cursor.execute('INSERT INTO sale_details (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)', 
                            (sale_id, product_id, quantity, price))

        conn.commit()
        conn.close()
        messagebox.showinfo("Venta", "Venta realizada con éxito")
        for item in self.sale_tree.get_children():
            self.sale_tree.delete(item)

# ----------------------------------------------------
def show(username):
    root = tk.Tk()
    AdminPanel(root,username)
    root.mainloop()

if __name__ == "__main__":
    show()