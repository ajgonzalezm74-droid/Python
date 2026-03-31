// static/js/graficos_integrado.js

let chartInstance = null;
let datosActuales = null;

// Mostrar gráficos
document.getElementById('btnMostrarGraficos')?.addEventListener('click', function() {
    const container = document.getElementById('graficos-container');
    if (container) {
        container.style.display = 'block';
        container.scrollIntoView({ behavior: 'smooth' });
        cargarDatosGraficos('dia');
    }
});

// Cerrar gráficos
document.getElementById('btnCerrarGraficos')?.addEventListener('click', function() {
    document.getElementById('graficos-container').style.display = 'none';
});

// Cargar datos desde la API
async function cargarDatosGraficos(periodo) {
    const contenido = document.getElementById('graficos-contenido');
    contenido.innerHTML = `
        <div class="loading-grafico">
            <div class="spinner"></div>
            <p>Cargando datos...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/api/estadisticas?periodo=${periodo}`);
        const data = await response.json();
        datosActuales = data;
        mostrarGraficos(data);
    } catch (error) {
        console.error('Error:', error);
        contenido.innerHTML = `
            <div class="error-mensaje">
                ⚠️ Error al cargar los datos.<br>
                <small>Verifica tu conexión o recarga la página.</small>
            </div>
        `;
    }
}

// Mostrar gráficos con los datos
function mostrarGraficos(data) {
    const contenido = document.getElementById('graficos-contenido');
    
    contenido.innerHTML = `
        <div class="grafico-canvas-container">
            <canvas id="graficoPrincipal" width="500" height="400"></canvas>
        </div>
        <div class="estadisticas-grid">
            <div class="estadistica-card ingresos">
                <h6>💰 Ingresos</h6>
                <h3>$${data.total_ingresos.toFixed(2)}</h3>
            </div>
            <div class="estadistica-card gastos">
                <h6>💸 Gastos</h6>
                <h3>$${data.total_gastos.toFixed(2)}</h3>
            </div>
            <div class="estadistica-card balance">
                <h6>✅ Balance</h6>
                <h3>$${data.balance.toFixed(2)}</h3>
            </div>
        </div>
        <div class="text-center mt-3">
            <small class="text-muted">Período: ${data.periodo} | ${data.total_movimientos} movimientos</small>
        </div>
    `;
    
    const tipoGrafico = document.getElementById('tipo-grafico').value;
    dibujarGrafico(data, tipoGrafico);
}

// Dibujar gráfico según tipo
function dibujarGrafico(data, tipo) {
    const ctx = document.getElementById('graficoPrincipal').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    if (tipo === 'gastos') {
        const categorias = Object.keys(data.gastos_por_categoria || {});
        const valores = Object.values(data.gastos_por_categoria || {});
        
        if (categorias.length === 0) {
            mostrarMensajeSinDatos(ctx);
            return;
        }
        
        const colores = {
            'comida': '#FF6384', 'transporte': '#36A2EB', 'servicios': '#FFCE56',
            'alquiler': '#4BC0C0', 'entretenimiento': '#9966FF', 'salud': '#FF9F40',
            'educacion': '#66FF66', 'otros': '#C9CBCF'
        };
        
        const iconos = {
            'comida': '🍔', 'transporte': '🚗', 'servicios': '💡',
            'alquiler': '🏠', 'entretenimiento': '🎬', 'salud': '🏥',
            'educacion': '📚', 'otros': '📦'
        };
        
        chartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categorias.map(c => `${iconos[c] || '📦'} ${c.toUpperCase()}`),
                datasets: [{
                    data: valores,
                    backgroundColor: categorias.map(c => colores[c] || '#C9CBCF'),
                    borderWidth: 2,
                    borderColor: 'white'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom', labels: { font: { size: 10 } } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const porcentaje = ((context.raw / total) * 100).toFixed(1);
                                return `${context.label}: $${context.raw.toFixed(2)} (${porcentaje}%)`;
                            }
                        }
                    }
                }
            }
        });
        
    } else if (tipo === 'ingresos') {
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['💰 Ingresos', '💸 Gastos'],
                datasets: [{
                    data: [data.total_ingresos, data.total_gastos],
                    backgroundColor: ['#28a745', '#dc3545'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { callback: v => '$' + v.toFixed(2) } }
                }
            }
        });
        
    } else if (tipo === 'evolucion') {
        if (!data.meses || data.meses.length === 0) {
            mostrarMensajeSinDatos(ctx);
            return;
        }
        
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.meses,
                datasets: [
                    {
                        label: '💰 Ingresos',
                        data: data.ingresos_mensuales,
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40,167,69,0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: '💸 Gastos',
                        data: data.gastos_mensuales,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220,53,69,0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: { beginAtZero: true, ticks: { callback: v => '$' + v.toFixed(2) } }
                }
            }
        });
    }
}

function mostrarMensajeSinDatos(ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = '#666';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('No hay datos para mostrar', ctx.canvas.width / 2, ctx.canvas.height / 2);
}

// Eventos de filtros
document.querySelectorAll('.btn-filtro-grafico').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.btn-filtro-grafico').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        cargarDatosGraficos(this.dataset.periodo);
    });
});

document.getElementById('tipo-grafico')?.addEventListener('change', function() {
    if (datosActuales) {
        dibujarGrafico(datosActuales, this.value);
    }
});
