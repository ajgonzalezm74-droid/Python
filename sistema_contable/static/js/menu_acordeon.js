// static/js/menu_acordeon.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Inicializando menú acordeón...');
    
    // Función para expandir/colapsar submenú
    function toggleSubmenu(parentLink) {
        const parentLi = parentLink.closest('.has-children');
        if (!parentLi) {
            console.log('❌ No se encontró .has-children');
            return;
        }
        
        const submenu = parentLi.querySelector('.sub-menu');
        const arrow = parentLink.querySelector('.arrow');
        
        if (!submenu) {
            console.log('❌ No se encontró .sub-menu');
            return;
        }
        
        // Verificar estado actual
        const isOpen = submenu.classList.contains('open') || submenu.style.display === 'block';
        
        if (isOpen) {
            // Cerrar
            submenu.classList.remove('open');
            submenu.style.display = 'none';
            if (arrow) arrow.style.transform = 'rotate(0deg)';
            console.log('📁 Cerrando menú');
        } else {
            // Abrir
            submenu.classList.add('open');
            submenu.style.display = 'block';
            if (arrow) arrow.style.transform = 'rotate(180deg)';
            console.log('📂 Abriendo menú');
        }
    }
    
    // Obtener todos los enlaces padres
    const menuParents = document.querySelectorAll('.nav-link.parent');
    console.log('📋 Menús padres encontrados:', menuParents.length);
    
    if (menuParents.length === 0) {
        console.log('⚠️ No se encontraron menús con clase "parent"');
        return;
    }
    
    // Asignar eventos a cada menú padre
    menuParents.forEach((parent, index) => {
        console.log(`  ${index + 1}. ${parent.querySelector('span')?.innerText || 'sin nombre'}`);
        
        // Eliminar event listener previo si existe
        parent.removeEventListener('click', window.handleMenuClick);
        
        // Crear y asignar nuevo event listener
        const handleClick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('🖱️ Click en:', this.querySelector('span')?.innerText);
            toggleSubmenu(this);
        };
        
        parent.addEventListener('click', handleClick);
        
        // Guardar referencia para debug
        parent._handleClick = handleClick;
    });
    
    // Inicializar menús que deberían estar abiertos (ej: página actual)
    function initOpenMenus() {
        const currentUrl = window.location.pathname;
        document.querySelectorAll('.sub-menu .nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href && (href === currentUrl || currentUrl.includes(href))) {
                const parentLi = link.closest('.has-children');
                if (parentLi) {
                    const parentLink = parentLi.querySelector('.nav-link.parent');
                    if (parentLink && !parentLink.classList.contains('open')) {
                        toggleSubmenu(parentLink);
                    }
                }
            }
        });
    }
    
    initOpenMenus();
    
    console.log('✅ Menú acordeón inicializado correctamente');
});