from models import HistorialTasa
from extensions import db
from datetime import datetime
from exchange_provider import ExchangeProvider # Agregamos el import aquí


def guardar_si_cambia(tipo, valor):

    ultima = (
        HistorialTasa.query
        .filter_by(tipo=tipo)
        .order_by(HistorialTasa.fecha.desc())
        .first()
    )

    # Si no hay registros, guardar
    if not ultima:
        nueva = HistorialTasa(
            tipo=tipo,
            valor=valor
        )
        db.session.add(nueva)
        db.session.commit()
        print(f"Guardado inicial {tipo}: {valor}")
        return

    # Si cambió el valor, guardar
    if ultima.valor != valor:
        nueva = HistorialTasa(
            tipo=tipo,
            valor=valor
        )
        db.session.add(nueva)
        db.session.commit()
        print(f"Actualizado {tipo}: {valor}")
    else:
        print(f"Sin cambios {tipo}")
        
        # NUEVA FUNCIÓN MAESTRA
def actualizar_todo():
    """Obtiene y guarda todas las tasas de un solo golpe."""
    try:
        provider = ExchangeProvider()
        tasas = provider.get_all_rates()
        
        guardar_si_cambia("bcv_usd", tasas["bcv_usd"])
        guardar_si_cambia("bcv_eur", tasas["bcv_eur"])
        guardar_si_cambia("p2p_ves", tasas["p2p_ves"])
        return tasas
    except Exception as e:
        print(f"Error al actualizar tasas: {e}")
        return None