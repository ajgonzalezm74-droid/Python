// static/js/calculadora_contable.js - Versión optimizada y ligera

// Variables globales
let chartInstance = null;
let chartLoaded = false;

// Inicialización diferida
document.addEventListener('DOMContentLoaded', function() {
    // Solo inicializar lo esencial
    initEssential();
    
    // Cargar el resto después de que la página sea interactiva
    requestIdleCallback(() => {
        initNonEssential();
    }, { timeout: 2000 });
});

// Funciones esenciales (se cargan inmediatamente)
function initEssential() {
    // Configurar eventos básicos
    setupFormEvents();
    setupFilterButtons();
    setupExportButtons();
    updateTotals();
    
    // Configurar eliminación de items (event delegation)
    const lista = document.getElementById('lista-items');
    if (lista) {
        lista.addEventListener('click', async (e) => {
            const btn = e.target.closest('.btn-eliminar');
            if (btn) {
                e.preventDefault();
                await deleteItem(btn.dataset.id);
            }
        });
    }
}

// Funciones no esenciales (carga diferida)
function initNonEssential() {
    // Configurar modal de gráfico con carga perezosa
    const modal = document.getElementById('modalGrafico');
    if (modal) {
        modal.addEventListener('shown.bs.modal', () => {
            loadChart();
        });
    }
    
    // Pre-cargar librerías si es necesario
    preloadLibraries();
}

// Configurar eventos del formulario
function setupFormEvents() {
    // Guardar tasa seleccionada
    const form = document.getElementById('item-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const tasaSelect = document.getElementById('tasa-selector');
            if (tasaSelect) {
                const selected = tasaSelect.options[tasaSelect.selectedIndex];
                document.getElementById('tasa_referencia').value = tasaSelect.value;
                document.getElementById('tasa_tipo').value = selected.text.split(':')[0].trim();
            }
        });
    }
    
    // Botón limpiar
    const btnLimpiar = document.getElementById('btnLimpiar');
    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', () => {
            document.querySelector('input[name="nombre_item"]').value = '';
            document.querySelector('input[name="precio_bs"]').value = '';
            document.querySelector('select[name="tipo"]').value = 'ingreso';
            document.querySelector('select[name="categoria"]').value = '';
            document.querySelector('textarea[name="notas"]').value = '';
            showToast('Formulario limpiado', 'success');
        });
    }
    
    // Selector de tasa
    const tasaSelector = document.getElementById('tasa-selector');
    if (tasaSelector) {
        tasaSelector.addEventListener('change', () => updateTotals());
    }
}

// Configurar botones de filtro
function setupFilterButtons() {
    document.querySelectorAll('.filtro-periodo').forEach(btn => {
        btn.addEventListener('click', async () => {
            const periodo = btn.dataset.periodo;
            // Actualizar UI
            document.querySelectorAll('.filtro-periodo').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Aplicar filtro
            await applyFilter(periodo);
        });
    });
}

// Aplicar filtro al servidor
async function applyFilter(periodo) {
    try {
        const response = await fetch(`/api/filtrar-movimientos?periodo=${periodo}`);
        const data = await response.json();
        updateList(data.items);
        showToast(data.texto, 'info');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al filtrar', 'error');
    }
}

// Actualizar lista de movimientos
function updateList(items) {
    const container = document.getElementById('lista-items');
    if (!container) return;
    
    if (items.length === 0) {
        container.innerHTML = '<div class="text-center text-muted p-3 small">No hay movimientos</div>';
    } else {
        container.innerHTML = items.map(item => `
            <div class="list-group-item list-group-item-action p-2 border-bottom">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center gap-2 flex-wrap">
                            <strong class="small">${escapeHtml(item.nombre_item)}</strong>
                            ${item.categoria ? `<span class="badge bg-secondary" style="font-size: 9px;">${escapeHtml(item.categoria)}</span>` : ''}
                            <small class="text-muted" style="font-size: 10px;">${item.fecha}</small>
                        </div>
                        <div class="mt-1">
                            <span class="badge ${item.precio_bs >= 0 ? 'bg-success' : 'bg-danger'}" style="font-size: 11px;">
                                ${item.precio_bs >= 0 ? '💰' : '💸'} Bs. ${Math.abs(item.precio_bs).toFixed(0)}
                            </span>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-outline-danger btn-eliminar" data-id="${item.id}" style="padding: 2px 6px;">🗑️</button>
                </div>
            </div>
        `).join('');
    }
    
    updateTotals();
}

// Actualizar totales
function updateTotals() {
    const items = document.querySelectorAll('#lista-items .list-group-item');
    const tasa = parseFloat(document.getElementById('tasa-selector')?.value) || 1;
    
    let ingresos = 0;
    let gastos = 0;
    let ingresosBS = 0;
    let gastosBS = 0;
    
    items.forEach(item => {
        const badge = item.querySelector('.badge.bg-success, .badge.bg-danger');
        if (!badge) return;
        
        const text = badge.textContent;
        const match = text.match(/[\d\.-]+/);
        if (!match) return;
        
        const monto = parseFloat(match[0]);
        
        if (monto > 0) {
            ingresosBS += monto;
            ingresos += monto / tasa;
        } else if (monto < 0) {
            gastosBS += Math.abs(monto);
            gastos += Math.abs(monto) / tasa;
        }
    });
    
    // Actualizar UI
    const totalInc = document.getElementById('total-inc');
    const totalExp = document.getElementById('total-exp');
    const leftover = document.getElementById('leftover');
    const balanceNeto = document.getElementById('balance-neto');
    const totalMovimientos = document.getElementById('total-movimientos');
    
    if (totalInc) totalInc.textContent = `$${ingresos.toFixed(0)}`;
    if (totalExp) totalExp.textContent = `$${gastos.toFixed(0)}`;
    if (leftover) leftover.textContent = `$${(ingresos - gastos).toFixed(0)}`;
    if (balanceNeto) balanceNeto.textContent = `Bs. ${(ingresosBS - gastosBS).toFixed(0)}`;
    if (totalMovimientos) totalMovimientos.textContent = items.length;
}

// Eliminar item
async function deleteItem(itemId) {
    if (!confirm('¿Eliminar este registro?')) return;
    
    try {
        const response = await fetch(`/eliminar-item/${itemId}`, { method: 'DELETE' });
        if (response.ok) {
            const item = document.querySelector(`.btn-eliminar[data-id="${itemId}"]`)?.closest('.list-group-item');
            if (item) {
                item.remove();
                updateTotals();
                showToast('Registro eliminado', 'success');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar', 'error');
    }
}

// Cargar gráfico (solo cuando se necesita)
async function loadChart() {
    if (chartLoaded) return;
    
    // Cargar Chart.js solo cuando se abre el modal
    if (typeof Chart === 'undefined') {
        await loadScript('https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js');
    }
    
    // Obtener datos para el gráfico
    const response = await fetch('/api/gastos-por-categoria');
    const data = await response.json();
    
    const ctx = document.getElementById('graficoGastos').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    if (data.categorias && data.categorias.length > 0) {
        chartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.categorias,
                datasets: [{
                    data: data.valores,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom', labels: { font: { size: 10 } } }
                }
            }
        });
        chartLoaded = true;
    } else {
        ctx.fillStyle = '#ddd';
        ctx.fillRect(0, 0, 300, 300);
        ctx.fillStyle = '#666';
        ctx.font = '12px sans-serif';
        ctx.fillText('No hay datos', 120, 150);
    }
}

// Configurar botones de exportación
function setupExportButtons() {
    const btnExcel = document.getElementById('btnExportarExcel');
    if (btnExcel) {
        btnExcel.addEventListener('click', exportToExcel);
    }
    
    const btnPDF = document.getElementById('btnExportarPDF');
    if (btnPDF) {
        btnPDF.addEventListener('click', exportToPDF);
    }
}

// Exportar a Excel
function exportToExcel() {
    const items = document.querySelectorAll('#lista-items .list-group-item');
    const data = [['Movimiento', 'Monto Bs', 'Categoría', 'Fecha']];
    
    items.forEach(item => {
        const nombre = item.querySelector('strong')?.textContent || '';
        const badge = item.querySelector('.badge.bg-success, .badge.bg-danger');
        const monto = badge?.textContent?.match(/[\d\.-]+/)?.[0] || '0';
        const categoria = item.querySelector('.badge.bg-secondary')?.textContent || '';
        const fecha = item.querySelector('.text-muted')?.textContent || '';
        data.push([nombre, parseFloat(monto), categoria, fecha]);
    });
    
    const ws = XLSX.utils.aoa_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Movimientos');
    XLSX.writeFile(wb, `movimientos_${new Date().toISOString().split('T')[0]}.xlsx`);
    showToast('Exportado a Excel', 'success');
}

// Exportar a PDF (solo el resumen)
function exportToPDF() {
    showToast('Preparando PDF...', 'info');
    
    if (typeof html2pdf === 'undefined') {
        loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js', () => {
            generatePDF();
        });
    } else {
        generatePDF();
    }
}

function generatePDF() {
    const element = document.querySelector('.card-resumen');
    const opt = {
        margin: [0.5, 0.5],
        filename: 'resumen_financiero.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'a5', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save();
    showToast('PDF generado', 'success');
}

// Cargar script dinámicamente
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.onload = callback;
    document.head.appendChild(script);
}

// Mostrar toast notification
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} position-fixed top-0 start-50 translate-middle-x mt-2`;
    toast.style.zIndex = '9999';
    toast.style.minWidth = '250px';
    toast.style.fontSize = '0.8rem';
    toast.innerHTML = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// Escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
