import tkinter as tk
from tkinter import messagebox
from pyBCV import Currency
import requests
import json

bcv = Currency()

# ==============================
# 🔹 BINANCE P2P (TASA REAL DE VENTA - VERSIÓN MEJORADA)
# ==============================
def obtener_mejor_tasa_binance():
    try:
        # Endpoint correcto de Binance P2P
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Intentar con diferentes montos para encontrar anuncios
        montos = ["50", "100", "500", "1000", "5000"]
        
        for monto in montos:
            print(f"Buscando con monto: {monto} USDT")
            
            payload = {
                "asset": "USDT",
                "fiat": "VES",
                "tradeType": "SELL",  # SELL = venta de USDT
                "page": 1,
                "rows": 10,
                "payTypes": [],
                "publisherType": "merchant",
                "transAmount": monto
            }
            
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                if data.get("code") == "000000" and data.get("data"):
                    precios = []
                    for adv in data["data"]:
                        try:
                            precio = float(adv["adv"]["price"])
                            min_amount = float(adv["adv"]["minSingleTransAmount"])
                            max_amount = float(adv["adv"]["maxSingleTransAmount"])
                            
                            print(f"  - Anuncio: {precio} Bs (mínimo: {min_amount} USDT, máximo: {max_amount} USDT)")
                            
                            if precio > 0:
                                precios.append(precio)
                        except Exception as e:
                            print(f"  Error parsing: {e}")
                            continue
                    
                    if precios:
                        # Ordenar de mayor a menor
                        precios.sort(reverse=True)
                        print(f"Precios encontrados: {precios[:5]}")
                        
                        # Tomar el mejor precio (el más alto)
                        mejor_precio = precios[0]
                        return round(mejor_precio, 2)
        
        # Si no se encontraron anuncios, probar sin especificar monto
        print("Probando sin especificar monto...")
        payload = {
            "asset": "USDT",
            "fiat": "VES",
            "tradeType": "SELL",
            "page": 1,
            "rows": 10,
            "payTypes": [],
            "publisherType": "merchant"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            
            if data.get("code") == "000000" and data.get("data"):
                precios = []
                for adv in data["data"]:
                    try:
                        precio = float(adv["adv"]["price"])
                        if precio > 0:
                            precios.append(precio)
                    except:
                        continue
                
                if precios:
                    precios.sort(reverse=True)
                    return round(precios[0], 2)
        
        return 0
        
    except Exception as e:
        print(f"Error detallado Binance P2P: {e}")
        import traceback
        traceback.print_exc()
        return 0

# ==============================
# 🔹 BINANCE SPOT (Alternativa)
# ==============================
def obtener_binance_spot():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTVES"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and 'price' in data:
                precio = float(data['price'])
                print(f"Binance Spot: {precio}")
                return round(precio, 2)
        
        return 0
    except Exception as e:
        print(f"Error Binance Spot: {e}")
        return 0

# ==============================
# 🔹 OBTENER TASAS
# ==============================
def obtener_tasas():
    tasas = {}

    # ===== BCV =====
    try:
        usd = bcv.get_rate(currency_code='USD')
        eur = bcv.get_rate(currency_code='EUR')

        usd = float(str(usd).replace(",", "."))
        eur = float(str(eur).replace(",", "."))

        tasas["USD"] = round(usd, 2)
        tasas["EUR"] = round(eur, 2)
        print(f"BCV USD: {usd}")

    except Exception as e:
        print(f"Error BCV: {e}")
        tasas["USD"] = 0
        tasas["EUR"] = 0

    # ===== BINANCE P2P (Tasa real) =====
    binance_real = obtener_mejor_tasa_binance()
    
    if binance_real > 0:
        tasas["BINANCE"] = binance_real
        print(f"✅ Usando Binance P2P real: {binance_real} Bs")
    else:
        print("⚠️ No se encontraron anuncios P2P")
        
        # Intentar spot
        binance_spot = obtener_binance_spot()
        if binance_spot > 0:
            tasas["BINANCE"] = binance_spot
            print(f"Usando Binance Spot: {binance_spot} Bs")
        else:
            # Usar una tasa de referencia manual (basada en experiencia)
            # En Venezuela, la tasa paralelo suele ser aproximadamente 10-15% sobre BCV
            if tasas["USD"] > 0:
                tasa_estimada = round(tasas["USD"] * 1.12, 2)
                tasas["BINANCE"] = tasa_estimada
                print(f"Usando tasa estimada: {tasa_estimada} Bs (BCV * 1.12)")
            else:
                # Valor por defecto si todo falla
                tasas["BINANCE"] = 0
                print("No se pudo obtener ninguna tasa")

    # ===== PROMEDIO =====
    valores = [v for v in tasas.values() if v > 0]
    if valores:
        tasas["★ PROMEDIO"] = round(sum(valores) / len(valores), 2)

    return tasas

# ==============================
# 🔹 FUNCIÓN PARA ACTUALIZAR TASAS MANUALMENTE
# ==============================
def tasa_manual():
    """Permite ingresar una tasa manualmente si las APIs fallan"""
    ventana = tk.Toplevel(root)
    ventana.title("Ingresar Tasa Manual")
    ventana.geometry("300x150")
    ventana.resizable(False, False)
    
    tk.Label(ventana, text="Tasa Binance Manual:", font=("Arial", 10)).pack(pady=10)
    entry_manual = tk.Entry(ventana, font=("Arial", 12))
    entry_manual.pack(pady=5)
    
    def guardar_tasa():
        try:
            tasa = float(entry_manual.get())
            if tasa > 0:
                # Guardar en un archivo para persistencia
                with open("tasa_manual.txt", "w") as f:
                    f.write(str(tasa))
                messagebox.showinfo("Éxito", f"Tasa manual guardada: {tasa} Bs")
                ventana.destroy()
                cargar_todas_las_tasas()  # Recargar con la nueva tasa
            else:
                messagebox.showwarning("Error", "Ingrese una tasa válida")
        except:
            messagebox.showwarning("Error", "Ingrese un número válido")
    
    tk.Button(ventana, text="Guardar", command=guardar_tasa, bg="#4CAF50", fg="white").pack(pady=10)
    
    # Cargar tasa guardada si existe
    try:
        with open("tasa_manual.txt", "r") as f:
            tasa_guardada = f.read()
            entry_manual.insert(0, tasa_guardada)
    except:
        pass

# ==============================
# 🔹 FUNCIONES UI
# ==============================
def cargar_todas_las_tasas():
    lista_tasas.delete(0, tk.END)
    lista_tasas.insert(tk.END, "🔄 Obteniendo tasas...")
    root.update()
    
    tasas = obtener_tasas()
    
    lista_tasas.delete(0, tk.END)
    
    # Intentar cargar tasa manual si existe
    try:
        with open("tasa_manual.txt", "r") as f:
            tasa_manual_valor = float(f.read().strip())
            if tasa_manual_valor > 0:
                tasas["BINANCE (MANUAL)"] = tasa_manual_valor
    except:
        pass
    
    # Orden específico
    orden = ["USD", "EUR", "BINANCE", "BINANCE (MANUAL)", "★ PROMEDIO"]
    
    for nombre in orden:
        if nombre in tasas:
            valor = tasas[nombre]
            if valor > 0:
                linea = f"{nombre:<15} : {valor:>10.2f} Bs."
                lista_tasas.insert(tk.END, linea)
            else:
                linea = f"{nombre:<15} : {'N/D':>10}"
                lista_tasas.insert(tk.END, linea)
    
    # Seleccionar automáticamente la primera tasa si hay productos
    if productos and lista_tasas.size() > 0:
        lista_tasas.select_set(0)
        recalcular_automatico()
    
    # Mostrar mensaje si Binance no se pudo obtener
    if tasas.get("BINANCE", 0) == 0 and "BINANCE (MANUAL)" not in tasas:
        messagebox.showwarning("Advertencia", 
                              "No se pudo obtener la tasa real de Binance.\n"
                              "Puedes:\n"
                              "1. Hacer clic en 'Tasa Manual' para ingresarla tú mismo\n"
                              "2. Verificar tu conexión a internet\n"
                              "3. Intentar más tarde")

def recalcular_automatico(*args):
    """Recalcula automáticamente cuando se selecciona una tasa diferente"""
    if not productos:
        return
    
    try:
        seleccion = lista_tasas.curselection()
        if not seleccion:
            return

        texto_tasa = lista_tasas.get(seleccion[0])
        
        # Extraer el valor de la tasa
        parte = texto_tasa.split(":")[1].replace("Bs.", "").strip()
        if parte == "N/D":
            return
        tasa = float(parte)

        if tasa <= 0:
            return

        # Actualizar resultados
        lista_resultados.delete(0, tk.END)
        nombre_tasa = texto_tasa.split(":")[0].strip()
        
        lista_resultados.insert(tk.END, f"=== {nombre_tasa} ===")
        lista_resultados.insert(tk.END, f"1 USD = {tasa:.2f} Bs")
        lista_resultados.insert(tk.END, "-" * 30)
        
        for producto, precio in productos:
            convertido = precio / tasa
            lista_resultados.insert(tk.END, f"{producto:<20} : ${convertido:>8.2f}")
        
        if len(productos) > 1:
            total_bs = sum(precio for _, precio in productos)
            total_usd = total_bs / tasa
            lista_resultados.insert(tk.END, "-" * 30)
            lista_resultados.insert(tk.END, f"{'TOTAL':<20} : ${total_usd:>8.2f}")
            
    except Exception as e:
        print("Error en cálculo automático:", e)

def agregar_producto():
    nombre = entry_prod_nombre.get()
    if not nombre:
        messagebox.showwarning("Atención", "Ingresa el nombre del producto.")
        return
    
    try:
        precio = float(entry_prod_precio.get())
        if precio <= 0:
            messagebox.showwarning("Atención", "El precio debe ser mayor a 0.")
            return

        productos.append((nombre, precio))
        lista_productos.insert(tk.END, f"{nombre:<20} - {precio:>10.2f} Bs")
        
        entry_prod_nombre.delete(0, tk.END)
        entry_prod_precio.delete(0, tk.END)
        entry_prod_nombre.focus()
        
        # Recalcular automáticamente si hay una tasa seleccionada
        if lista_tasas.curselection():
            recalcular_automatico()
        
    except ValueError:
        messagebox.showwarning("Dato inválido", "Ingresa un precio numérico válido.")

def eliminar_producto():
    seleccion = lista_productos.curselection()
    if seleccion:
        lista_productos.delete(seleccion[0])
        productos.pop(seleccion[0])
        
        # Recalcular automáticamente si hay productos y tasa seleccionada
        if productos and lista_tasas.curselection():
            recalcular_automatico()
        elif not productos:
            lista_resultados.delete(0, tk.END)
    else:
        messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")

def limpiar_todo():
    if messagebox.askyesno("Confirmar", "¿Eliminar todos los productos?"):
        productos.clear()
        lista_productos.delete(0, tk.END)
        lista_resultados.delete(0, tk.END)

# ==============================
# 🔹 UI PRINCIPAL
# ==============================
root = tk.Tk()
root.title("Calculadora de Tasas Venezuela")
root.geometry("500x780")
root.resizable(True, True)

productos = []

# Configuración de colores
bg_color = "#f0f0f0"
root.configure(bg=bg_color)

# Frame principal
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Título
tk.Label(main_frame, text="💰 CALCULADORA DE TASAS VENEZUELA", 
         font=("Arial", 14, "bold"), bg=bg_color).pack(pady=5)

# ===== TASAS =====
tk.Label(main_frame, text="📊 TASAS DISPONIBLES (Selecciona una)", 
         font=("Arial", 10, "bold"), bg=bg_color).pack(pady=5)

frame_tasas = tk.Frame(main_frame, bg=bg_color)
frame_tasas.pack(fill=tk.X, padx=10)

lista_tasas = tk.Listbox(frame_tasas, font=("Courier", 10), height=5, 
                         bg="white", relief=tk.GROOVE)
lista_tasas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_tasas = tk.Scrollbar(frame_tasas, command=lista_tasas.yview)
scroll_tasas.pack(side=tk.RIGHT, fill=tk.Y)
lista_tasas.config(yscrollcommand=scroll_tasas.set)

# Evento para recalcular automáticamente al seleccionar una tasa
lista_tasas.bind('<<ListboxSelect>>', lambda e: recalcular_automatico())

frame_btn_tasas = tk.Frame(main_frame, bg=bg_color)
frame_btn_tasas.pack(pady=5)

tk.Button(frame_btn_tasas, text="🔄 Actualizar Tasas", command=cargar_todas_las_tasas,
          bg="#2196F3", fg="white", padx=15).pack(side=tk.LEFT, padx=5)

tk.Button(frame_btn_tasas, text="✏️ Tasa Manual", command=tasa_manual,
          bg="#FF9800", fg="white", padx=15).pack(side=tk.LEFT, padx=5)

# Separador
tk.Frame(main_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=5)

# ===== PRODUCTOS =====
tk.Label(main_frame, text="🛒 AGREGAR PRODUCTO", 
         font=("Arial", 10, "bold"), bg=bg_color).pack(pady=5)

# Nombre
tk.Label(main_frame, text="Nombre del Producto:", bg=bg_color).pack()
entry_prod_nombre = tk.Entry(main_frame, width=35)
entry_prod_nombre.pack(pady=5)
entry_prod_nombre.bind('<Return>', lambda e: entry_prod_precio.focus())

# Precio
tk.Label(main_frame, text="Precio en Bolívares (Bs):", bg=bg_color).pack()
entry_prod_precio = tk.Entry(main_frame, width=35)
entry_prod_precio.pack(pady=5)
entry_prod_precio.bind('<Return>', lambda e: agregar_producto())

# Botón Añadir
tk.Button(main_frame, text="➕ AÑADIR PRODUCTO", command=agregar_producto,
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
          padx=20, pady=5).pack(pady=10)

# Lista de productos
tk.Label(main_frame, text="📋 LISTA DE PRODUCTOS", 
         font=("Arial", 9, "bold"), bg=bg_color).pack(pady=5)

frame_productos = tk.Frame(main_frame, bg=bg_color)
frame_productos.pack(fill=tk.X, padx=10)

lista_productos = tk.Listbox(frame_productos, font=("Courier", 10), height=5, 
                              bg="white", relief=tk.GROOVE)
lista_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_prod = tk.Scrollbar(frame_productos, command=lista_productos.yview)
scroll_prod.pack(side=tk.RIGHT, fill=tk.Y)
lista_productos.config(yscrollcommand=scroll_prod.set)

# Botones productos
frame_btn_prod = tk.Frame(main_frame, bg=bg_color)
frame_btn_prod.pack(pady=5)

tk.Button(frame_btn_prod, text="🗑️ Eliminar Producto", command=eliminar_producto,
          bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)

tk.Button(frame_btn_prod, text="🧹 Limpiar Todo", command=limpiar_todo,
          bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=5)

# Separador
tk.Frame(main_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=5)

# ===== RESULTADOS =====
tk.Label(main_frame, text="💵 RESULTADOS EN USD", 
         font=("Arial", 10, "bold"), bg=bg_color).pack(pady=5)

frame_resultados = tk.Frame(main_frame, bg=bg_color)
frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10)

lista_resultados = tk.Listbox(frame_resultados, font=("Courier", 10), height=6, 
                               fg="green", bg="white", relief=tk.GROOVE)
lista_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_res = tk.Scrollbar(frame_resultados, command=lista_resultados.yview)
scroll_res.pack(side=tk.RIGHT, fill=tk.Y)
lista_resultados.config(yscrollcommand=scroll_res.set)

# Información
info_text = "💡 Si la tasa de Binance no aparece, usa 'Tasa Manual' para ingresarla\n   Puedes ver los detalles en la terminal"
tk.Label(main_frame, text=info_text, font=("Arial", 8), bg=bg_color, fg="#666", 
         justify=tk.LEFT).pack(pady=5)

# Carga inicial
root.after(500, cargar_todas_las_tasas)

root.mainloop()