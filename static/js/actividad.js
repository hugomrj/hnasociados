


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




    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Evita que el enlace navegue
            let itemId = this.getAttribute("data-item-id");
            let deleteUrl = this.getAttribute("data-delete-url");
            
            // Actualiza el contenido del modal con el ID del registro
            //document.getElementById('itemIdPlaceholder').textContent = itemId;
            
            // Inicializa el modal y lo muestra
            const modal = new mdb.Modal(document.getElementById('itemModal'));
            modal.show();

            document.getElementById('confirmarEliminarRegistro').onclick = function () {
                //alert(itemId);
                var form = document.getElementById('form_delete');                                
                form.action = deleteUrl;

            };
        });
    });




});


