from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from pyBCV import Currency
import requests
import threading

# Configurar tamaño de ventana para pruebas (opcional)
# Window.size = (360, 640)  # Tamaño típico de teléfono

bcv = Currency()

class ProductoWidget(BoxLayout):
    """Widget para mostrar cada producto con botón de eliminar"""
    def __init__(self, nombre, precio, callback_eliminar, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.precio = precio
        self.callback_eliminar = callback_eliminar
        self.size_hint_y = None
        self.height = dp(45)
        self.spacing = dp(5)
        
        # Nombre del producto
        self.add_widget(Label(
            text=f"{nombre}",
            size_hint_x=0.6,
            halign='left',
            valign='middle'
        ))
        
        # Precio
        self.add_widget(Label(
            text=f"{precio:,.2f} Bs",
            size_hint_x=0.3,
            halign='right',
            valign='middle'
        ))
        
        # Botón eliminar
        btn_eliminar = Button(
            text="X",
            size_hint_x=0.1,
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=dp(14)
        )
        btn_eliminar.bind(on_release=lambda x: self.callback_eliminar(self))
        self.add_widget(btn_eliminar)

class ResultadoWidget(BoxLayout):
    """Widget para mostrar cada resultado"""
    def __init__(self, producto, usd, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(10)
        
        self.add_widget(Label(
            text=producto,
            size_hint_x=0.6,
            halign='left',
            valign='middle'
        ))
        
        self.add_widget(Label(
            text=f"${usd:,.2f}",
            size_hint_x=0.4,
            halign='right',
            valign='middle',
            color=(0.2, 0.8, 0.2, 1)
        ))

class TasaButton(Button):
    """Botón personalizado para las tasas"""
    def __init__(self, nombre, valor, callback, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.valor = valor
        self.callback = callback
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = dp(14)
        
        if valor > 0:
            self.text = f"{nombre:<12} : {valor:>10.2f} Bs"
        else:
            self.text = f"{nombre:<12} : N/D"
        
        self.bind(on_release=lambda x: callback(nombre, valor))

class CalculadoraLayout(BoxLayout):
    productos = ListProperty([])
    tasas = {}
    tasa_actual = None
    tasa_valor_actual = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(5)
        self.padding = dp(10)
        
        Clock.schedule_once(lambda dt: self.cargar_tasas(), 0.5)
    
    # ==============================
    # 🔹 Obtener tasa Binance P2P mejorada
    # ==============================
    def obtener_binance_p2p(self):
        try:
            # Probar con diferentes montos
            montos = ["50", "100", "500", "1000"]
            
            for monto in montos:
                url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                payload = {
                    "asset": "USDT",
                    "fiat": "VES",
                    "tradeType": "SELL",
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
                                if precio > 0:
                                    precios.append(precio)
                            except:
                                continue
                        
                        if precios:
                            mejor_precio = max(precios)
                            print(f"Binance P2P encontrada con monto {monto}: {mejor_precio}")
                            return round(mejor_precio, 2)
            
            # Probar sin monto
            url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json"
            }
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
                        mejor_precio = max(precios)
                        print(f"Binance P2P encontrada sin monto: {mejor_precio}")
                        return round(mejor_precio, 2)
            
            return 0
            
        except Exception as e:
            print(f"Error obteniendo Binance P2P: {e}")
            return 0

    # ==============================
    # 🔹 Obtener todas las tasas
    # ==============================
    def obtener_tasas(self):
        tasas = {}

        # BCV
        try:
            usd = float(str(bcv.get_rate('USD')).replace(",", "."))
            eur = float(str(bcv.get_rate('EUR')).replace(",", "."))
            tasas["USD"] = round(usd, 2)
            tasas["EUR"] = round(eur, 2)
            print(f"BCV USD: {usd}")
        except Exception as e:
            print(f"Error BCV: {e}")
            tasas["USD"] = 0
            tasas["EUR"] = 0

        # Binance P2P
        binance_p2p = self.obtener_binance_p2p()
        
        if binance_p2p > 0:
            tasas["BINANCE"] = binance_p2p
            print(f"✅ Binance P2P: {binance_p2p}")
        elif tasas["USD"] > 0:
            tasas["BINANCE"] = round(tasas["USD"] * 1.12, 2)
            print(f"Estimada Binance: {tasas['BINANCE']}")
        else:
            tasas["BINANCE"] = 0

        # Promedio
        valores = [v for v in tasas.values() if v > 0]
        if valores:
            tasas["★ PROMEDIO"] = round(sum(valores) / len(valores), 2)

        self.tasas = tasas
        return tasas

    # ==============================
    # 🔹 Cargar tasas
    # ==============================
    def cargar_tasas(self):
        """Carga las tasas en un hilo separado"""
        # Mostrar loading
        self.ids.lista_tasas.clear_widgets()
        loading = Label(
            text="🔄 Obteniendo tasas...",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        self.ids.lista_tasas.add_widget(loading)
        
        def obtener_en_hilo():
            tasas = self.obtener_tasas()
            Clock.schedule_once(lambda dt: self.actualizar_botones_tasas(tasas))
        
        threading.Thread(target=obtener_en_hilo, daemon=True).start()
    
    def actualizar_botones_tasas(self, tasas):
        """Actualiza los botones de tasas en la UI"""
        self.ids.lista_tasas.clear_widgets()
        
        orden = ["USD", "EUR", "BINANCE", "★ PROMEDIO"]
        
        for nombre in orden:
            if nombre in tasas:
                valor = tasas[nombre]
                btn = TasaButton(nombre, valor, self.seleccionar_tasa)
                self.ids.lista_tasas.add_widget(btn)
        
        # Botón para tasa manual
        btn_manual = Button(
            text="✏️ Ingresar Tasa Manual",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14),
            background_color=(0.4, 0.4, 0.4, 1)
        )
        btn_manual.bind(on_release=lambda x: self.mostrar_input_manual())
        self.ids.lista_tasas.add_widget(btn_manual)
    
    # ==============================
    # 🔹 Ingresar tasa manual
    # ==============================
    def mostrar_input_manual(self):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        popup = Popup(
            title="Ingresar Tasa Manual",
            size_hint=(0.9, 0.4),
            auto_dismiss=False
        )
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        layout.add_widget(Label(
            text="Ingresa la tasa de Binance que ves en la página:",
            size_hint_y=None,
            height=dp(40),
            font_size=dp(14)
        ))
        
        input_tasa = TextInput(
            text="",
            hint_text="Ejemplo: 675.50",
            multiline=False,
            font_size=dp(16),
            input_filter='float'
        )
        layout.add_widget(input_tasa)
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        def guardar_tasa(instance):
            try:
                tasa = float(input_tasa.text)
                if tasa > 0:
                    self.tasas["MANUAL"] = tasa
                    self.seleccionar_tasa("MANUAL", tasa)
                    popup.dismiss()
                    
                    # Actualizar botones
                    self.actualizar_botones_tasas(self.tasas)
            except:
                pass
        
        btn_guardar = Button(text="Guardar", background_color=(0.2, 0.6, 0.2, 1))
        btn_guardar.bind(on_release=guardar_tasa)
        
        btn_cancelar = Button(text="Cancelar", background_color=(0.6, 0.2, 0.2, 1))
        btn_cancelar.bind(on_release=lambda x: popup.dismiss())
        
        btn_layout.add_widget(btn_guardar)
        btn_layout.add_widget(btn_cancelar)
        layout.add_widget(btn_layout)
        
        popup.content = layout
        popup.open()
    
    # ==============================
    # 🔹 Seleccionar tasa y calcular
    # ==============================
    def seleccionar_tasa(self, nombre, valor):
        """Selecciona una tasa y recalcula automáticamente"""
        self.tasa_actual = nombre
        self.tasa_valor_actual = valor
        
        # Actualizar label de tasa seleccionada
        self.ids.tasa_seleccionada.text = f"📌 Tasa: {nombre} - 1 USD = {valor:.2f} Bs"
        
        # Recalcular
        self.recalcular()
    
    # ==============================
    # 🔹 Agregar producto
    # ==============================
    def agregar_producto(self):
        nombre = self.ids.input_nombre.text.strip()
        precio_text = self.ids.input_precio.text.strip()

        if not nombre or not precio_text:
            return

        try:
            precio = float(precio_text)
            if precio <= 0:
                return
                
            self.productos.append((nombre, precio))
            
            # Agregar widget a la lista
            producto_widget = ProductoWidget(
                nombre, 
                precio, 
                self.eliminar_producto
            )
            self.ids.lista_productos.add_widget(producto_widget)

            # Limpiar inputs
            self.ids.input_nombre.text = ""
            self.ids.input_precio.text = ""

            # Recalcular si hay tasa seleccionada
            if self.tasa_actual:
                self.recalcular()

        except:
            pass
    
    def eliminar_producto(self, widget):
        """Elimina un producto específico"""
        try:
            # Buscar y eliminar de la lista
            for i, (nombre, precio) in enumerate(self.productos):
                if nombre == widget.nombre and precio == widget.precio:
                    self.productos.pop(i)
                    break
            
            # Eliminar widget
            self.ids.lista_productos.remove_widget(widget)
            
            # Recalcular si hay tasa seleccionada
            if self.tasa_actual and self.productos:
                self.recalcular()
            elif not self.productos:
                self.ids.resultados_container.clear_widgets()
                
        except:
            pass
    
    # ==============================
    # 🔹 Recalcular resultados
    # ==============================
    def recalcular(self):
        """Calcula y muestra los resultados"""
        self.ids.resultados_container.clear_widgets()
        
        if self.tasa_valor_actual <= 0:
            self.ids.resultados_container.add_widget(Label(
                text="⚠️ Selecciona una tasa válida",
                size_hint_y=None,
                height=dp(40),
                font_size=dp(14),
                color=(0.8, 0.4, 0, 1)
            ))
            return
        
        if not self.productos:
            self.ids.resultados_container.add_widget(Label(
                text="📝 Agrega productos para ver resultados",
                size_hint_y=None,
                height=dp(40),
                font_size=dp(14)
            ))
            return
        
        total = 0
        
        for producto, precio in self.productos:
            usd = precio / self.tasa_valor_actual
            total += usd
            
            resultado = ResultadoWidget(producto, usd)
            self.ids.resultados_container.add_widget(resultado)
        
        # Mostrar total
        if len(self.productos) > 1:
            self.ids.resultados_container.add_widget(Label(
                text="-" * 30,
                size_hint_y=None,
                height=dp(20),
                font_size=dp(12)
            ))
            
            total_widget = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
            total_widget.add_widget(Label(
                text="TOTAL",
                bold=True,
                size_hint_x=0.6,
                halign='left',
                valign='middle',
                font_size=dp(16)
            ))
            total_widget.add_widget(Label(
                text=f"${total:,.2f}",
                bold=True,
                size_hint_x=0.4,
                halign='right',
                valign='middle',
                color=(0.2, 0.8, 0.2, 1),
                font_size=dp(16)
            ))
            self.ids.resultados_container.add_widget(total_widget)


class CalculadoraApp(App):
    def build(self):
        # Configurar la aplicación para que sea responsive
        from kivy.core.window import Window
        
        # Hacer que la ventana sea redimensionable
        Window.size = (400, 700)  # Tamaño inicial, se puede cambiar
        Window.minimum_width = 300
        Window.minimum_height = 500
        
        return CalculadoraLayout()


if __name__ == "__main__":
    CalculadoraApp().run()