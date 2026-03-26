// static/js/clientes.js
// Módulo de gestión de clientes

class ClientesModule {
    constructor() {
        this.currentPage = 1;
        this.rowsPerPage = 10;
        this.searchInput = null;
        this.statusFilter = null;
        this.init();
    }
    
    init() {
        console.log('📋 Inicializando módulo de clientes...');
        
        // Configurar filtros
        this.searchInput = document.getElementById('searchInput');
        this.statusFilter = document.getElementById('statusFilter');
        
        if (this.searchInput) {
            this.searchInput.addEventListener('keyup', () => this.filtrarTabla());
        }
        
        if (this.statusFilter) {
            this.statusFilter.addEventListener('change', () => this.filtrarTabla());
        }
        
        // Configurar exportación
        const btnExportar = document.getElementById('btnExportar');
        if (btnExportar) {
            btnExportar.addEventListener('click', () => this.exportarClientes());
        }
        
        // Inicializar paginación
        this.actualizarPaginacion();
        this.crearContador();
        
        // Configurar modal
        this.configurarModal();
    }
    
    filtrarTabla() {
        const searchTerm = this.searchInput ? this.searchInput.value.toLowerCase() : '';
        const statusFilter = this.statusFilter ? this.statusFilter.value : 'todos';
        const rows = document.querySelectorAll('#tabla-clientes tbody tr');
        let visibleCount = 0;
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const estado = row.dataset.estado;
            
            let show = true;
            if (searchTerm && !text.includes(searchTerm)) show = false;
            if (statusFilter !== 'todos' && estado !== statusFilter) show = false;
            
            row.style.display = show ? '' : 'none';
            if (show) visibleCount++;
        });
        
        // Actualizar contador
        this.actualizarContador(visibleCount, rows.length);
        
        // Resetear paginación
        this.currentPage = 1;
        this.actualizarPaginacion();
    }
    
    actualizarPaginacion() {
        const rows = document.querySelectorAll('#tabla-clientes tbody tr:not([style*="display: none"])');
        const totalPages = Math.ceil(rows.length / this.rowsPerPage);
        const paginationDiv = document.getElementById('pagination');
        
        if (!paginationDiv) return;
        
        if (totalPages <= 1) {
            paginationDiv.innerHTML = '';
            this.mostrarFilasPagina(rows);
            return;
        }
        
        let html = '<div class="pagination-controls">';
        
        // Botón anterior
        html += `<button class="page-link" onclick="clientesModule.cambiarPagina(${this.currentPage - 1})" ${this.currentPage === 1 ? 'disabled' : ''}>&laquo;</button>`;
        
        // Números de página
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            html += `<button class="page-link ${i === this.currentPage ? 'active' : ''}" onclick="clientesModule.cambiarPagina(${i})">${i}</button>`;
        }
        
        // Botón siguiente
        html += `<button class="page-link" onclick="clientesModule.cambiarPagina(${this.currentPage + 1})" ${this.currentPage === totalPages ? 'disabled' : ''}>&raquo;</button>`;
        html += '</div>';
        
        paginationDiv.innerHTML = html;
        this.mostrarFilasPagina(rows);
    }
    
    mostrarFilasPagina(rows) {
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;
        
        rows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? '' : 'none';
        });
    }
    
    cambiarPagina(page) {
        if (page < 1) return;
        this.currentPage = page;
        this.actualizarPaginacion();
    }
    
    crearContador() {
        const container = document.querySelector('.table-container');
        if (container && !document.getElementById('registros-counter')) {
            const counter = document.createElement('div');
            counter.id = 'registros-counter';
            counter.className = 'registros-counter';
            container.appendChild(counter);
        }
    }
    
    actualizarContador(visibles, total) {
        const counter = document.getElementById('registros-counter');
        if (counter) {
            counter.innerHTML = `<i class="fas fa-chart-line"></i> Mostrando ${visibles} de ${total} clientes`;
        }
    }
    
    configurarModal() {
        const modal = document.getElementById('clienteModal');
        const closeBtn = modal ? modal.querySelector('.close-btn') : null;
        
        if (closeBtn) {
            closeBtn.onclick = () => this.cerrarModal();
        }
        
        // Cerrar al hacer clic fuera del contenido
        window.onclick = (event) => {
            if (event.target === modal) {
                this.cerrarModal();
            }
        };
    }
    
    verCliente(id) {
        fetch(`/clientes/${id}/detalles`)
            .then(r => r.json())
            .then(data => {
                const modalBody = document.getElementById('detallesCliente');
                if (modalBody) {
                    modalBody.innerHTML = this.generarHTMLDetalles(data);
                }
                document.getElementById('clienteModal').classList.add('active');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al cargar detalles del cliente');
            });
    }
    
    generarHTMLDetalles(data) {
        return `
            <div style="grid-column: span 2; background: #f8fafc; padding: 1rem; border-radius: 8px;">
                <strong>Nombre Completo:</strong> ${this.escapeHtml(data.nombre)} ${this.escapeHtml(data.apellidos)}
            </div>
            <div><strong>Documento:</strong> ${data.tipo_documento || 'V'}-${data.id_documento || '---'}</div>
            <div><strong>RIF:</strong> ${this.escapeHtml(data.rif) || '---'}</div>
            <div><strong>Email:</strong> ${this.escapeHtml(data.email) || '---'}</div>
            <div><strong>Teléfono:</strong> ${this.escapeHtml(data.telefono) || '---'}</div>
            <div><strong>Teléfono Alternativo:</strong> ${this.escapeHtml(data.telefono_alternativo) || '---'}</div>
            <div><strong>Dirección:</strong> ${this.escapeHtml(data.direccion) || '---'}</div>
            <div><strong>Ciudad:</strong> ${this.escapeHtml(data.ciudad) || '---'}</div>
            <div><strong>Estado:</strong> ${this.escapeHtml(data.estado) || '---'}</div>
            <div><strong>País:</strong> ${this.escapeHtml(data.pais) || '---'}</div>
            <div><strong>Compañía:</strong> ${this.escapeHtml(data.nombre_compania) || '---'}</div>
            <div><strong>Cargo:</strong> ${this.escapeHtml(data.cargo) || '---'}</div>
            <div><strong>Departamento:</strong> ${this.escapeHtml(data.departamento) || '---'}</div>
            <div style="grid-column: span 2;"><strong>Notas:</strong> ${this.escapeHtml(data.notas) || '---'}</div>
            <div><strong>Creado por:</strong> ${this.escapeHtml(data.creado_por) || 'Sistema'}</div>
            <div><strong>Fecha Creación:</strong> ${data.fecha_creacion || '---'}</div>
            <div><strong>Estado:</strong> <span class="status-badge ${data.activo ? 'active' : 'inactive'}">${data.activo ? 'Activo' : 'Inactivo'}</span></div>
        `;
    }
    
    eliminarCliente(id) {
        if (!confirm('¿Estás seguro de eliminar este cliente?')) return;
        
        fetch(`/clientes/${id}/eliminar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            }
        })
        .then(r => r.json())
        .then(data => {
            alert(data.message || 'Cliente eliminado');
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar cliente');
        });
    }
    
    activarCliente(id) {
        if (!confirm('¿Activar este cliente?')) return;
        
        fetch(`/clientes/${id}/activar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            }
        })
        .then(r => r.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
    }
    
    exportarClientes() {
        const rows = document.querySelectorAll('#tabla-clientes tbody tr:not([style*="display: none"])');
        let csvContent = "ID,Documento,Nombre,Email,Teléfono,Compañía,Estado,Fecha Creación\n";
        
        rows.forEach(row => {
            const cols = row.querySelectorAll('td');
            if (cols.length >= 7) {
                const id = cols[0].innerText;
                const documento = cols[1].innerText;
                const nombre = cols[2].innerText.replace(/<br.*?>.*$/s, '').trim();
                const email = cols[3].innerText.replace(/<.*?>/, '').trim();
                const telefono = cols[4].innerText.split('\n')[0].replace(/<.*?>/, '').trim();
                const compania = cols[5].innerText;
                const estado = cols[6].innerText;
                const fecha = cols[7].innerText;
                
                csvContent += `"${id}","${documento}","${nombre}","${email}","${telefono}","${compania}","${estado}","${fecha}"\n`;
            }
        });
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `clientes_${new Date().toISOString().slice(0,19)}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    cerrarModal() {
        document.getElementById('clienteModal').classList.remove('active');
    }
    
    getCsrfToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar cuando el DOM esté listo
let clientesModule = null;

document.addEventListener('DOMContentLoaded', function() {
    clientesModule = new ClientesModule();
});

// Exportar funciones globales para usar desde HTML onclick
window.verCliente = (id) => clientesModule?.verCliente(id);
window.eliminarCliente = (id) => clientesModule?.eliminarCliente(id);
window.activarCliente = (id) => clientesModule?.activarCliente(id);