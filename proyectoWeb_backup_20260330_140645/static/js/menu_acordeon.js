// Función para abrir un item del acordeón
  function openAccordionItem(targetId) {
    const targetItem = document.querySelector(`.accordion-item[data-accordion="${targetId}"]`);
    if (targetItem) {
      const content = targetItem.querySelector('.accordion-content');
      const icon = targetItem.querySelector('.accordion-icon');
      const allContents = document.querySelectorAll('.accordion-content');
      const allIcons = document.querySelectorAll('.accordion-icon');
      
      // Cerrar todos
      allContents.forEach(c => {
        if (c !== content) {
          c.style.display = 'none';
        }
      });
      allIcons.forEach(i => {
        if (i !== icon) {
          i.style.transform = 'rotate(0deg)';
        }
      });
      
      // Abrir el seleccionado
      if (content.style.display === 'none' || !content.style.display) {
        content.style.display = 'block';
        if (icon) icon.style.transform = 'rotate(180deg)';
        // Scroll al item
        targetItem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        content.style.display = 'none';
        if (icon) icon.style.transform = 'rotate(0deg)';
      }
    }
  }

  // Event listeners para los enlaces del menú
  document.querySelectorAll('[data-accordion-target]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.getAttribute('data-accordion-target');
      openAccordionItem(target);
    });
  });

  // Event listeners para los botones del hero
  const exploreBtn = document.getElementById('exploreBtn');
  const contactBtn = document.getElementById('contactBtnAcordeon');
  
  if (exploreBtn) {
    exploreBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openAccordionItem('consulta');
    });
  }
  
  if (contactBtn) {
    contactBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openAccordionItem('contacto');
    });
  }