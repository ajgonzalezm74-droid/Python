// ========= FORMULARIO DE CONTACTO CON ENVÍO REAL (FormSubmit.co) =========
  const contactForm = document.getElementById('accordionContactForm');
  const accSubmitBtn = document.getElementById('accSubmitBtn');
  const accFormStatus = document.getElementById('accFormStatus');
  
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('accName').value.trim();
    const email = document.getElementById('accEmail').value.trim();
    const phone = document.getElementById('accPhone').value.trim();
    const message = document.getElementById('accMessage').value.trim();
    
    if (!name || !email || !message) {
      accFormStatus.innerHTML = '<div class="error-message">⚠️ Por favor completa nombre, email y mensaje.</div>';
      return;
    }
    
    accSubmitBtn.disabled = true;
    accSubmitBtn.innerHTML = '<span class="loading-spinner"></span> Enviando...';
    accFormStatus.innerHTML = '';
    
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('message', message);
    formData.append('_subject', `Nuevo requerimiento desde AJG Solution - ${name}`);
    formData.append('_replyto', email);
    
    try {
      const response = await fetch('https://formsubmit.co/ajax/ajgonzalezm74@gmail.com', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      if (response.ok && result.success !== false) {
        accFormStatus.innerHTML = '<div class="success-message">✅ ¡Mensaje enviado con éxito! Te contactaremos pronto.</div>';
        contactForm.reset();
      } else {
        throw new Error('Error en el envío');
      }
    } catch (error) {
      accFormStatus.innerHTML = '<div class="error-message">❌ Error al enviar. Por favor intenta directamente al correo: ajgonzalezm74@gmail.com</div>';
    } finally {
      accSubmitBtn.disabled = false;
      accSubmitBtn.innerHTML = 'Enviar mensaje →';
      setTimeout(() => { if (accFormStatus.innerHTML) accFormStatus.innerHTML = ''; }, 5000);
    }
  });