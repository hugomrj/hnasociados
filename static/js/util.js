// Función para formatear los números con separadores de miles
function formatearNumeros() {
    const inputs = document.querySelectorAll('input[data-number="int"]');

    inputs.forEach(input => {
        const formatearInput = (event) => {
            const input = event.target;
            let valor = input.value.replace(/\D/g, '');  // Solo deja dígitos

            if (valor) {
                input.value = parseInt(valor).toLocaleString('de-DE');
            } else {
                input.value = '';
            }
        };

        // Formateo inicial
        let valorInicial = input.value.replace(/\D/g, '');
        if (valorInicial) {
            input.value = parseInt(valorInicial).toLocaleString('de-DE');
        }

        input.addEventListener('blur', formatearInput);
    });
}







// Función para quitar el formato y volver al número original
function quitarFormato() {
    const inputs = document.querySelectorAll('input[data-number="int"]');
    inputs.forEach(input => {
        console.log('Antes:', input.value);
        let valor = input.value.replace(/\./g, '');  // quita puntos
        if (!isNaN(valor)) {
            input.value = valor;
            console.log('Después:', input.value);
        }
    });
}






function bloquearInput() {

    var inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(function(input) {
        input.disabled = true;
    });
    

}












