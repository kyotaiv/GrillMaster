from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now 

class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True, verbose_name="Id de categoria")
    nombreCategoria = models.CharField(max_length=50, blank=True, verbose_name="Nombre de categoria")
    def __str__(self):
        return self.nombreCategoria

class Productos(models.Model):
    name = models.CharField(max_length=200)
    id = models.CharField(max_length=100,primary_key=True)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField()
    categoria= models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    def __str__(self):
        return self.name

class Genero(models.Model):
    id_genero = models.AutoField(db_column='idGenero', primary_key=True)
    genero = models.CharField(max_length=20, blank=False, null=False)
    def __str__(self):
        return str(self.genero)

class Registro_cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nac = models.DateField()
    id_genero = models.ForeignKey('Genero', on_delete=models.CASCADE, db_column='idGenero')

    def __str__(self):
        return self.user.username
    
class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.BigIntegerField()
    taxes = models.BigIntegerField(default=0)
    status = models.IntegerField(default=3)
    shipping = models.BigIntegerField(default=0)
    date = models.DateTimeField(blank=False, null=False, default=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def status_str(self):
        if self.status == 0:
            return 'Procesando servicios'
        if self.status == 1:
            return 'Servicios confirmados y en espera del dia'
        if self.status == 2:
            return 'Servicios recibidos'
        return 'Desconocido'
    
    def __str__(self):
        return str(self.id)
    
    @property
    def percent(self):
        return round(self.status * 33.3)
        
class Detalles_orden(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles_orden')
    product_id = models.ForeignKey(Productos, on_delete=models.CASCADE)
    amount = models.IntegerField()
    subtotal = models.IntegerField()

class OpcionesContacto(models.Model):
    opciones = models.CharField(primary_key=True, verbose_name="Opcion de contacto",max_length=200 )

class Contacto(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(primary_key=True, max_length=200)
    description = models.CharField(max_length=1000)
    reason = models.ForeignKey('OpcionesContacto', on_delete=models.CASCADE, db_column='Opciones')
    image = models.ImageField()