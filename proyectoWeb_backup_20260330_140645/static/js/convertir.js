function convertir() {
            // Obtenemos la tasa seleccionada del dropdown
            const tasaActiva = parseFloat(document.getElementById('tipoTasa').value);
            const monto = document.getElementById('monto_ext').value;
            const campoDestino = document.getElementById('resultado_ves');
            
            if (monto > 0) {
                const total = (monto * tasaActiva).toFixed(2);
                // Formateo de moneda local
                campoDestino.value = new Intl.NumberFormat('es-VE', { 
                    style: 'currency', 
                    currency: 'VES' 
                }).format(total);
            } else {
                campoDestino.value = "";
            }
        }