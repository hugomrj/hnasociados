


document.addEventListener('DOMContentLoaded', function() {


    var actividad_add = document.getElementById('actividad_add');
    if (actividad_add) {
        actividad_add.addEventListener('click', function() {
            
            var url = event.target.getAttribute('data-url');
            alert("La URL es: " + url);

        });
    }


});


