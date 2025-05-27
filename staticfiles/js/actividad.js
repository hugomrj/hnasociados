


document.addEventListener('DOMContentLoaded', function() {


    var obligacion_add = document.getElementById('obligacion_add');
    if (obligacion_add) {
        obligacion_add.addEventListener('click', function() {
            
            var form = document.getElementById('form');
            var url = form.action ;

            // Enviar el formulario
            form.submit();                 

        });
    }




    var obligacion_edit = document.getElementById('obligacion_edit');
    if (obligacion_edit) {
        obligacion_edit.addEventListener('click', function() {
            
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


