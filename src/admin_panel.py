import tkinter as tk
from models.database import connect

def show():
    window = tk.Tk()
    window.title("Panel de Administración")

    # Campos de producto
    tk.Label(window, text="Nombre del producto").grid(row=0, column=0)
    entry_name = tk.Entry(window)
    entry_name.grid(row=0, column=1)

    tk.Label(window, text="Código de barras").grid(row=1, column=0)
    entry_barcode = tk.Entry(window)
    entry_barcode.grid(row=1, column=1)

    tk.Label(window, text="Precio").grid(row=2, column=0)
    entry_price = tk.Entry(window)
    entry_price.grid(row=2, column=1)

    def add_product():
        name = entry_name.get()
        barcode = entry_barcode.get()
        price = float(entry_price.get())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO products (name, barcode, price) VALUES (?, ?, ?)', (name, barcode, price))
        conn.commit()
        conn.close()

        tk.messagebox.showinfo("Producto agregado", f"Producto '{name}' agregado exitosamente")

    # Botón para agregar producto
    btn_add = tk.Button(window, text="Agregar producto", command=add_product)
    btn_add.grid(row=3, column=0, columnspan=2)

    window.mainloop()
