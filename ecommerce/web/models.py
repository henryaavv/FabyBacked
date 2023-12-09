from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    cliente_dni=models.CharField(max_length=8)
    cliente_telefono = models.CharField(max_length=50)
    cliente_fecha_nacimiento=models.DateField(null=True)
    cliente_direción = models.TextField()
  
    class Meta:
        db_table = 'tbl_cliente'

    def __str__(self):
	    return self.cliente_dni
    


class Categoria(models.Model):
    catego_nombre = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'tbl_categoria'

    def __str__(self):
        return self.catego_nombre
    


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    produc_nombre = models.CharField(max_length=45)
    produc_imagen = models.ImageField(upload_to='productos',blank=True)
    produc_descripcion = models.TextField(null=True)
    produc_precio = models.DecimalField(max_digits=5,decimal_places=2)
    produc_cantidad = models.IntegerField(default=0, null=True, blank=True)
    
    class Meta:
        db_table = 'tbl_producto'       

    def __str__(self):  
        return self.produc_nombre
    
class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('S', 'SOLICITADO'),
        ('P', 'PAGADO')
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    nro_pedido = models.CharField(max_length=20, null=True)
    monto_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    direccion_envio = models.TextField(null=True)
    estado = models.CharField(max_length=1, default='S', choices=ESTADO_CHOICES)

    class Meta:
        db_table = 'tbl_pedido'

    def __str__(self):
        return self.nro_pedido
      
      
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)   
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'tbl_pedido_detalle'
    
    def __str__(self):
        return self.producto.produc_nombre



class Cargo(models.Model):
    cargo_nombre = models.CharField(max_length=45)
    cargo_descripcion = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'tbl_cargo'

    def __str__(self):
        return self.cargo_nombre
    
   

class Empleado(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT)
    empleado_dni=models.CharField(max_length=8)
    empleado_telefono = models.CharField(max_length=50)
    fecha_contrato = models.DateTimeField(auto_now_add=True)
    empleado_direción = models.TextField()
    salario = models.CharField(max_length=45)

    class Meta:
        db_table = 'tbl_empleado'

    def __str__(self):
	    return self.empleado_dni
    


class Registrar_pedido(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT)
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    regis_pedido_comentario = models.CharField(max_length=200, null=True)
    regis_pedido_fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
  

    class Meta:
        db_table = 'tbl_registro_pedido'

    def __str__(self):
        return self.regis_pedido_comentario
    

class Entregar_pedido(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT)
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    entre_pedido_numero = models.CharField(max_length=20, null=True) 
    entre_pedido_comentario = models.CharField(max_length=200, null=True)
    entre_pedido_fecha_entrega = models.DateTimeField(auto_now_add=True, null=True)
   

    class Meta:
        db_table = 'tbl_entrega_pedido'

    def __str__(self):
        return self.entre_pedido_numero

        