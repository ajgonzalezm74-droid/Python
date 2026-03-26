# routes/dashboard.py
from flask import Blueprint, render_template, session, jsonify, request
from routes.auth import login_required
from sqlalchemy import func
from models import db  # ← Importación necesaria

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    nombre = session.get('nombre', 'Usuario')
    return render_template('dashboard.html', nombre=nombre)

# routes/dashboard.py - Reemplaza la función dashboard_stats

@dashboard_bp.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """API para estadísticas del dashboard"""
    from models.cliente import Cliente
    #from models.cobranza import Cobranza
    #from models.pago import Pago
    #from models.cita import Cita
    from datetime import datetime, date
    from sqlalchemy import func
    
    permisos = session.get('permisos', [])
    is_admin = 'admin_total' in permisos
    
    data = {}
    
    # Clientes - Esto es lo que necesitas
    if 'ver_clientes' in permisos or is_admin:
        try:
            # Contar clientes activos
            total = Cliente.query.filter_by(activo=1).count()
            data['total_clientes'] = total
            print(f"📊 Total clientes activos: {total}")
        except Exception as e:
            print(f"❌ Error contando clientes: {e}")
            data['total_clientes'] = 0
    
    # Cobranzas - Comentado temporalmente para evitar errores
    # if 'ver_cobranzas' in permisos or is_admin:
    #     try:
    #         total = db.session.query(func.sum(Cobranza.monto)).filter(
    #             Cobranza.estado == 'pendiente'
    #         ).scalar() or 0
    #         data['total_cobranzas'] = float(total)
    #     except:
    #         data['total_cobranzas'] = 0
    
    # Pagos - Comentado temporalmente
    # if 'ver_pagos' in permisos or is_admin:
    #     try:
    #         mes_actual = datetime.now().strftime('%Y-%m')
    #         total = db.session.query(func.sum(Pago.monto)).filter(
    #             func.strftime('%Y-%m', Pago.fecha) == mes_actual
    #         ).scalar() or 0
    #         data['total_pagos'] = float(total)
    #     except:
    #         data['total_pagos'] = 0
    
    # Citas - Comentado temporalmente
    # if 'ver_citas' in permisos or is_admin:
    #     try:
    #         hoy = date.today().strftime('%Y-%m-%d')
    #         total = Cita.query.filter(func.date(Cita.fecha_hora) == hoy).count()
    #         data['total_citas'] = total
    #     except:
    #         data['total_citas'] = 0
    
    # Valores por defecto para evitar errores
    data.setdefault('total_cobranzas', 0)
    data.setdefault('total_pagos', 0)
    data.setdefault('total_citas', 0)
    
    return jsonify(data)

@dashboard_bp.route('/api/ultimos-clientes')
@login_required
def ultimos_clientes():
    """API para últimos clientes"""
    from models.cliente import Cliente
    
    permisos = session.get('permisos', [])
    if 'ver_clientes' not in permisos and 'admin_total' not in permisos:
        return jsonify([])
    
    try:
        clientes = Cliente.query.filter_by(activo=True).order_by(
            Cliente.id_cliente.desc()
        ).limit(5).all()
        
        print(f"👥 Clientes encontrados: {len(clientes)}")
        for c in clientes:
            print(f"   - {c.id_cliente}: {c.nombre} {c.apellidos}")
        
        return jsonify([{
            'id': c.id_cliente,
            'nombre': c.nombre,
            'apellidos': c.apellidos or '',
            'email': c.email or '',
            'telefono': c.telefono or ''
        } for c in clientes])
        
    except Exception as e:
        print(f"❌ Error al cargar clientes: {e}")
        return jsonify([])

@dashboard_bp.route('/api/proximas-citas')
@login_required
def proximas_citas():
    """API para próximas citas"""
    from models.cita import Cita
    from datetime import datetime
    
    permisos = session.get('permisos', [])
    if 'ver_citas' not in permisos and 'admin_total' not in permisos:
        return jsonify([])
    
    ahora = datetime.now()
    citas = Cita.query.filter(Cita.fecha_hora > ahora).order_by(Cita.fecha_hora).limit(5).all()
    
    return jsonify([{
        'id': c.id,
        'cliente_nombre': c.cliente.nombre if c.cliente else 'Sin cliente',
        'fecha': c.fecha_hora.strftime('%d/%m/%Y'),
        'hora': c.fecha_hora.strftime('%H:%M')
    } for c in citas])