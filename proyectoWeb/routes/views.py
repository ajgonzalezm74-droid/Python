# routes/views.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import HistorialTasa, CalculoUsuario, User
from exchange_provider import ExchangeProvider
from services.tasas_service import guardar_si_cambia, actualizar_todo
from services.analisis_service import calcular_variacion_rango, obtener_historial_por_rango

views = Blueprint("views", __name__)

@views.route("/")
def inicio():
    actualizar_todo()
    return render_template("index.html")

@views.route("/acerca")
def acerca():
    return render_template("acerca.html")

@views.route("/calculadora")
def calculadora():
    provider = ExchangeProvider()
    try:
        binance = provider.get_binance_p2p()
        if not binance or binance <= 0:
            raise ValueError("Binance inválido")
        guardar_si_cambia("p2p_ves", binance)
    except Exception as e:
        print("⚠ Error Binance:", e)
        ultima = HistorialTasa.query.filter_by(tipo="p2p_ves").order_by(HistorialTasa.fecha.desc()).first()
        binance = ultima.valor if ultima else 0.0

    tasas = {
        "bcv_usd": HistorialTasa.query.filter_by(tipo="bcv_usd").order_by(HistorialTasa.fecha.desc()).first().valor,
        "bcv_eur": HistorialTasa.query.filter_by(tipo="bcv_eur").order_by(HistorialTasa.fecha.desc()).first().valor,
        "p2p_ves": binance
    }
    return render_template("calculadora.html", tasas=tasas)

@views.route("/tendencia", methods=["GET", "POST"])
def tendencia():
    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]

    if request.method == "POST":
        tipo = request.form.get("tipo")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
        return render_template("tendencia.html", tipos=tipos, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo=tipo, resultado=resultado)

    return render_template("tendencia.html", tipos=tipos)

@views.route("/historial", methods=["GET", "POST"])
def historial():
    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]
    registros = None
    fecha_inicio = None
    fecha_fin = None
    
    if request.method == "POST":
        tipo = request.form["tipo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        registros = obtener_historial_por_rango(tipo, fecha_inicio, fecha_fin)
        
    return render_template("historial.html", tipos=tipos, registros=registros, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

@views.route("/historial-tendencia", methods=["GET", "POST"])
def historial_tendencia():
    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]
    datos = None
    resultado = None
    fecha_inicio = None
    fecha_fin = None
    
    if request.method == "POST":
        tipo = request.form["tipo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        datos = obtener_historial_por_rango(tipo, fecha_inicio, fecha_fin)
        if datos:
            resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
    
    return render_template("historial_tendencia.html", tipos=tipos, datos=datos, resultado=resultado, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

@views.route("/contacto")
def contacto():
    return render_template("contacto.html")

@views.route("/calculadora-roi", methods=["GET", "POST"])
def calculadora_roi():
    resultado = None
    if request.method == "POST":
        try:
            inversion = float(request.form.get("investment", 0))
            beneficio_mensual = float(request.form.get("monthlySaving", 0))
            meses = int(request.form.get("months", 0))
            
            if meses > 0 and inversion > 0:
                roi_total = beneficio_mensual * meses
                roi_porcentaje = (roi_total / inversion) * 100
                resultado = f"ROI Total: ${roi_total:,.2f} | ROI %: {roi_porcentaje:.2f}%"
            else:
                resultado = "Ingrese valores válidos."
        except ValueError:
            resultado = "Error: Valores numéricos inválidos."
    
    return render_template("calculadora_roi.html", resultado=resultado)

# Calculadora Contable - PROTEGIDA
@views.route('/calculadora-contable', methods=['GET', 'POST'])
@login_required
def calculadora_contable():
    # Obtener tasas actuales
    try:
        from exchange_provider import ExchangeProvider
        provider = ExchangeProvider()
        
        bcv_usd = provider.get_bcv_rates().get('USD', 0)
        p2p_ves = provider.get_binance_p2p() or 0
        
        tasas = {
            'bcv_usd': bcv_usd,
            'bcv_eur': provider.get_bcv_rates().get('EUR', 0),
            'p2p_ves': p2p_ves
        }
    except Exception as e:
        print(f"Error obteniendo tasas: {e}")
        tasas = {'bcv_usd': 0, 'bcv_eur': 0, 'p2p_ves': 0}
    
    if request.method == 'POST':
        try:
            nombre_item = request.form.get('nombre_item')
            precio_bs = request.form.get('precio_bs')
            tipo = request.form.get('tipo')
            tasa_referencia = request.form.get('tasa_referencia')
            tasa_tipo = request.form.get('tasa_tipo')
            
            print(f"DEBUG - Datos recibidos:")
            print(f"  nombre_item: {nombre_item}")
            print(f"  precio_bs: {precio_bs}")
            print(f"  tipo: {tipo}")
            print(f"  tasa_referencia: {tasa_referencia}")
            print(f"  tasa_tipo: {tasa_tipo}")
            
            if not nombre_item or not precio_bs:
                flash('Todos los campos son requeridos', 'error')
                return redirect(url_for('views.calculadora_contable'))
            
            monto = float(precio_bs)
            if tipo == 'gasto':
                monto = -abs(monto)
            elif tipo == 'ingreso':
                monto = abs(monto)
            
            # Crear el nuevo cálculo
            nuevo_calculo = CalculoUsuario(
                user_id=current_user.id,
                nombre_item=nombre_item,
                precio_bs=monto
            )
            
            # Agregar tasa solo si se proporcionó
            if tasa_referencia:
                nuevo_calculo.tasa_usd = float(tasa_referencia)
            if tasa_tipo:
                nuevo_calculo.tasa_tipo = tasa_tipo
            
            db.session.add(nuevo_calculo)
            db.session.commit()
            
            print(f"DEBUG - Item guardado: ID {nuevo_calculo.id}")
            flash('Item guardado correctamente', 'success')
            return redirect(url_for('views.calculadora_contable'))
            
        except ValueError as ve:
            db.session.rollback()
            print(f"Error de valor: {ve}")
            flash(f'Error: El monto debe ser un número válido', 'error')
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            flash(f'Error al guardar: {str(e)}', 'error')
    
    # Obtener items del usuario
    items = CalculoUsuario.query.filter_by(user_id=current_user.id).order_by(CalculoUsuario.fecha.desc()).all()
    print(f"DEBUG - Items encontrados: {len(items)}")
    
    return render_template("calc_contble.html", tasas=tasas, items=items)

# Eliminar item - PROTEGIDA
@views.route('/eliminar-item/<int:item_id>', methods=['DELETE'])
@login_required
def eliminar_item(item_id):
    try:
        item = CalculoUsuario.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400