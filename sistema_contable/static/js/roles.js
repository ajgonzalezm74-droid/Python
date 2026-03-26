// Cargar permisos disponibles
let todosPermisos = [];

async function cargarPermisos() {
    const response = await fetch('/admin/permisos/todos');
    todosPermisos = await response.json();
    return todosPermisos;
}

// Mostrar formulario para nuevo rol
document.getElementById('btnNuevoRol').onclick = async function() {
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Nuevo Rol';
    document.getElementById('rolId').value = '';
    document.getElementById('rolNombre').value = '';
    document.getElementById('rolDescripcion').value = '';
    
    if (todosPermisos.length === 0) {
        await cargarPermisos();
    }
    
    mostrarPermisosSeleccionables([]);
    document.getElementById('rolModal').classList.add('active');
}

// Editar rol
window.editarRol = async function(id) {
    const response = await fetch(`/admin/roles/${id}`);
    const rol = await response.json();
    
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Editar Rol';
    document.getElementById('rolId').value = rol.id_rol;
    document.getElementById('rolNombre').value = rol.nombre;
    document.getElementById('rolDescripcion').value = rol.descripcion;
    
    if (todosPermisos.length === 0) {
        await cargarPermisos();
    }
    
    mostrarPermisosSeleccionables(rol.permisos);
    document.getElementById('rolModal').classList.add('active');
}

// Mostrar permisos seleccionables
function mostrarPermisosSeleccionables(permisosSeleccionados) {
    const container = document.getElementById('permisosContainer');
    const permisosPorModulo = {};
    
    todosPermisos.forEach(p => {
        if (!permisosPorModulo[p.modulo]) permisosPorModulo[p.modulo] = [];
        permisosPorModulo[p.modulo].push(p);
    });
    
    let html = '';
    for (const [modulo, permisos] of Object.entries(permisosPorModulo)) {
        html += `<div style="margin-bottom: 1rem; padding: 0.5rem; background: #f8fafc; border-radius: 8px;">
                    <h4 style="margin-bottom: 0.5rem; color: var(--primary-color);">${modulo.toUpperCase()}</h4>`;
        for (const p of permisos) {
            const checked = permisosSeleccionados.includes(p.id_permiso) || 
                           (permisosSeleccionados.some && permisosSeleccionados.some(ps => ps.id_permiso === p.id_permiso));
            html += `<label style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                        <input type="checkbox" name="permisos" value="${p.id_permiso}" ${checked ? 'checked' : ''}>
                        <span><strong>${p.nombre}</strong> - ${p.descripcion}</span>
                    </label>`;
        }
        html += `</div>`;
    }
    container.innerHTML = html;
}

// Guardar rol
window.guardarRol = async function() {
    const id = document.getElementById('rolId').value;
    const nombre = document.getElementById('rolNombre').value;
    const descripcion = document.getElementById('rolDescripcion').value;
    const permisos = Array.from(document.querySelectorAll('input[name="permisos"]:checked')).map(cb => cb.value);
    
    const data = { nombre, descripcion, permisos };
    const url = id ? `/admin/roles/${id}/editar` : '/admin/roles/nuevo';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    if (result.success) {
        alert(result.message);
        cerrarModal();
        location.reload();
    } else {
        alert('Error: ' + result.message);
    }
}

// Ver permisos de un rol
window.verPermisos = async function(id) {
    const response = await fetch(`/admin/roles/${id}/permisos`);
    const permisos = await response.json();
    
    const porModulo = {};
    permisos.forEach(p => {
        if (!porModulo[p.modulo]) porModulo[p.modulo] = [];
        porModulo[p.modulo].push(p);
    });
    
    let html = '';
    for (const [modulo, lista] of Object.entries(porModulo)) {
        html += `<h4 style="margin: 1rem 0 0.5rem; color: var(--primary-color);">${modulo.toUpperCase()}</h4>
                 <ul style="list-style: none;">`;
        lista.forEach(p => {
            html += `<li><i class="fas fa-check-circle" style="color: #10b981;"></i> ${p.nombre}</li>`;
        });
        html += `</ul>`;
    }
    
    document.getElementById('listaPermisos').innerHTML = html || '<p>No tiene permisos asignados</p>';
    document.getElementById('permisosModal').classList.add('active');
}

// Ver usuarios de un rol
window.verUsuarios = async function(id) {
    const response = await fetch(`/admin/roles/${id}/usuarios`);
    const usuarios = await response.json();
    
    if (usuarios.length === 0) {
        document.getElementById('listaUsuarios').innerHTML = '<p>No hay usuarios con este rol</p>';
    } else {
        let html = '<ul style="list-style: none;">';
        usuarios.forEach(u => {
            html += `<li style="padding: 0.5rem; border-bottom: 1px solid var(--border-color);">
                        <i class="fas fa-user-circle"></i> 
                        <strong>${u.nombre}</strong> (@${u.username})<br>
                        <small>${u.email}</small>
                    </li>`;
        });
        html += '</ul>';
        document.getElementById('listaUsuarios').innerHTML = html;
    }
    document.getElementById('usuariosModal').classList.add('active');
}

// Eliminar rol
window.eliminarRol = async function(id) {
    if (!confirm('¿Estás seguro de eliminar este rol?')) return;
    
    const response = await fetch(`/admin/roles/${id}/eliminar`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': '{{ csrf_token }}'}
    });
    
    const result = await response.json();
    if (result.success) {
        alert(result.message);
        location.reload();
    } else {
        alert('Error: ' + result.message);
    }
}

function cerrarModal() {
    document.getElementById('rolModal').classList.remove('active');
}

function cerrarPermisosModal() {
    document.getElementById('permisosModal').classList.remove('active');
}

function cerrarUsuariosModal() {
    document.getElementById('usuariosModal').classList.remove('active');
}

// Cargar permisos al inicio
cargarPermisos();
