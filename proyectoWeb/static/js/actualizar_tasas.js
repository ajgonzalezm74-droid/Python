let ultimoBinance = null;

async function actualizarTasas() {
    try {
        const response = await fetch('/api/tasas');
        const data = await response.json();

        const binanceElement = document.getElementById('p2p_ves');
        const arrowElement = document.getElementById('p2p_arrow');

        const nuevoValor = parseFloat(data.p2p_ves);

        if (ultimoBinance !== null) {

            binanceElement.classList.remove("tasa-up", "tasa-down", "tasa-neutral");

            if (nuevoValor > ultimoBinance) {
                binanceElement.classList.add("tasa-up");
                arrowElement.innerHTML = "▲ ";
                arrowElement.style.color = "#00ff88";

            } else if (nuevoValor < ultimoBinance) {
                binanceElement.classList.add("tasa-down");
                arrowElement.innerHTML = "▼ ";
                arrowElement.style.color = "#ff4d4d";

            } else {
                binanceElement.classList.add("tasa-neutral");
                arrowElement.innerHTML = "— ";
                arrowElement.style.color = "#cccccc";
            }
        }

        binanceElement.innerText = nuevoValor;
        ultimoBinance = nuevoValor;

    } catch (error) {
        console.error("Error actualizando tasas:", error);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    actualizarTasas();
    setInterval(actualizarTasas, 300000);
});