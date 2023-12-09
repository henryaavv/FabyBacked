from django.contrib import admin

# Register your models here.

from .models import Cliente,Categoria,Producto,Pedido,PedidoDetalle,Cargo,Empleado,Registrar_pedido,Entregar_pedido

admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Registrar_pedido)
admin.site.register(Entregar_pedido)
