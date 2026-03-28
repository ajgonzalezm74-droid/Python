// ========= ACORDEÓN: lógica toggle =========
const accordionItems = document.querySelectorAll('.accordion-item');

function toggleAccordion(item) {
  const isActive = item.classList.contains('active');
  // Cerrar todos
  accordionItems.forEach(i => i.classList.remove('active'));
  // Si no estaba activo, abrir el actual
  if (!isActive) {
    item.classList.add('active');
  }
}

accordionItems.forEach(item => {
  const header = item.querySelector('.accordion-header');
  
  header.addEventListener('click', (e) => {
    // SI EL CLIC FUE EN UN ENLACE CON UN HREF REAL, NO DETENERLO
    if (e.target.closest('a') && e.target.closest('a').getAttribute('href') !== '#') {
      return; // Permite que Flask cargue la vista
    }

    // SI NO ES UN LINK, ENTONCES SÍ PREVENIMOS Y HACEMOS EL TOGGLE
    e.preventDefault();
    toggleAccordion(item);
  });
});

// Abrir primer item por defecto
if (accordionItems.length > 0) {
  accordionItems[0].classList.add('active');
}
