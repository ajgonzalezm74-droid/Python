from models import HistorialTasa
from extensions import db
from datetime import datetime


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