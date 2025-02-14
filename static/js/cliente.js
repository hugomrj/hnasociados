


document.addEventListener('DOMContentLoaded', function() {


    var add = document.getElementById('registro_add');
    if (add) {
        add.addEventListener('click', function() {
            
            var form = document.getElementById('form');
            var url = form.action ;

            // Enviar el formulario
            form.submit();                 

        });
    }




    var edit = document.getElementById('registro_edit');
    if (edit) {
        edit.addEventListener('click', function() {
            
            var form = document.getElementById('form');
            // Enviar el formulario
            form.submit();                 

        });
    }





    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); 
            let itemId = this.getAttribute("data-item-id");
            let deleteUrl = this.getAttribute("data-delete-url");
            
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


