from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

from usuarios.models import UsuarioPersonalizado
from catalogo.models import Marca, Categoria, Producto
from proveedores.models import Proveedor
from ventas.models import Venta, DetalleVenta
from compras.models import Compra, DetalleCompra


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba realistas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Borra todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        fake = Faker('es_ES')

        if options['clear']:
            self.stdout.write(self.style.WARNING('Borrando datos existentes...'))
            DetalleVenta.objects.all().delete()
            Venta.objects.all().delete()
            DetalleCompra.objects.all().delete()
            Compra.objects.all().delete()
            Producto.objects.all().delete()
            Categoria.objects.all().delete()
            Marca.objects.all().delete()
            Proveedor.objects.all().delete()
            UsuarioPersonalizado.objects.all().delete()
            Group.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos borrados.'))

        self.stdout.write('Creando grupos...')
        grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')
        grupo_vendedor, _ = Group.objects.get_or_create(name='Vendedor')
        grupo_admin, _ = Group.objects.get_or_create(name='Administrador')

        self.stdout.write('Creando usuarios...')
        clientes = []
        for i in range(20):
            user = UsuarioPersonalizado.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password='cliente123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                telefono=fake.phone_number()[:20],
                dni=str(fake.unique.random_number(digits=8, fix_len=True)),
            )
            user.groups.add(grupo_cliente)
            clientes.append(user)

        vendedores = []
        for i in range(2):
            user = UsuarioPersonalizado.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password='vendedor123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                telefono=fake.phone_number()[:20],
                dni=str(fake.unique.random_number(digits=8, fix_len=True)),
            )
            user.groups.add(grupo_vendedor)
            vendedores.append(user)

        admin_user = UsuarioPersonalizado.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema',
            telefono='1111111111',
            dni='11111111',
        )
        admin_user.groups.add(grupo_admin)
        self.stdout.write(self.style.SUCCESS(f'  - 20 clientes, 2 vendedores, 1 admin (admin/admin123)'))

        self.stdout.write('Creando marcas...')
        marcas_nombres = ['Asus', 'HP', 'Lenovo', 'Dell', 'Acer', 'MSI', 'Samsung', 'LG', 'Logitech', 'Razer']
        marcas = []
        for nombre in marcas_nombres:
            marca = Marca.objects.create(
                nombre=nombre,
                descripcion=fake.text(max_nb_chars=200),
                pais_origen=fake.country(),
            )
            marcas.append(marca)

        self.stdout.write('Creando categorías...')
        categorias_nombres = [
            'Notebooks', 'Monitores', 'Teclados', 'Mouse', 'Auriculares',
            'Impresoras', 'Router', 'Disco Externo', 'Memoria RAM', 'Fuentes'
        ]
        categorias = []
        for nombre in categorias_nombres:
            cat = Categoria.objects.create(
                nombre=nombre,
                descripcion=fake.text(max_nb_chars=200),
            )
            categorias.append(cat)

        self.stdout.write('Creando productos...')
        productos_nombres = [
            'Notebook Gaming 15"', 'Notebook Ultrabook 14"', 'Monitor 27" 144Hz',
            'Teclado Mecánico RGB', 'Mouse Inalámbrico Ergonómico', 'Auriculares 7.1',
            'Impresora Multifunción', 'Router WiFi 6', 'SSD NVMe 1TB', 'RAM DDR5 32GB',
            'Notebook Office 15.6"', 'Monitor Curvo 32"', 'Teclado Membrana',
            'Mouse Gamer 16000 DPI', 'Auriculares Bluetooth', 'Impresora Láser',
            'Switch 8 Puertos', 'HDD Externo 4TB', 'RAM DDR4 16GB', 'Fuente 750W 80+',
            'Notebook 2-en-1 13"', 'Monitor 4K 28"', 'Teclado Compacto 60%',
            'Mouse Vertical', 'Auriculares Cancelación Ruido'
        ]
        productos = []
        for i, nombre in enumerate(productos_nombres):
            precio_base = random.randint(50000, 800000)
            producto = Producto.objects.create(
                nombre=nombre,
                descripcion_corta=fake.text(max_nb_chars=100),
                descripcion_larga=fake.text(max_nb_chars=500),
                sku=f'SKU-{random.randint(100000, 999999)}',
                precio_lista=precio_base,
                precio_oferta=round(precio_base * random.uniform(0.7, 0.95), 2) if random.random() > 0.3 else None,
                stock_total=random.randint(10, 200),
                destacado=random.random() > 0.7,
                marca=random.choice(marcas),
                categoria=random.choice(categorias),
            )
            productos.append(producto)

        self.stdout.write('Creando proveedores...')
        proveedores = []
        for i in range(20):
            prov = Proveedor.objects.create(
                nombre=fake.unique.company(),
                cuit=f'{random.randint(20, 33)}-{random.randint(10000000, 99999999)}-{random.randint(0, 9)}',
                email=fake.unique.company_email(),
                telefono=fake.phone_number()[:50],
                direccion=fake.address(),
            )
            proveedores.append(prov)

        self.stdout.write('Creando ventas...')
        estados_venta = ['pendiente', 'completada', 'cancelada']
        ventas = []
        for i in range(20):
            fecha = timezone.now() - timedelta(days=random.randint(0, 90))
            venta = Venta.objects.create(
                cliente=random.choice(clientes),
                estado=random.choice(estados_venta),
                nro_factura=f'FC-{random.randint(100000, 999999)}',
                created_at=fecha,
            )
            ventas.append(venta)

            num_detalles = random.randint(1, 4)
            productos_venta = random.sample(productos, min(num_detalles, len(productos)))
            for prod in productos_venta:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=prod,
                    unidades=random.randint(1, 5),
                    precio_unitario=prod.precio_oferta if prod.precio_oferta else prod.precio_lista,
                )

        self.stdout.write('Creando compras...')
        estados_compra = ['pendiente', 'recibida', 'cancelada']
        for i in range(20):
            compra = Compra.objects.create(
                proveedor=random.choice(proveedores),
                estado=random.choice(estados_compra),
                nro_factura=f'FC-C-{random.randint(100000, 999999)}',
            )

            num_detalles = random.randint(1, 5)
            productos_compra = random.sample(productos, min(num_detalles, len(productos)))
            total = 0
            for prod in productos_compra:
                unidades = random.randint(5, 50)
                precio = round(prod.precio_lista * random.uniform(0.4, 0.7), 2)
                DetalleCompra.objects.create(
                    compra=compra,
                    producto=prod,
                    unidades=unidades,
                    precio=precio,
                )
                total += unidades * precio
            compra.total = total
            compra.save()

        self.stdout.write(self.style.SUCCESS('\n¡Base de datos poblada con éxito!'))
        self.stdout.write(f'  - Grupos: 3')
        self.stdout.write(f'  - Usuarios: 23 (20 clientes, 2 vendedores, 1 admin)')
        self.stdout.write(f'  - Marcas: {len(marcas)}')
        self.stdout.write(f'  - Categorías: {len(categorias)}')
        self.stdout.write(f'  - Productos: {len(productos)}')
        self.stdout.write(f'  - Proveedores: {len(proveedores)}')
        self.stdout.write(f'  - Ventas: {len(ventas)}')
        self.stdout.write(f'  - Compras: 20')