# routes/views.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import HistorialTasa, CalculoUsuario, User
from exchange_provider import ExchangeProvider
from services.tasas_service import guardar_si_cambia, actualizar_todo
from services.analisis_service import calcular_variacion_rango, obtener_historial_por_rango

views = Blueprint("views", __name__)

#--------------------------------------------------------------------------
# Página de inicio - PÚBLICA
#--------------------------------------------------------------------------
@views.route("/")
def inicio():
    actualizar_todo()
    return render_template("index.html")

#--------------------------------------------------------------------------
# Página de acerca - PÚBLICA
#--------------------------------------------------------------------------
@views.route("/acerca")
def acerca():
    return render_template("acerca.html")

#--------------------------------------------------------------------------
# Página de calculadora - PÚBLICA
#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
# Página de tendencia - PÚBLICA
#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
# Página de historial - PÚBLICA
#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
# Página de historial y tendencia combinados - PÚBLICA
#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
# Página de contacto - PÚBLICA
#--------------------------------------------------------------------------

@views.route("/contacto")
def contacto():
    return render_template("contacto.html")

#--------------------------------------------------------------------------
# Calculadora ROI - PÚBLICA
#--------------------------------------------------------------------------

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

#--------------------------------------------------------------------------
# Calculadora Contable - PROTEGIDA
#--------------------------------------------------------------------------

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
            categoria = request.form.get('categoria')  # Obtener categoría
            notas = request.form.get('notas')  # Obtener notas
            
            print(f"DEBUG - Datos recibidos:")
            print(f"  nombre_item: {nombre_item}")
            print(f"  precio_bs: {precio_bs}")
            print(f"  tipo: {tipo}")
            print(f"  tasa_referencia: {tasa_referencia}")
            print(f"  tasa_tipo: {tasa_tipo}")
            print(f"  categoria: {categoria}")
            print(f"  notas: {notas}")
            
            if not nombre_item or not precio_bs:
                flash('Todos los campos son requeridos', 'error')
                return redirect(url_for('views.calculadora_contable'))
            
            monto = float(precio_bs)
            if tipo == 'gasto':
                monto = -abs(monto)
            elif tipo == 'ingreso':
                monto = abs(monto)
            
            # Crear el nuevo cálculo con todos los campos
            nuevo_calculo = CalculoUsuario(
                user_id=current_user.id,
                nombre_item=nombre_item,
                precio_bs=monto,
                categoria=categoria if categoria and categoria != '' else None,
                notas=notas if notas and notas != '' else None
            )
            
            # Agregar tasa solo si se proporcionó
            if tasa_referencia:
                nuevo_calculo.tasa_usd = float(tasa_referencia)
            if tasa_tipo:
                nuevo_calculo.tasa_tipo = tasa_tipo
            
            db.session.add(nuevo_calculo)
            db.session.commit()
            
            print(f"DEBUG - Item guardado: ID {nuevo_calculo.id}")
            flash(f'{tipo.capitalize()} registrado: {nombre_item} - Bs. {monto:,.2f}', 'success')
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

#--------------------------------------------------------------------------
# Eliminar item - PROTEGIDA
#--------------------------------------------------------------------------
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
    
#--------------------------------------------------------------------------
# Página de gráficos - PROTEGIDA
#--------------------------------------------------------------------------    

@views.route('/graficos')
@login_required
def graficos():
    """Página de gráficos estadísticos"""
    return render_template("graficos.html")

#--------------------------------------------------------------------------
# API para estadísticas - PROTEGIDA
#--------------------------------------------------------------------------
@views.route('/api/estadisticas')
@login_required
def api_estadisticas():
    """API para obtener estadísticas para gráficos"""
    from datetime import datetime, timedelta
    import calendar
    
    periodo = request.args.get('periodo', 'dia')
    hoy = datetime.utcnow()
    
    # Definir fechas según período
    if periodo == 'dia':
        fecha_inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
        texto_periodo = "Hoy"
    elif periodo == 'semana':
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fecha_inicio = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        texto_periodo = "Esta semana"
    elif periodo == 'mes':
        fecha_inicio = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        texto_periodo = "Este mes"
    else:
        fecha_inicio = datetime(2000, 1, 1)
        texto_periodo = "Todos los movimientos"
    
    # Obtener movimientos del usuario
    movimientos = CalculoUsuario.query.filter(
        CalculoUsuario.user_id == current_user.id,
        CalculoUsuario.fecha >= fecha_inicio
    ).all()
    
    print(f"API: {len(movimientos)} movimientos encontrados")
    
    # Obtener tasa actual
    try:
        from exchange_provider import ExchangeProvider
        provider = ExchangeProvider()
        tasa = provider.get_bcv_rates().get('USD', 60)
        if not tasa or tasa <= 0:
            tasa = 60
    except:
        tasa = 60
    
    # Calcular totales
    total_ingresos_bs = 0
    total_gastos_bs = 0
    gastos_por_categoria = {}
    
    for m in movimientos:
        if m.precio_bs > 0:
            total_ingresos_bs += m.precio_bs
        elif m.precio_bs < 0:
            total_gastos_bs += abs(m.precio_bs)
            # Usar getattr para evitar error si no existe el atributo
            cat = getattr(m, 'categoria', None)
            if not cat:
                cat = 'otros'
            gastos_por_categoria[cat] = gastos_por_categoria.get(cat, 0) + abs(m.precio_bs)
    
    # Convertir a USD
    total_ingresos = total_ingresos_bs / tasa
    total_gastos = total_gastos_bs / tasa
    balance = total_ingresos - total_gastos
    
    # Convertir gastos por categoría a USD
    gastos_por_categoria_usd = {k: v / tasa for k, v in gastos_por_categoria.items()}
    
    # Datos mensuales (últimos 6 meses)
    meses = []
    ingresos_mensuales = []
    gastos_mensuales = []
    
    for i in range(5, -1, -1):
        fecha_mes = hoy - timedelta(days=30*i)
        mes_nombre = calendar.month_name[fecha_mes.month][:3]
        meses.append(f"{mes_nombre} {fecha_mes.year}")
        
        inicio_mes = fecha_mes.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if fecha_mes.month == 12:
            fin_mes = fecha_mes.replace(year=fecha_mes.year+1, month=1, day=1)
        else:
            fin_mes = fecha_mes.replace(month=fecha_mes.month+1, day=1)
        
        mov_mes = CalculoUsuario.query.filter(
            CalculoUsuario.user_id == current_user.id,
            CalculoUsuario.fecha >= inicio_mes,
            CalculoUsuario.fecha < fin_mes
        ).all()
        
        ingresos_mes = sum(m.precio_bs for m in mov_mes if m.precio_bs > 0) / tasa
        gastos_mes = sum(abs(m.precio_bs) for m in mov_mes if m.precio_bs < 0) / tasa
        
        ingresos_mensuales.append(ingresos_mes)
        gastos_mensuales.append(gastos_mes)
    
    return jsonify({
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'gastos_por_categoria': gastos_por_categoria_usd,
        'meses': meses,
        'ingresos_mensuales': ingresos_mensuales,
        'gastos_mensuales': gastos_mensuales,
        'periodo': texto_periodo,
        'total_movimientos': len(movimientos)
    })  
    
    #--------------------------------------------------------------------------
    # Agregar al final del archivo views.py
    #--------------------------------------------------------------------------
@views.route('/api/filtrar-movimientos')
@login_required
def api_filtrar_movimientos():
    """API para filtrar movimientos por período"""
    from datetime import datetime, timedelta
    
    periodo = request.args.get('periodo', 'todo')
    hoy = datetime.utcnow()
    
    if periodo == 'dia':
        fecha_inicio = hoy.replace(hour=0, minute=0, second=0)
        texto = 'Hoy'
    elif periodo == 'semana':
        fecha_inicio = hoy - timedelta(days=hoy.weekday())
        fecha_inicio = fecha_inicio.replace(hour=0, minute=0, second=0)
        texto = 'Esta semana'
    elif periodo == 'mes':
        fecha_inicio = hoy.replace(day=1, hour=0, minute=0, second=0)
        texto = 'Este mes'
    else:
        fecha_inicio = None
        texto = 'Todos los movimientos'
    
    query = CalculoUsuario.query.filter_by(user_id=current_user.id)
    if fecha_inicio:
        query = query.filter(CalculoUsuario.fecha >= fecha_inicio)
    
    items = query.order_by(CalculoUsuario.fecha.desc()).all()
    
    return jsonify({
        'items': [{
            'id': i.id,
            'nombre_item': i.nombre_item,
            'precio_bs': i.precio_bs,
            'categoria': i.categoria,
            'notas': i.notas,
            'fecha': i.fecha.strftime('%d/%m/%Y %H:%M'),
            'tasa_usd': i.tasa_usd
        } for i in items],
        'texto': texto
    })