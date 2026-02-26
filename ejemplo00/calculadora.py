import tkinter as tk
from tkinter import messagebox
from pyBCV import Currency

bcv = Currency()

def cargar_tasa_automatica():
    """Obtiene la tasa del BCV y la pone en el cuadro de entrada al iniciar"""
    try:
        tasa_actual = bcv.get_rate(currency_code='USD')
        entry_tasa.delete(0, tk.END)
        entry_tasa.insert(0, str(tasa_actual))
    except Exception as e:
        messagebox.showwarning("Aviso", "No se pudo obtener la tasa automática. Ingrésala manualmente.")


def calcular():
    try:
        # CORRECCIÓN: Primero obtenemos el valor del Entry y luego lo convertimos a float
        tasa_texto = entry_tasa.get()
        tasa = float(tasa_texto)
        
        if tasa <= 0:
            raise ValueError
        
        lista_resultados.delete(0, tk.END)
        
        if not productos:
            messagebox.showwarning("Atención", "La lista de productos está vacía.")
            return

        for producto, precio in productos:
            precio_convertido = precio / tasa
            lista_resultados.insert(tk.END, f"{producto}: ${precio_convertido:.2f}")
            
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa una tasa de cambio válida (número mayor a 0).")

def agregar_producto():
    nombre = entry_prod_nombre.get()
    try:
        precio = float(entry_prod_precio.get())
        if nombre == "":
            nombre = "Producto sin nombre"
        
        productos.append((nombre, precio))
        lista_productos.insert(tk.END, f"{nombre} - {precio}Bs")
        
        # Limpiar campos de entrada
        entry_prod_nombre.delete(0, tk.END)
        entry_prod_precio.delete(0, tk.END)
    except ValueError:
        messagebox.showwarning("Dato inválido", "Ingresa un precio numérico para el producto.")

# Seccion de limpiar
def limpiar_todo():
    productos.clear() # vacia la memoria
    lista_productos.delete(0,tk.END) #limpia cuadro de productos
    lista_resultados.delete(0,tk.END) #limpia cuadro de resultados

    messagebox.showinfo("Limpieza","Lista Borrada. puede iniciar el calculo")


# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Precios por Tasa")
root.geometry("400x600")

productos = []

# --- Sección Tasa ---
tk.Label(root, text="Tasa de Cambio (ej. 1 USD = X):", font=("Arial", 10, "bold")).pack(pady=5)
entry_tasa = tk.Entry(root)
entry_tasa.pack()

tk.Button(root, text="Actualizar Tasa BCV", command=cargar_tasa_automatica, font=("Arial", 8)).pack(pady=2)
tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

# --- Sección Agregar Productos ---
tk.Label(root, text="Nombre del Producto:").pack()
entry_prod_nombre = tk.Entry(root)
entry_prod_nombre.pack()

tk.Label(root, text="Precio (Moneda Local):").pack()
entry_prod_precio = tk.Entry(root) 
entry_prod_precio.pack()

tk.Button(root, text="Añadir a la lista", command=agregar_producto, bg="#0622a3",fg="white").pack(pady=5)

# --- Listas y Resultados ---
tk.Label(root, text="Lista de Productos:", font=("Arial", 8, "italic")).pack()
lista_productos = tk.Listbox(root, height=5)
lista_productos.pack(fill=tk.X, padx=20)

tk.Button(root, text="CALCULAR CONVERSIÓN", command=calcular, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

#boton de limpiar
tk.Button(root, text="limpiar la lista", command=limpiar_todo, bg="#810a0a",fg="white").pack(pady=5)

tk.Label(root, text="Precios Convertidos:", font=("Arial", 10, "bold")).pack()
lista_resultados = tk.Listbox(root, height=5, fg="blue")
lista_resultados.pack(fill=tk.X, padx=20)

# Ejecutar carga inicial de tasa
cargar_tasa_automatica()

root.mainloop()
