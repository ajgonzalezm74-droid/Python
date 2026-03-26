// static/js/script.js
// JavaScript para la página de login y administración de usuarios

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';

    // Función para eliminar usuario (se define globalmente para ser llamada desde onclick)
    window.eliminarUsuario = function(id) {
        if (confirm('¿Estás seguro de eliminar este usuario?')) {
            fetch(`/admin/usuarios/${id}/eliminar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || data.error);
                if (!data.error) location.reload();
            });
        }
    };

    // Función para mostrar/ocultar contraseña
    window.togglePassword = function() {
        const passwordInput = document.getElementById('password');
        const toggleIcon = document.getElementById('toggleIcon');
        
        if (passwordInput && toggleIcon) {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye');
            }
        }
    };

    // Función para autocompletar credenciales de demo
    window.fillDemoCredentials = function() {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        
        if (usernameInput) usernameInput.value = 'admin@mail.com';
        if (passwordInput) passwordInput.value = 'User2024';
        
        // Animación sutil
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.style.backgroundColor = '#e8f5e9';
            setTimeout(() => {
                input.style.backgroundColor = '';
            }, 500);
        });
    };

    // Función para mostrar errores
    window.showError = function(message) {
        if (errorMessage) errorMessage.textContent = message;
        if (errorModal) errorModal.classList.add('active');
        
        // Animar los inputs con error
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.classList.add('error-shake');
            setTimeout(() => {
                input.classList.remove('error-shake');
            }, 500);
        });
    };

    // Función para cerrar modal
    window.closeModal = function() {
        if (errorModal) errorModal.classList.remove('active');
    };

    // Mostrar modal de error si hay parámetro en URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('error')) {
        showError(urlParams.get('error'));
    }

    // Cerrar modal con tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && errorModal && errorModal.classList.contains('active')) {
            closeModal();
        }
    });

    // Cerrar modal al hacer clic fuera
    if (errorModal) {
        errorModal.addEventListener('click', function(e) {
            if (e.target === errorModal) {
                closeModal();
            }
        });
    }

    // Mostrar/ocultar loading al enviar formulario
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (!username || !password || !username.value || !password.value) {
                e.preventDefault();
                showError('Por favor, completa todos los campos');
                return;
            }

            if (loginBtn) {
                loginBtn.classList.add('loading');
                loginBtn.disabled = true;
            }
        });
    }

    // Validación en tiempo real
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.style.borderColor = '';
            const formGroup = this.closest('.form-group');
            if (formGroup) {
                const errorMsg = formGroup.querySelector('.error-message');
                if (errorMsg) {
                    errorMsg.remove();
                }
            }
        });
    });

    // Animación para mensajes flash
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Menú móvil toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            if (sidebar) sidebar.classList.toggle('open');
            if (sidebar) sidebar.classList.toggle('collapsed');
            if (mainContent) mainContent.classList.toggle('expanded');
            
            // Cambiar ícono
            const icon = menuToggle.querySelector('i');
            if (icon) {
                if (sidebar && sidebar.classList.contains('open')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
    
    // Cerrar menú al hacer clic en un enlace (móvil)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('open');
                if (mainContent) mainContent.classList.remove('expanded');
                const icon = menuToggle?.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });
    
    // Ajustar al cambiar tamaño de ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && sidebar) {
            sidebar.classList.remove('open');
            sidebar.classList.remove('collapsed');
            if (mainContent) mainContent.classList.remove('expanded');
        }
    });
});