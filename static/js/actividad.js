


document.addEventListener('DOMContentLoaded', function() {


    var actividad_add = document.getElementById('actividad_add');
    if (actividad_add) {
        actividad_add.addEventListener('click', function() {
            
            var form = document.getElementById('form');
            var url = form.action ;

            // Enviar el formulario
            form.submit();                 

        });
    }


    var actividad_edit = document.getElementById('actividad_edit');
    if (actividad_edit) {
        actividad_edit.addEventListener('click', function() {
            
            var form = document.getElementById('form');
            // Enviar el formulario
            form.submit();                 
          

        });
    }




});


