// static/js/permisos_dashboard.js
// Script para cargar datos del dashboard según permisos del usuario

// Variable global para almacenar permisos
let userPermisos = [];
let isAdmin = false;

// Inicializar el dashboard con los permisos del usuario
function initDashboard(permisos) {
    userPermisos = permisos;
    isAdmin = userPermisos.includes('admin_total');
    
    console.log('📊 Dashboard cargando con permisos:', userPermisos);
    
    // Cargar estadísticas
    cargarEstadisticas();
    
    // Cargar clientes solo si tiene permiso
    if (userPermisos.includes('ver_clientes') || isAdmin) {
        cargarUltimosClientes();
    }
    
    // Cargar citas solo si tiene permiso
    if (userPermisos.includes('ver_citas') || isAdmin) {
        cargarProximasCitas();
    }
}

// Función para cargar estadísticas
function cargarEstadisticas() {
    fetch('/api/dashboard-stats')
        .then(r => {
            if (!r.ok) throw new Error('Error en la respuesta del servidor');
            return r.json();
        })
        .then(data => {
            if (data.total_clientes && document.getElementById('total-clientes')) {
                document.getElementById('total-clientes').textContent = data.total_clientes;
            }
            if (data.total_cobranzas && document.getElementById('total-cobranzas')) {
                document.getElementById('total-cobranzas').textContent = `$${data.total_cobranzas}`;
            }
            if (data.total_pagos && document.getElementById('total-pagos')) {
                document.getElementById('total-pagos').textContent = `$${data.total_pagos}`;
            }
            if (data.total_citas && document.getElementById('total-citas')) {
                document.getElementById('total-citas').textContent = data.total_citas;
            }
        })
        .catch(error => console.error('❌ Error cargando estadísticas:', error));
}

// Función para cargar últimos clientes
function cargarUltimosClientes() {
    const puedeEditar = userPermisos.includes('editar_clientes') || isAdmin;
    
    const tbody = document.getElementById('ultimos-clientes');
    if (!tbody) return;
    
    tbody.innerHTML = '<td colspan="3"><i class="fas fa-spinner fa-spin"></i> Cargando clientes...</td>';
    
    fetch('/api/ultimos-clientes')
        .then(r => {
            if (!r.ok) throw new Error('Error en la respuesta');
            return r.json();
        })
        .then(clientes => {
            if (clientes.length === 0) {
                tbody.innerHTML = '<td colspan="3" style="text-align: center;">No hay clientes registrados</td>';
                return;
            }
            
            tbody.innerHTML = clientes.map(c => `
                
                    <td><strong>${escapeHtml(c.nombre)}</strong></td>
                    <td>${escapeHtml(c.email)}</td>
                    ${puedeEditar ? `
                    <td class="action-buttons">
                        <a href="/clientes/${c.id}/editar" class="btn-icon" title="Editar">
                            <i class="fas fa-edit"></i>
                        </a>
                     </td>
                    ` : ''}
                
            `).join('');
        })
        .catch(error => {
            console.error('❌ Error cargando clientes:', error);
            tbody.innerHTML = '<td colspan="3" style="text-align: center; color: #ef4444;">Error al cargar clientes</td>';
        });
}

// Función para cargar próximas citas
function cargarProximasCitas() {
    const puedeEditar = userPermisos.includes('editar_citas') || isAdmin;
    
    const tbody = document.getElementById('proximas-citas');
    if (!tbody) return;
    
    tbody.innerHTML = '<td colspan="4"><i class="fas fa-spinner fa-spin"></i> Cargando citas...</td>';
    
    fetch('/api/proximas-citas')
        .then(r => {
            if (!r.ok) throw new Error('Error en la respuesta');
            return r.json();
        })
        .then(citas => {
            if (citas.length === 0) {
                tbody.innerHTML = '<td colspan="4" style="text-align: center;">No hay citas programadas</td>';
                return;
            }
            
            tbody.innerHTML = citas.map(c => `
                
                    <td><strong>${escapeHtml(c.cliente_nombre)}</strong></td>
                    <td>${escapeHtml(c.fecha)}</td>
                    <td>${escapeHtml(c.hora)}</td>
                    ${puedeEditar ? `
                    <td class="action-buttons">
                        <a href="/citas/${c.id}/editar" class="btn-icon" title="Editar">
                            <i class="fas fa-edit"></i>
                        </a>
                     </td>
                    ` : ''}
                
            `).join('');
        })
        .catch(error => {
            console.error('❌ Error cargando citas:', error);
            tbody.innerHTML = '<td colspan="4" style="text-align: center; color: #ef4444;">Error al cargar citas</td>';
        });
}

// Función auxiliar para escapar HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Exportar función para uso global
window.initDashboard = initDashboard;