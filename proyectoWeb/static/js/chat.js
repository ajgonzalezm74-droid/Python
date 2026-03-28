function toggleChat() {
    const chat = document.getElementById('chat-window');
    if (chat.style.getPropertyValue('display') === 'none' || chat.style.display === 'none') {
        chat.style.setProperty('display', 'flex', 'important');
    } else {
        chat.style.setProperty('display', 'none', 'important');
    }
}

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('btn-enviar-chat')
        .addEventListener('click', enviarPregunta);

    document.getElementById('user-input')
        .addEventListener('keypress', (e) => { 
            if(e.key === 'Enter') enviarPregunta(); 
        });

});

async function enviarPregunta() {
    const input = document.getElementById('user-input');
    const body = document.getElementById('chat-body');
    const pregunta = input.value.trim();

    if (!pregunta) return;

    body.innerHTML += `<p class="text-end"><strong>Tú:</strong> ${pregunta}</p>`;
    input.value = '';
    
    const loading = document.createElement('p');
    loading.className = "text-warning";
    loading.innerHTML = "<i>IA pensando...</i>";
    body.appendChild(loading);
    body.scrollTop = body.scrollHeight;

    try {
        const response = await fetch('/chat', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: pregunta })
        });
        const data = await response.json();
        loading.remove();
        body.innerHTML += `<div class="bg-secondary p-2 rounded mb-2"><strong>IA:</strong> ${data.respuesta}</div>`;
    } catch (e) {
        loading.innerText = "Error: Verifica la API Key.";
    }
    body.scrollTop = body.scrollHeight;
}
