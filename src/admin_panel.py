import tkinter as tk
from tkinter import ttk, messagebox
from models.database import connect
import sqlite3

class AdminPanel:
    def __init__(self, master):
        self.master = master
        self.master.title("Panel de Administración")
        self.master.geometry("800x600")

        # Crear el menú superior
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # Agregar opciones al menú
        self.menu.add_command(label="Agregar Usuarios", command=self.show_add_user)
        self.menu.add_command(label="Agregar Productos", command=self.show_add_product)
        self.menu.add_command(label="Ver Productos", command=self.show_view_products)
        self.menu.add_command(label="Generar Reportes", command=self.show_reports)
        self.menu.add_command(label="Realizar Ventas", command=self.show_sales)

        # Frame principal
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Inicialmente mostramos la pantalla de agregar usuarios
        self.show_add_user()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_add_user(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Agregar Usuario", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Nombre de usuario:").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Label(self.main_frame, text="Rol:").pack()
        self.role_var = tk.StringVar(value="vendedor")
        tk.Radiobutton(self.main_frame, text="Admin", variable=self.role_var, value="admin").pack()
        tk.Radiobutton(self.main_frame, text="Vendedor", variable=self.role_var, value="vendedor").pack()

        tk.Button(self.main_frame, text="Agregar Usuario", command=self.add_user).pack(pady=10)

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
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def show_add_product(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Agregar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Nombre del producto:").pack()
        self.product_name_entry = tk.Entry(self.main_frame)
        self.product_name_entry.pack()

        tk.Label(self.main_frame, text="Código de barras:").pack()
        self.barcode_entry = tk.Entry(self.main_frame)
        self.barcode_entry.pack()

        tk.Label(self.main_frame, text="Precio:").pack()
        self.price_entry = tk.Entry(self.main_frame)
        self.price_entry.pack()

        tk.Label(self.main_frame, text="Cantidad en stock:").pack()
        self.stock_entry = tk.Entry(self.main_frame)
        self.stock_entry.pack()

        tk.Button(self.main_frame, text="Agregar Producto", command=self.add_product).pack(pady=10)

    def add_product(self):
        name = self.product_name_entry.get()
        barcode = self.barcode_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if name and barcode and price and stock:
            try:
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
        tk.Label(self.main_frame, text="Ver Productos", font=("Arial", 16)).pack(pady=10)

        # Frame para el filtro
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Filtrar por:").pack(side=tk.LEFT)
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Filtrar", command=self.filter_products).pack(side=tk.LEFT)

        # Tabla de productos
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Nombre", "Código de Barras", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones para modificar y eliminar producto seleccionado
        tk.Button(self.main_frame, text="Modificar Producto Seleccionado", command=self.modify_product).pack(pady=5)
        tk.Button(self.main_frame, text="Eliminar Producto Seleccionado", command=self.delete_product).pack(pady=5)

        # Cargar productos
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
                WHERE id LIKE ? OR name LIKE ? OR barcode LIKE ? OR price LIKE ? OR stock LIKE ?
            ''', ('%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT * FROM products')
        
        for product in cursor.fetchall():
            self.tree.insert("", "end", values=product)
        
        conn.close()

    def filter_products(self):
        filter_text = self.filter_entry.get()
        self.load_products_to_tree(filter_text)
        self.clear_frame()
        tk.Label(self.main_frame, text="Ver Productos", font=("Arial", 16)).pack(pady=10)

        # Frame para el filtro
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Filtrar por:").pack(side=tk.LEFT)
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Filtrar", command=self.filter_products).pack(side=tk.LEFT)

        # Tabla de productos
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Nombre", "Código de Barras", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones para modificar y eliminar producto seleccionado
        tk.Button(self.main_frame, text="Modificar Producto Seleccionado", command=self.modify_product).pack(pady=5)
        tk.Button(self.main_frame, text="Eliminar Producto Seleccionado", command=self.delete_product).pack(pady=5)

        # Cargar productos
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
                WHERE id LIKE ? OR name LIKE ? OR barcode LIKE ? OR price LIKE ? OR stock LIKE ?
            ''', ('%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT * FROM products')
        
        for product in cursor.fetchall():
            self.tree.insert("", "end", values=product)
        
        conn.close()

    def filter_products(self):
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
        
        tk.Label(modify_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(modify_window)
        name_entry.insert(0, product[1])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(modify_window, text="Código de Barras:").grid(row=1, column=0, padx=5, pady=5)
        barcode_entry = tk.Entry(modify_window)
        barcode_entry.insert(0, product[2])
        barcode_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(modify_window, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
        price_entry = tk.Entry(modify_window)
        price_entry.insert(0, product[3])
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(modify_window, text="Stock:").grid(row=3, column=0, padx=5, pady=5)
        stock_entry = tk.Entry(modify_window)
        stock_entry.insert(0, product[4])
        stock_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_entry.get()
            new_barcode = barcode_entry.get()
            new_price = price_entry.get()
            new_stock = stock_entry.get()

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

        def update_stock():
            new_stock = stock_entry.get()
            if new_stock:
                try:
                    new_stock = int(new_stock)
                    
                    conn = connect()
                    cursor = conn.cursor()
                    
                    # Obtener el stock actual del producto
                    cursor.execute('SELECT stock FROM products WHERE id = ?', (product[0],))
                    current_stock = cursor.fetchone()[0]
                    
                    # Actualizar el stock según la lógica especificada
                    if current_stock < 0:
                        updated_stock = current_stock + new_stock
                    else:
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

        tk.Button(modify_window, text="Guardar Cambios", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(modify_window, text="Actualizar Cantidad de Stock", command=update_stock).grid(row=5, column=0, columnspan=2, pady=10)

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

    def show_reports(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Generar Reportes", font=("Arial", 16)).pack(pady=10)
        
        # Aquí puedes agregar opciones para diferentes tipos de reportes
        tk.Button(self.main_frame, text="Reporte de Ventas", command=self.generate_sales_report).pack(pady=5)
        tk.Button(self.main_frame, text="Reporte de Inventario", command=self.generate_inventory_report).pack(pady=5)

    def generate_sales_report(self):
        # Implementa la lógica para generar el reporte de ventas
        messagebox.showinfo("Reporte", "Generando reporte de ventas...")

    def generate_inventory_report(self):
        # Implementa la lógica para generar el reporte de inventario
        messagebox.showinfo("Reporte", "Generando reporte de inventario...")
    def show_sales(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Realizar Venta", font=("Arial", 16)).pack(pady=10)

        # Lista de productos
        self.product_listbox = tk.Listbox(self.main_frame, width=50)
        self.product_listbox.pack(pady=10)
        self.load_products()

        # Cantidad
        tk.Label(self.main_frame, text="Cantidad:").pack()
        self.quantity_entry = tk.Entry(self.main_frame)
        self.quantity_entry.pack()

        # Botón para agregar a la venta
        tk.Button(self.main_frame, text="Agregar a la venta", command=self.add_to_sale).pack(pady=5)

        # Lista de items en la venta actual
        self.sale_listbox = tk.Listbox(self.main_frame, width=50)
        self.sale_listbox.pack(pady=10)

        # Botón para finalizar la venta
        tk.Button(self.main_frame, text="Finalizar Venta", command=self.finish_sale).pack(pady=5)

    def load_products(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name, price FROM products')
        for product in cursor.fetchall():
            self.product_listbox.insert(tk.END, f"{product[0]} - ${product[1]:.2f}")
        conn.close()

    def add_to_sale(self):
        selected = self.product_listbox.curselection()
        if selected:
            product = self.product_listbox.get(selected[0])
            quantity = self.quantity_entry.get()
            if quantity.isdigit() and int(quantity) > 0:
                self.sale_listbox.insert(tk.END, f"{product} x {quantity}")
            else:
                messagebox.showerror("Error", "Por favor, ingrese una cantidad válida")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto")

    def finish_sale(self):
        if self.sale_listbox.size() > 0:
            conn = connect()
            cursor = conn.cursor()
            total = 0
            sale_items = []

            for i in range(self.sale_listbox.size()):
                item = self.sale_listbox.get(i)
                product_name, rest = item.split(" - $")
                price, quantity = rest.split(" x ")
                price = float(price)
                quantity = int(quantity)
                total += price * quantity
                sale_items.append((product_name, price, quantity))

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
            self.sale_listbox.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No hay productos en la venta actual")

def show():
    root = tk.Tk()
    AdminPanel(root)
    root.mainloop()

if __name__ == "__main__":
    show()