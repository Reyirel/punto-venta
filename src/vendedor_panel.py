import tkinter as tk
from tkinter import ttk, messagebox
from models.database import connect
import sqlite3

class VendedorPanel:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Panel de Vendedor")
        self.master.geometry("800x600")

        # Mostrar el nombre de usuario en la parte superior
        tk.Label(self.master, text=f"Usuario: {username}", font=("Arial", 12)).pack(pady=5)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_sales()

    def show_sales(self):
        tk.Label(self.main_frame, text="Realizar Venta", font=("Arial", 16)).pack(pady=10)
    
        # Campo de entrada para el filtro de búsqueda
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(filter_frame, text="Filtrar:").pack(side=tk.LEFT)
        self.product_filter_entry = tk.Entry(filter_frame)
        self.product_filter_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Filtrar", command=self.filter_products_for_sale).pack(side=tk.LEFT)
    
        # Tabla de productos
        self.product_tree = ttk.Treeview(self.main_frame, columns=("name", "barcode", "price"), show="headings", height=5)
        self.product_tree.heading("name", text="Nombre")
        self.product_tree.heading("barcode", text="Código de Barras")
        self.product_tree.heading("price", text="Precio")
        self.product_tree.column("name", width=200)
        self.product_tree.column("barcode", width=150)
        self.product_tree.column("price", width=100)
        self.product_tree.pack(pady=10)
        self.load_products()
    
        # Cantidad
        tk.Label(self.main_frame, text="Cantidad:").pack()
        self.quantity_entry = tk.Entry(self.main_frame)
        self.quantity_entry.pack()
    
        # Botón para agregar a la venta
        tk.Button(self.main_frame, text="Agregar a la venta", command=self.add_to_sale).pack(pady=5)
    
        # Tabla de items en la venta actual
        self.sale_tree = ttk.Treeview(self.main_frame, columns=("name", "price", "quantity"), show="headings")
        self.sale_tree.heading("name", text="Nombre")
        self.sale_tree.heading("price", text="Precio")
        self.sale_tree.heading("quantity", text="Cantidad")
        self.sale_tree.pack(pady=10)
    
        # Botones para modificar y eliminar productos en la venta
        tk.Button(self.main_frame, text="Modificar Producto Seleccionado", command=self.modify_sale_item).pack(pady=5)
        tk.Button(self.main_frame, text="Eliminar Producto Seleccionado", command=self.delete_sale_item).pack(pady=5)
    
        # Botón para finalizar la venta
        tk.Button(self.main_frame, text="Finalizar Venta", command=self.finish_sale).pack(pady=5)

    def filter_products_for_sale(self):
        filter_text = self.product_filter_entry.get()
        self.load_products(filter_text)
    
    def load_products(self, filter_text=""):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        conn = connect()
        cursor = conn.cursor()
        if filter_text:
            cursor.execute('SELECT name, barcode, price FROM products WHERE name LIKE ? OR barcode LIKE ?', ('%' + filter_text + '%', '%' + filter_text + '%'))
        else:
            cursor.execute('SELECT name, barcode, price FROM products')
        for product in cursor.fetchall():
            self.product_tree.insert("", tk.END, values=(product[0], product[1], f"${product[2]:.2f}"))
        conn.close()

    def add_to_sale(self):
        selected = self.product_tree.selection()
        if selected:
            product = self.product_tree.item(selected[0], "values")
            quantity = self.quantity_entry.get()
            if quantity.isdigit() and int(quantity) > 0:
                self.sale_tree.insert("", tk.END, values=(product[0], product[2], quantity))
            else:
                messagebox.showerror("Error", "Por favor, ingrese una cantidad válida")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto")

    def modify_sale_item(self):
        selected = self.sale_tree.selection()
        if selected:
            item = self.sale_tree.item(selected[0], "values")
            product_name, price, quantity = item

            modify_window = tk.Toplevel(self.master)
            modify_window.title(f"Modificar Producto: {product_name}")

            tk.Label(modify_window, text="Cantidad:").grid(row=0, column=0, padx=5, pady=5)
            quantity_entry = tk.Entry(modify_window)
            quantity_entry.insert(0, quantity)
            quantity_entry.grid(row=0, column=1, padx=5, pady=5)

            def save_changes():
                new_quantity = quantity_entry.get()
                if new_quantity.isdigit() and int(new_quantity) > 0:
                    self.sale_tree.item(selected[0], values=(product_name, price, new_quantity))
                    modify_window.destroy()
                else:
                    messagebox.showerror("Error", "Por favor, ingrese una cantidad válida")

            tk.Button(modify_window, text="Guardar Cambios", command=save_changes).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_sale_item(self):
        selected = self.sale_tree.selection()
        if selected:
            self.sale_tree.delete(selected[0])
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar")

    def finish_sale(self):
        if self.sale_tree.get_children():
            conn = connect()
            cursor = conn.cursor()
            total = 0
            sale_items = []

            for item in self.sale_tree.get_children():
                product_name, price, quantity = self.sale_tree.item(item, "values")
                price = float(price.strip("$"))
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
            for item in self.sale_tree.get_children():
                self.sale_tree.delete(item)
        else:
            messagebox.showerror("Error", "No hay productos en la venta actual")

def show(username):
    root = tk.Tk()
    VendedorPanel(root, username)
    root.mainloop()

if __name__ == "__main__":
    show("vendedor")  # Para pruebas, puedes cambiar "vendedor" por cualquier nombre de usuario