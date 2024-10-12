import tkinter as tk

def show():
    window = tk.Tk()
    window.title("Panel de Vendedor")

    tk.Label(window, text="Bienvenido al panel de vendedor").pack()

    window.mainloop()
