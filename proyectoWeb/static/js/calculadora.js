function agregarCalculo() {
    const monto_ext = document.getElementById('monto_ext').value;
    const selectTasa = document.getElementById('tipoTasa');
    const tasaValor = parseFloat(selectTasa.value);
    const tasaNombre = selectTasa.options[selectTasa.selectedIndex].text.split('(')[0]; // Obtiene el nombre (BCV, Binance, etc)
    const tabla = document.getElementById('lista_calculos');

    if (monto_ext > 0) {
        const total = (monto_ext * tasaValor).toFixed(2);
        
        // Formateo de moneda
        const totalFormateado = new Intl.NumberFormat('es-VE', { 
            minimumFractionDigits: 2 
        }).format(total);

        // Crear una nueva fila en la tabla
        const nuevaFila = document.createElement('tr');
        nuevaFila.innerHTML = `
            <td>${monto_ext} USD</td>
            <td>${tasaNombre}</td>
            <td class="fw-bold text-warning">${totalFormateado} Bs.</td>
            <td><button class="btn btn-sm text-danger" onclick="this.closest('tr').remove()">✕</button></td>
        `;

        // Insertar al principio de la lista
        tabla.prepend(nuevaFila);

        // Limpiar el input para el siguiente cálculo
        document.getElementById('monto_ext').value = "";
        document.getElementById('resultado_ves').value = "";
    } else {
        alert("Por favor, ingresa un monto válido.");
    }
}

function limpiarLista() {
    if(confirm("¿Deseas borrar todos los cálculos acumulados?")) {
        document.getElementById('lista_calculos').innerHTML = "";
    }
}