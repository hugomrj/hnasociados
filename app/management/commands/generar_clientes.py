import random
from django.core.management.base import BaseCommand
from app.models.cliente_views_model import Cliente  # Asegúrate de que la ruta sea correcta


import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hnasociados.settings')
django.setup()


class Command(BaseCommand):
    help = 'Genera 30 registros aleatorios para la tabla clientes'

    def handle(self, *args, **kwargs):
        nombres = [
           'Juan', 'Maria', 'Pedro', 'Ana', 'Luis', 'Laura', 'Carlos', 'Sofia', 'Diego', 'Valentina',
            'Fernando', 'Camila', 'Ricardo', 'Martina', 'Sebastian', 'Lucia', 'Gabriel', 'Paula', 'Javier', 'Julieta',
            'Roberto', 'Andrea', 'Hugo', 'Victoria', 'Manuel', 'Elena', 'Daniel', 'Florencia', 'Alejandro', 'Carolina'
        ]
        apellidos = [
            'Gomez', 'Perez', 'Gonzalez', 'Rodriguez', 'Lopez', 'Martinez', 'Fernandez', 'Diaz', 'Sanchez', 'Romero',
            'Torres', 'Ramirez', 'Flores', 'Benitez', 'Acosta', 'Medina', 'Herrera', 'Jimenez', 'Ortega', 'Silva',
            'Castro', 'Mendoza', 'Rojas', 'Navarro', 'Guerrero', 'Vargas', 'Delgado', 'Cabrera', 'Morales', 'Paredes',
            'Figueroa', 'Salazar', 'Peralta', 'Dominguez', 'Coronel', 'Britez', 'Galeano', 'Vera', 'Franco', 'Cantero'
        ]

        dominios = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']

        for _ in range(100):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            cedula = str(random.randint(10000000, 99999999))  # Cédula de 8 dígitos
            timbrado = str(random.randint(100000, 999999)) if random.random() > 0.5 else None
            celular = str(random.randint(100000000, 999999999)) if random.random() > 0.5 else None
            email = f"{nombre.lower()}.{apellido.lower()}@{random.choice(dominios)}"
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

        self.stdout.write(self.style.SUCCESS('registros aleatorios creados exitosamente.'))