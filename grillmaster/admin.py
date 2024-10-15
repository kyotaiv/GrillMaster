from django.contrib import admin
from .models import Categoria, Detalles_orden, Genero, Orden, Productos, Registro_cliente, Contacto, OpcionesContacto

# Register your models here.
admin.site.register(Productos)
admin.site.register(Registro_cliente)
admin.site.register(Genero)
admin.site.register(Orden)
admin.site.register(Detalles_orden)
admin.site.register(Categoria)
admin.site.register(Contacto)
admin.site.register(OpcionesContacto)
