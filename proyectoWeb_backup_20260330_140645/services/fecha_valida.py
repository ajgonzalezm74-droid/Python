from datetime import datetime, timedelta

def calcular_fecha_valida(fecha=None):
    """
    Calcula la fecha válida de la tasa según el horario del BCV.
    Si no se pasa fecha, usa la fecha actual.
    """

    if fecha is None:
        fecha = datetime.now()

    dia = fecha.weekday()  # lunes=0 ... domingo=6

    # sábado → lunes
    if dia == 5:
        return fecha + timedelta(days=2)

    # domingo → lunes
    if dia == 6:
        return fecha + timedelta(days=1)

    # viernes después de 16:00 → lunes
    if dia == 4 and fecha.hour >= 16:
        return fecha + timedelta(days=3)

    return fecha