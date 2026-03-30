// Función para calcular totales en USD
function calcularTotales() {
    const items = document.querySelectorAll('#lista-items .list-group-item:not(.text-muted)');
    
    let ingresosUSD = 0;
    let gastosUSD = 0;
    
    items.forEach(itemElement => {
        // Buscar el badge con el valor en USD (si existe)
        const usdBadge = itemElement.querySelector('.badge.bg-info');
        if (usdBadge) {
            const usdText = usdBadge.textContent;
            const montoUSD = parseFloat(usdText.replace('$', '').trim());
            
            if (montoUSD > 0) {
                ingresosUSD += montoUSD;
            } else if (montoUSD < 0) {
                gastosUSD += Math.abs(montoUSD);
            }
        } else {
            // Si no tiene tasa guardada, usar la tasa actual
            const bsBadge = itemElement.querySelector('.badge.bg-success, .badge.bg-danger');
            if (bsBadge) {
                const bsText = bsBadge.textContent;
                const montoBs = parseFloat(bsText.replace('Bs.', '').trim());
                const tasaActual = parseFloat(document.getElementById('tasa-selector').value) || 1;
                const montoUSD = montoBs / tasaActual;
                
                if (montoBs > 0) {
                    ingresosUSD += montoUSD;
                } else if (montoBs < 0) {
                    gastosUSD += Math.abs(montoUSD);
                }
            }
        }
    });
    
    const leftoverUSD = ingresosUSD - gastosUSD;
    
    // Actualizar la interfaz
    document.getElementById('total-inc').textContent = `$${ingresosUSD.toFixed(2)}`;
    document.getElementById('total-exp').textContent = `$${gastosUSD.toFixed(2)}`;
    document.getElementById('leftover').textContent = `$${leftoverUSD.toFixed(2)}`;
    
    // Cambiar color según resultado
    const leftoverSpan = document.getElementById('leftover');
    if (leftoverUSD >= 0) {
        leftoverSpan.classList.add('text-success');
        leftoverSpan.classList.remove('text-danger');
    } else {
        leftoverSpan.classList.add('text-danger');
        leftoverSpan.classList.remove('text-success');
    }
}

// Guardar la tasa seleccionada al enviar el formulario
document.getElementById('item-form').addEventListener('submit', function() {
    const tasaSelect = document.getElementById('tasa-selector');
    const selectedOption = tasaSelect.options[tasaSelect.selectedIndex];
    const tasaValor = tasaSelect.value;
    const tasaTipo = selectedOption.text.split(':')[0].trim();
    
    document.getElementById('tasa_referencia').value = tasaValor;
    document.getElementById('tasa_tipo').value = tasaTipo;
});

// Eliminar items
document.querySelectorAll('.btn-eliminar').forEach(btn => {
    btn.addEventListener('click', async function() {
        const itemId = this.dataset.id;
        if (confirm('¿Eliminar este registro?')) {
            try {
                const response = await fetch(`/eliminar-item/${itemId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    this.closest('.list-group-item').remove();
                    calcularTotales();
                    
                    if (document.querySelectorAll('#lista-items .list-group-item:not(.text-muted)').length === 0) {
                        const emptyMsg = document.createElement('div');
                        emptyMsg.className = 'list-group-item text-center text-muted';
                        emptyMsg.textContent = 'No hay movimientos registrados';
                        document.getElementById('lista-items').appendChild(emptyMsg);
                    }
                } else {
                    const data = await response.json();
                    alert(data.message || 'Error al eliminar');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al eliminar el registro');
            }
        }
    });
});

// Escuchar cambios en el selector de tasas
const tasaSelector = document.getElementById('tasa-selector');
if (tasaSelector) {
    tasaSelector.addEventListener('change', calcularTotales);
}

// Calcular totales al cargar la página
document.addEventListener('DOMContentLoaded', calcularTotales);