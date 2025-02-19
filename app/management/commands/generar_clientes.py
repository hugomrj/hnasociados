import random
from django.core.management.base import BaseCommand
from app.models.cliente_views_model import Cliente


class Command(BaseCommand):
    help = "Genera registros aleatorios en la tabla Cliente"

    def add_arguments(self, parser):
        parser.add_argument('cantidad', type=int, help='Cantidad de registros a generar')

    def handle(self, *args, **kwargs):
        cantidad_registros = kwargs['cantidad']

        nombres = [
            'Juan', 'Maria', 'Pedro', 'Ana', 'Luis', 'Laura', 'Carlos', 'Sofia', 'Diego', 'Valentina',
            'Fernando', 'Camila', 'Ricardo', 'Martina', 'Sebastian', 'Lucia', 'Gabriel', 'Paula', 'Javier', 'Julieta',
            'Roberto', 'Andrea', 'Hugo', 'Victoria', 'Manuel', 'Elena', 'Daniel', 'Florencia', 'Alejandro', 'Carolina',
            'Eduardo', 'Isabel', 'Martín', 'Belen', 'Francisco', 'Diana', 'Agustin', 'Rocio', 'Emiliano', 'Milagros',
            'Nicolas', 'Cecilia', 'Gustavo', 'Lorena', 'Mariano', 'Estefania', 'Leonardo', 'Gisela', 'Federico', 'Noelia',
            'Rodrigo', 'Antonella', 'Marcos', 'Jimena', 'Christian', 'Patricia', 'Raul', 'Silvana', 'Ezequiel', 'Nadia',
            'Victor', 'Melina', 'Axel', 'Romina', 'Cristian', 'Daniela', 'Ramiro', 'Giuliana', 'Fabián', 'Tamara',
            'Bruno', 'Valeria', 'Enzo', 'Micaela', 'Adrian', 'Pilar', 'Facundo', 'Mara', 'Lucas', 'Evelyn',
            'Santiago', 'Bianca', 'Joaquin', 'Marina', 'Kevin', 'Celeste', 'Ivan', 'Magdalena', 'Maximiliano', 'Sara',
            'Joel', 'Tatiana', 'Dario', 'Violeta', 'Oscar', 'Genoveva', 'Ruben', 'Beatriz', 'Matias', 'Veronica'
        ]

        apellidos = [
            'Gomez', 'Perez', 'Gonzalez', 'Rodriguez', 'Lopez', 'Martinez', 'Fernandez', 'Diaz', 'Sanchez', 'Romero',
            'Torres', 'Ramirez', 'Flores', 'Benitez', 'Acosta', 'Medina', 'Herrera', 'Jimenez', 'Ortega', 'Silva',
            'Castro', 'Mendoza', 'Rojas', 'Navarro', 'Guerrero', 'Vargas', 'Delgado', 'Cabrera', 'Morales', 'Paredes',
            'Figueroa', 'Salazar', 'Peralta', 'Dominguez', 'Coronel', 'Britez', 'Galeano', 'Vera', 'Franco', 'Cantero',
            'Zarate', 'Lezcano', 'Alonso', 'Ojeda', 'Cardozo', 'Pavon', 'Barrios', 'Ayala', 'Caceres', 'Centurion',
            'Frutos', 'Leguizamon', 'Villalba', 'Benegas', 'Acuña', 'Gimenez', 'Segovia', 'Nuñez', 'Quinteros', 'Fleitas',
            'Arce', 'Bogado', 'Rivarola', 'Chamorro', 'Figueredo', 'Montiel', 'Portillo', 'Caballero', 'Villagra', 'Reyes',
            'Galeano', 'Maldonado', 'Meza', 'Sosa', 'Rolon', 'Garcia', 'Molinas', 'Velazquez', 'Vargas', 'Yegros',
            'Benitez', 'Valenzuela', 'Samaniego', 'Gauto', 'Cantero', 'Estigarribia', 'Acosta', 'Gonzaga', 'Riveros', 'Duarte'
        ]


        dominios = [
            'gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com', 'icloud.com',
            'zoho.com', 'mail.com', 'yandex.com', 'aol.com', 'gmx.com',
            'inbox.com', 'rediffmail.com', 'live.com'
        ]


        for _ in range(cantidad_registros):
            nombre = random.choice(nombres)

            apellido1, apellido2 = random.sample(apellidos, 2)
            apellido = f"{apellido1} {apellido2}"
            
            cedula = str(random.randint(1000000, 5999999))
            timbrado = str(random.randint(10000000, 99999999))  
            celular = str(random.randint(100000000, 999999999)) if random.random() > 0.5 else None
            email = f"{nombre.lower()}.{apellido1.lower()}@{random.choice(dominios)}"
            direccion = f"Calle {random.randint(1, 100)}, Ciudad {random.randint(1, 10)}"

            Cliente.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                timbrado=timbrado,
                celular=celular,
                email=email,
                direccion=direccion
            )

        self.stdout.write(self.style.SUCCESS(f"{cantidad_registros} registros aleatorios creados exitosamente."))