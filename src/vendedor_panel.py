import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.database import connect
import sqlite3
from datetime import datetime
import pandas as pd

class VendedorPanel:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Panel de Vendedor")
        self.master.state('zoomed')  # Iniciar en pantalla completa
        self.master.resizable(0, 0)

        # Paleta de colores moderna
        self.colors = {
            'primary': "#2D3436",
            'secondary': "#636E72",
            'accent': "#00B894",
            'text': "#FFFFFF",
            'text_disabled': "#B2BEC3"
        }

        # Frame principal con diseño moderno
        self.menu_frame = tk.Frame(self.master, bg=self.colors['primary'], width=250)
        self.menu_frame.pack_propagate(False)  # Mantener el ancho fijo
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Header del menú con el nombre de usuario
        header_frame = tk.Frame(self.menu_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X, padx=15, pady=(20, 10))

        # Título "Panel Vendedor"
        tk.Label(header_frame, text="Panel Vendedor", font=("Helvetica", 14), bg=self.colors['primary'], fg=self.colors['text']).pack(anchor="w")

        # Nombre de usuario con estilo
        tk.Label(header_frame, text=username, font=("Helvetica", 12), bg=self.colors['primary'], fg=self.colors['text_disabled']).pack(anchor="w")

        # Separador
        ttk.Separator(self.menu_frame).pack(fill=tk.X, padx=15, pady=10)

        # Opciones del menú
        menu_options = [
            ("📋 Ver Productos", self.show_view_products),
            ("💰 Realizar Ventas", self.show_sales),
        ]
        
        # Frame para los botones del menú
        buttons_frame = tk.Frame(self.menu_frame, bg=self.colors['primary'])
        buttons_frame.pack(fill=tk.X, pady=10)

        self.buttons = []
        self.current_section = None

        for text, command in menu_options:
            button = tk.Button(buttons_frame, text=text, font=("Helvetica", 12), bg=self.colors['primary'], fg=self.colors['text'], bd=0, anchor="w", command=lambda cmd=command, txt=text: self.change_section(cmd, txt))
            button.pack(fill=tk.X, padx=15, pady=5)
            button.bind("<Enter>", lambda e, btn=button: self.on_enter(e, btn))
            button.bind("<Leave>", lambda e, btn=button: self.on_leave(e, btn))
            self.buttons.append(button)

        # Frame principal para el contenido
        self.main_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inicialmente mostramos la primera opción
        self.show_view_products()

    def on_enter(self, e, button):
        if button.cget('text') != self.current_section:
            button.configure(bg=self.colors['secondary'])

    def on_leave(self, e, button):
        if button.cget('text') != self.current_section:
            button.configure(bg=self.colors['primary'])

    def change_section(self, command, button_text):
        # Resetear el botón previamente seleccionado
        if self.current_section:
            for btn in self.buttons:
                if btn.cget('text') == self.current_section:
                    btn.configure(bg=self.colors['primary'])
                    break

        # Actualizar la sección actual
        self.current_section = button_text

        # Resaltar el botón seleccionado
        for btn in self.buttons:
            if btn.cget('text') == button_text:
                btn.configure(bg=self.colors['secondary'])
                break

        # Ejecutar el comando
        command()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_view_products(self):
        self.clear_frame()
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

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Código de Barras", "Precio", "Stock"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones para modificar y eliminar productos
        action_button_frame = tk.Frame(self.main_frame)
        action_button_frame.pack(pady=10)
        self.load_products_to_tree()

    def filter_products(self, event=None):
        filter_text = self.filter_entry.get()
        self.load_products_to_tree(filter_text)

    def load_products_to_tree(self, filter_text=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = connect()
        cursor = conn.cursor()
        if filter_text:
            cursor.execute('SELECT id, name, barcode, price, stock FROM products WHERE name LIKE ? OR barcode LIKE ?', ('%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT id, name, barcode, price, stock FROM products')
        for product in cursor.fetchall():
            self.tree.insert("", tk.END, values=product)
        conn.close()

    def modify_product(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], "values")
            product_id, name, barcode, price, stock = item

            modify_window = tk.Toplevel(self.master)
            modify_window.title(f"Modificar Producto: {name}")

            tk.Label(modify_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
            name_entry = tk.Entry(modify_window)
            name_entry.insert(0, name)
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(modify_window, text="Código de Barras:").grid(row=1, column=0, padx=5, pady=5)
            barcode_entry = tk.Entry(modify_window)
            barcode_entry.insert(0, barcode)
            barcode_entry.grid(row=1, column=1, padx=5, pady=5)

            tk.Label(modify_window, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
            price_entry = tk.Entry(modify_window)
            price_entry.insert(0, price)
            price_entry.grid(row=2, column=1, padx=5, pady=5)

            tk.Label(modify_window, text="Stock:").grid(row=3, column=0, padx=5, pady=5)
            stock_entry = tk.Entry(modify_window)
            stock_entry.insert(0, stock)
            stock_entry.grid(row=3, column=1, padx=5, pady=5)

            def save_changes():
                new_name = name_entry.get()
                new_barcode = barcode_entry.get()
                new_price = price_entry.get()
                new_stock = stock_entry.get()
                if new_name and new_barcode and new_price and new_stock:
                    conn = connect()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE products SET name = ?, barcode = ?, price = ?, stock = ? WHERE id = ?', (new_name, new_barcode, new_price, new_stock, product_id))
                    conn.commit()
                    conn.close()
                    self.load_products_to_tree()
                    modify_window.destroy()
                else:
                    messagebox.showerror("Error", "Por favor, complete todos los campos")

            tk.Button(modify_window, text="Guardar Cambios", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)


# venta de productos ----------------------------------
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
        search_label.pack(side=tk.LEFT, padx=(5, 100))
        
        self.product_filter_entry = tk.Entry(
            filter_frame,
            font=("Arial", 11),
            width=100,
            bd=2,
            relief=tk.GROOVE
        )
        self.product_filter_entry.pack(side=tk.LEFT, padx=5)
        self.product_filter_entry.bind("<KeyRelease>", self.filter_products_for_sale)

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
            bg="#009bc5",
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
            window_height = 150
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
                bg="#2ECC71",
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
        if self.sale_tree.get_children():
            total = 0
            sale_items = []

            for item in self.sale_tree.get_children():
                product_name, price, quantity = self.sale_tree.item(item, "values")
                price = float(price.strip("$"))
                quantity = int(quantity)
                total += price * quantity
                sale_items.append((product_name, price, quantity))

            # Ventana de pago mejorada
            payment_window = tk.Toplevel(self.master)
            payment_window.title("Finalizar Venta")
            payment_window.configure(bg="#f0f0f0")
            
            # Centrar la ventana
            window_width = 400
            window_height = 250
            screen_width = payment_window.winfo_screenwidth()
            screen_height = payment_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            payment_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Contenido de la ventana
            tk.Label(
                payment_window,
                text="Resumen de la Venta",
                font=("Arial", 16, "bold"),
                bg="#f0f0f0",
                fg="#000"
            ).pack(pady=15)

            tk.Label(
                payment_window,
                text=f"Total a Pagar: ${total:.2f}",
                font=("Arial", 14, "bold"),
                bg="#f0f0f0",
                fg="#27AE60"
            ).pack(pady=10)

            tk.Label(
                payment_window,
                text="Monto Recibido:",
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="#000"
            ).pack(pady=5)

            payment_entry = tk.Entry(
                payment_window,
                font=("Arial", 12),
                width=15,
                bd=2,
                relief=tk.GROOVE
            )
            payment_entry.pack(pady=5)

            def process_payment():
                payment = payment_entry.get()
                try:
                    payment = float(payment)
                    if payment >= total:
                        change = payment - total
                        messagebox.showinfo(
                            "Venta Exitosa",
                            f"Venta realizada con éxito\nCambio a entregar: ${change:.2f}"
                        )
                        payment_window.destroy()
                        self.complete_sale(sale_items, total)
                    else:
                        messagebox.showerror("Error", "El monto recibido es insuficiente")
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese un monto válido")

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

        cursor.execute('INSERT INTO sales (date, total) VALUES (datetime("now"), ?)', (total,))
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


def show(username):
    root = tk.Tk()
    VendedorPanel(root, username)
    root.mainloop()

if __name__ == "__main__":
    show("vendedor")