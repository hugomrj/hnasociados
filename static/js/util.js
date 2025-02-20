// Función para formatear los números con separadores de miles
function formatearNumeros() {
    // Selecciona todos los inputs con el atributo data-number="int"
    const inputs = document.querySelectorAll('input[data-number="int"]');

    inputs.forEach(input => {
        // Función para formatear el valor del input
        const formatearInput = (event) => {
            const input = event.target;
            
            // Primero, elimina todos los puntos y luego convierte el valor a número
            let valor = input.value.replace(/\./g, '');  // Elimina los puntos
            valor = parseFloat(valor.replace(/,/g, '')); // Elimina comas y convierte a número
            
            if (!isNaN(valor)) {
                // Aplica el formato con separadores de miles
                input.value = valor.toLocaleString();
            }
        };

        // Formatea el valor inicial del input
        let valorInicial = input.value.replace(/\./g, ''); // Elimina puntos
        valorInicial = parseFloat(valorInicial.replace(/,/g, '')); // Elimina comas y convierte a número
        
        if (!isNaN(valorInicial)) {
            input.value = valorInicial.toLocaleString();
        }

        // Asocia la función formatearInput al evento blur del input actual
        input.addEventListener('blur', formatearInput);
    });
}







// Función para quitar el formato y volver al número original
function quitarFormato() {
    const inputs = document.querySelectorAll('input[data-number="int"]');
    inputs.forEach(input => {
        let valor = input.value.replace(/,/g, '');
        if (!isNaN(valor)) {
            input.value = valor;
        }
    });
}




function bloquearInput() {

    var inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(function(input) {
        input.disabled = true;
    });
    

}









