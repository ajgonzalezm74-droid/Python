// static/js/dashboard.js
// Módulo para el dashboard - VERSIÓN LIMPIA

console.log('📊 dashboard.js cargado');

// Usar una sola variable global con nombre único
window.dashboardData = {
    permisos: [],
    isAdmin: false
};

// Función para cargar estadísticas
function cargarEstadisticas() {
    console.log('📊 Cargando estadísticas...');
    fetch('/api/dashboard-stats')
        .then(r => {
            if (!r.ok) throw new Error('Error en la respuesta');
            return r.json();
        })
        .then(data => {
            console.log('📊 Estadísticas:', data);
            
            const totalClientes = document.getElementById('total-clientes');
            if (totalClientes) totalClientes.textContent = data.total_clientes || 0;
            
            const totalCobranzas = document.getElementById('total-cobranzas');
            if (totalCobranzas) totalCobranzas.textContent = `$${data.total_cobranzas || 0}`;
            
            const totalPagos = document.getElementById('total-pagos');
            if (totalPagos) totalPagos.textContent = `$${data.total_pagos || 0}`;
            
            const totalCitas = document.getElementById('total-citas');
            if (totalCitas) totalCitas.textContent = data.total_citas || 0;
        })
        .catch(error => console.error('❌ Error estadísticas:', error));
}

// Función para cargar clientes
function cargarClientes() {
    console.log('👥 Cargando clientes...');
    fetch('/api/ultimos-clientes')
        .then(r => r.json())
        .then(clientes => {
            console.log('👥 Clientes:', clientes);
            const tbody = document.getElementById('ultimos-clientes');
            if (!tbody) return;
            
            if (clientes.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3">No hay clientes registrados</td></tr>';
                return;
            }
            
            const puedeEditar = window.dashboardData.permisos.includes('editar_clientes') || window.dashboardData.isAdmin;
            
            tbody.innerHTML = clientes.map(c => `
                <tr>
                    <td><strong>${c.nombre} ${c.apellidos || ''}</strong></td>
                    <td>${c.email || '---'}</td>
                    <td>${c.telefono || '---'}</td>
                    ${puedeEditar ? `<td><a href="/clientes/${c.id}/editar" class="btn-icon"><i class="fas fa-edit"></i></a></td>` : ''}
                </tr>
            `).join('');
        })
        .catch(error => console.error('❌ Error clientes:', error));
}

// Función para cargar citas
function cargarCitas() {
    fetch('/api/proximas-citas')
        .then(r => r.json())
        .then(citas => {
            const tbody = document.getElementById('proximas-citas');
            if (!tbody) return;
            
            if (citas.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">No hay citas programadas</td></tr>';
                return;
            }
            
            const puedeEditar = window.dashboardData.permisos.includes('editar_citas') || window.dashboardData.isAdmin;
            
            tbody.innerHTML = citas.map(c => `
                <tr>
                    <td><strong>${c.cliente_nombre}</strong></td>
                    <td>${c.fecha}</td>
                    <td>${c.hora}</td>
                    ${puedeEditar ? `<td><a href="/citas/${c.id}/editar" class="btn-icon"><i class="fas fa-edit"></i></a></td>` : ''}
                </tr>
            `).join('');
        })
        .catch(error => console.error('Error citas:', error));
}

// Función principal
window.initDashboard = function(permisos) {
    console.log('📊 Inicializando dashboard...');
    window.dashboardData.permisos = permisos || [];
    window.dashboardData.isAdmin = window.dashboardData.permisos.includes('admin_total');
    
    cargarEstadisticas();
    
    if (window.dashboardData.permisos.includes('ver_clientes') || window.dashboardData.isAdmin) {
        cargarClientes();
    }
    
    if (window.dashboardData.permisos.includes('ver_citas') || window.dashboardData.isAdmin) {
        cargarCitas();
    }
};

console.log('✅ dashboard.js listo');