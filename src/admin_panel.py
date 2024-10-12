import tkinter as tk
from tkinter import ttk, messagebox
from models.database import connect

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

        tk.Button(self.main_frame, text="Agregar Producto", command=self.add_product).pack(pady=10)

    def add_product(self):
        name = self.product_name_entry.get()
        barcode = self.barcode_entry.get()
        price = self.price_entry.get()

        if name and barcode and price:
            try:
                price = float(price)
                conn = connect()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO products (name, barcode, price) VALUES (?, ?, ?)', 
                               (name, barcode, price))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", f"Producto '{name}' agregado exitosamente")
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El código de barras ya existe")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

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
            # Aquí implementarías la lógica para guardar la venta en la base de datos
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