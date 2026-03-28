function toggleAccordion(element) {
            const content = element.nextElementSibling;
            
            // Cerrar otros acordeones (opcional)
            document.querySelectorAll('.accordion-content').forEach(item => {
                if (item !== content) {
                    item.style.maxHeight = null;
                }
            });

            // Abrir o cerrar el actual
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        }