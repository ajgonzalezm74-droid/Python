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

// static/js/calculadora.js

// Variables globales
let graficoGastos = null;
let deferredPrompt = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    inicializarEventos();
    calcularTotalesYGrafico();
    inicializarPWA();
});

// Inicializar todos los eventos
function inicializarEventos() {
    // Botón limpiar formulario
    const btnLimpiar = document.getElementById('btnLimpiar');
    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', limpiarFormulario);
    }
    
    // Guardar tasa al enviar formulario
    const form = document.getElementById('item-form');
    if (form) {
        form.addEventListener('submit', guardarTasaSeleccionada);
    }
    
    // Selector de tasa
    const tasaSelector = document.getElementById('tasa-selector');
    if (tasaSelector) {
        tasaSelector.addEventListener('change', calcularTotalesYGrafico);
    }
    
    // Filtros de período
    document.querySelectorAll('.filtro-periodo').forEach(btn => {
        btn.addEventListener('click', () => filtrarPorPeriodo(btn.dataset.periodo));
    });
    
    // Botones de exportación
    const btnPDF = document.getElementById('btnExportarPDF');
    if (btnPDF) btnPDF.addEventListener('click', exportarPDF);
    
    const btnExcel = document.getElementById('btnExportarExcel');
    if (btnExcel) btnExcel.addEventListener('click', exportarExcel);
    
    // Eliminar items (event delegation)
    document.getElementById('lista-items')?.addEventListener('click', async (e) => {
        const btnEliminar = e.target.closest('.btn-eliminar');
        if (btnEliminar) {
            await eliminarItem(btnEliminar.dataset.id);
        }
    });
}

// Limpiar formulario
function limpiarFormulario() {
    document.querySelector('input[name="nombre_item"]').value = '';
    document.querySelector('input[name="precio_bs"]').value = '';
    document.querySelector('select[name="tipo"]').value = 'ingreso';
    document.querySelector('select[name="categoria"]').value = '';
    document.querySelector('textarea[name="notas"]').value = '';
    
    // Mostrar mensaje de éxito
    mostrarMensaje('Formulario limpiado', 'success');
}

// Guardar tasa seleccionada
function guardarTasaSeleccionada() {
    const tasaSelect = document.getElementById('tasa-selector');
    const selectedOption = tasaSelect.options[tasaSelect.selectedIndex];
    document.getElementById('tasa_referencia').value = tasaSelect.value;
    document.getElementById('tasa_tipo').value = selectedOption.text.split(':')[0].trim();
}

// Eliminar item
async function eliminarItem(itemId) {
    if (!confirm('¿Eliminar este registro?')) return;
    
    try {
        const response = await fetch(`/eliminar-item/${itemId}`, { method: 'DELETE' });
        if (response.ok) {
            const item = document.querySelector(`.btn-eliminar[data-id="${itemId}"]`)?.closest('.list-group-item');
            if (item) {
                item.remove();
                calcularTotalesYGrafico();
                mostrarMensaje('Registro eliminado', 'success');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje('Error al eliminar', 'error');
    }
}

// Calcular totales y actualizar gráfico
function calcularTotalesYGrafico() {
    const items = document.querySelectorAll('#lista-items .list-group-item');
    const tasa = parseFloat(document.getElementById('tasa-selector')?.value) || 1;
    
    let ingresosUSD = 0;
    let gastosUSD = 0;
    let gastosPorCategoria = {};
    
    items.forEach(item => {
        // Buscar el badge de monto
        const badgeMonto = item.querySelector('.badge-monto');
        if (!badgeMonto) return;
        
        const texto = badgeMonto.textContent;
        const match = texto.match(/[\d\.-]+/);
        if (!match) return;
        
        const montoBs = parseFloat(match[0]);
        const montoUSD = Math.abs(montoBs) / tasa;
        
        // Obtener categoría
        const categoriaSpan = item.querySelector('.badge-categoria');
        const categoria = categoriaSpan ? categoriaSpan.textContent : 'otros';
        
        if (montoBs > 0) {
            ingresosUSD += montoUSD;
        } else if (montoBs < 0) {
            gastosUSD += montoUSD;
            gastosPorCategoria[categoria] = (gastosPorCategoria[categoria] || 0) + montoUSD;
        }
    });
    
    // Actualizar totales en USD
    const totalInc = document.getElementById('total-inc');
    const totalExp = document.getElementById('total-exp');
    const leftover = document.getElementById('leftover');
    
    if (totalInc) totalInc.textContent = `$${ingresosUSD.toFixed(2)}`;
    if (totalExp) totalExp.textContent = `$${gastosUSD.toFixed(2)}`;
    if (leftover) {
        const leftoverValue = ingresosUSD - gastosUSD;
        leftover.textContent = `$${leftoverValue.toFixed(2)}`;
        leftover.classList.remove('leftover-positive', 'leftover-negative');
        leftover.classList.add(leftoverValue >= 0 ? 'leftover-positive' : 'leftover-negative');
    }
    
    // Actualizar gráfico
    actualizarGrafico(gastosPorCategoria);
}

// Actualizar gráfico de torta
function actualizarGrafico(datos) {
    const canvas = document.getElementById('graficoGastos');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const categorias = Object.keys(datos);
    const valores = Object.values(datos);
    
    // Destruir gráfico anterior si existe
    if (graficoGastos) {
        graficoGastos.destroy();
    }
    
    // Crear nuevo gráfico
    if (categorias.length > 0) {
        graficoGastos = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categorias.map(c => {
                    const iconos = {
                        'comida': '🍔', 'transporte': '🚗', 'servicios': '💡',
                        'alquiler': '🏠', 'entretenimiento': '🎬', 'salud': '🏥',
                        'educacion': '📚', 'otros': '📦'
                    };
                    return `${iconos[c] || '📦'} ${c}`;
                }),
                datasets: [{
                    data: valores,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#C9CBCF', '#66FF66'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: { font: { size: 12 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const porcentaje = ((value / total) * 100).toFixed(1);
                                return `${label}: $${value.toFixed(2)} (${porcentaje}%)`;
                            }
                        }
                    }
                }
            }
        });
    } else {
        // Gráfico vacío
        graficoGastos = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Sin datos'],
                datasets: [{ data: [1], backgroundColor: ['#CCCCCC'] }]
            },
            options: {
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: { callbacks: { label: () => 'No hay datos' } }
                }
            }
        });
    }
}

// Filtrar por período
async function filtrarPorPeriodo(periodo) {
    // Actualizar UI de botones
    document.querySelectorAll('.filtro-periodo').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.periodo === periodo) {
            btn.classList.add('active');
        }
    });
    
    try {
        const response = await fetch(`/api/filtrar-movimientos?periodo=${periodo}`);
        const data = await response.json();
        actualizarLista(data.items);
        mostrarMensaje(`Mostrando movimientos: ${data.texto}`, 'info');
    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje('Error al filtrar', 'error');
    }
}

// Actualizar lista después de filtrar
function actualizarLista(items) {
    const contenedor = document.getElementById('lista-items');
    if (!contenedor) return;
    
    contenedor.innerHTML = '';
    
    if (items.length === 0) {
        contenedor.innerHTML = '<div class="list-group-item text-center text-muted">No hay movimientos en este período</div>';
    } else {
        items.forEach(item => {
            const monto = parseFloat(item.precio_bs);
            const esIngreso = monto >= 0;
            
            contenedor.innerHTML += `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div>
                                <strong>${escapeHtml(item.nombre_item)}</strong>
                                ${item.categoria ? `<span class="badge bg-secondary ms-2 badge-categoria">${escapeHtml(item.categoria)}</span>` : ''}
                                <small class="text-muted ms-2">${item.fecha}</small>
                            </div>
                            <div class="mt-1">
                                <span class="badge badge-monto ${esIngreso ? 'badge-ingreso' : 'badge-gasto'}">
                                    ${esIngreso ? '💰' : '💸'} Bs. ${Math.abs(monto).toFixed(2)}
                                </span>
                                ${item.tasa_usd ? `<span class="badge badge-usd ms-1">$${(Math.abs(monto) / item.tasa_usd).toFixed(2)}</span>` : ''}
                            </div>
                            ${item.notas ? `<div class="small text-muted mt-1">${escapeHtml(item.notas)}</div>` : ''}
                        </div>
                        <button class="btn btn-sm btn-outline-danger btn-eliminar" data-id="${item.id}">
                            🗑️
                        </button>
                    </div>
                </div>
            `;
        });
        
        // Reasignar eventos de eliminar
        document.querySelectorAll('.btn-eliminar').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                await eliminarItem(btn.dataset.id);
            });
        });
    }
    
    calcularTotalesYGrafico();
}

// Exportar a PDF
function exportarPDF() {
    const element = document.querySelector('.col-md-6:last-child');
    if (!element) return;
    
    const opt = {
        margin: [0.5, 0.5, 0.5, 0.5],
        filename: 'resumen_financiero.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, letterRendering: true },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    
    mostrarMensaje('Generando PDF...', 'info');
    html2pdf().set(opt).from(element).save()
        .then(() => mostrarMensaje('PDF generado exitosamente', 'success'))
        .catch(err => {
            console.error('Error:', err);
            mostrarMensaje('Error al generar PDF', 'error');
        });
}

// Exportar a Excel
function exportarExcel() {
    const items = document.querySelectorAll('#lista-items .list-group-item');
    const datos = [['Movimiento', 'Monto (Bs)', 'Categoría', 'Fecha', 'Notas']];
    
    items.forEach(item => {
        const nombre = item.querySelector('strong')?.textContent || '';
        const badgeMonto = item.querySelector('.badge-monto');
        const montoTexto = badgeMonto?.textContent || '';
        const montoMatch = montoTexto.match(/[\d\.-]+/);
        const monto = montoMatch ? parseFloat(montoMatch[0]) : 0;
        const categoria = item.querySelector('.badge-categoria')?.textContent || '';
        const fechaSpan = item.querySelector('.text-muted:first-child');
        const fecha = fechaSpan?.textContent || '';
        const notasDiv = item.querySelector('.text-muted.mt-1');
        const notas = notasDiv?.textContent || '';
        datos.push([nombre, monto, categoria, fecha, notas]);
    });
    
    const ws = XLSX.utils.aoa_to_sheet(datos);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Movimientos');
    
    mostrarMensaje('Exportando a Excel...', 'info');
    XLSX.writeFile(wb, `movimientos_${new Date().toISOString().split('T')[0]}.xlsx`);
    mostrarMensaje('Excel generado exitosamente', 'success');
}

// Mostrar mensaje temporal
function mostrarMensaje(mensaje, tipo) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo === 'error' ? 'danger' : tipo === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Inicializar PWA
function inicializarPWA() {
    const isInstalled = window.matchMedia('(display-mode: standalone)').matches;
    
    if (!isInstalled) {
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Crear botón de instalación
            const installBtn = document.createElement('div');
            installBtn.id = 'pwa-install-btn';
            installBtn.innerHTML = `
                <div style="position: fixed; bottom: 20px; right: 20px; z-index: 10000;">
                    <button id="installPwaBtn" class="btn-install-pwa">
                        📱 Instalar App
                    </button>
                </div>
            `;
            document.body.appendChild(installBtn);
            
            document.getElementById('installPwaBtn')?.addEventListener('click', () => {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('Usuario instaló la app');
                        installBtn.remove();
                    }
                    deferredPrompt = null;
                });
            });
        });
    }
}

// Función para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Escuchar cambios en la lista (MutationObserver)
const observer = new MutationObserver(() => {
    calcularTotalesYGrafico();
});

const listaItems = document.getElementById('lista-items');
if (listaItems) {
    observer.observe(listaItems, { childList: true, subtree: true });
}