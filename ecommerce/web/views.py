from django.shortcuts import render
from .models import Categoria,Producto, Pedido, PedidoDetalle
# Create your views here.
def index(request):
    lista_categorias = Categoria.objects.all()
    lista_productos = Producto.objects.all()

    context = {
        'categorias':lista_categorias,
        'productos':lista_productos
    }
    return render(request,'index.html',context)


def productos_por_categoria(request,categoria_id):
    """vista para filtrar productos por categoria"""
    obj_categoria= Categoria.objects.get(pk=categoria_id)
    lista_productos = obj_categoria.producto_set.all()
    lista_categorias = Categoria.objects.all()
    context = {
        'categorias':lista_categorias,
        'productos':lista_productos
    }

    return render(request,'index.html',context)



def productos_por_nombre(request):
    produc_nombre=request.POST['produc_nombre']

    lista_productos = Producto.objects.filter(produc_nombre__contains=produc_nombre)
    lista_categorias= Categoria.objects.all()
    
    context = {
        'categorias':lista_categorias,
        'productos':lista_productos
    }

    return render(request,'index.html',context)

#primero se crea la vista

def producto(request,producto_id):
    obj_producto = Producto.objects.get(pk=producto_id)
    context = {
        'producto':obj_producto
    }
    return render (request,'producto.html',context)


""""Vista de  carrito"""
  
from .carrito import Cart 

def carrito(request):
    return render(request,'carrito.html')
    
def agregar_carrito(request,producto_id):

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    obj_producto = Producto.objects.get(pk=producto_id)
    carrito = Cart(request)
    carrito.add(obj_producto,cantidad)

    print(request.session.get('cart'))
    return render(request,'carrito.html')

def eliminar_carrito(request,producto_id):
    obj_producto = Producto.objects.get(pk=producto_id)
    carrito = Cart(request)
    carrito.delete(obj_producto)

    return render(request,'carrito.html')


def limpiar_carrito(request):
    carrito = Cart(request)
    carrito.clear()
    return render(request,'carrito.html')




#Vista para clientes

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Cliente
from django.shortcuts import redirect


def crear_usuario(request):
    pagina_destino = request.GET.get('next', None)
    context = {
        'destino':pagina_destino
    }
    if request.method == 'POST':
        data_usuario = request.POST['usuario']
        data_password = request.POST['password']
        data_destino=request.POST['destino']

        usuario = User.objects.create_user(
            username=data_usuario,
            password=data_password)
        if usuario is not None:
            login(request, usuario)
            if data_destino != 'None':
                return redirect(data_destino)
            return redirect('/cuenta')
        
    return render(request, 'login.html')


from django.http import HttpResponse
"""
def crear_usuario(request):
    if request.method == 'POST':
        data_usuario = request.POST.get('usuario')
        data_password = request.POST.get('password')
        data_destino = request.POST.get('destino')

        try:
            # Crear usuario
            usuario = User.objects.create_user(
                username=data_usuario,
                password=data_password
            )
            
            # Autenticar al usuario
            login(request, usuario)

            # Redirigir
            if data_destino != 'None':
                return redirect(data_destino)
            return redirect('/cuenta')
        except Exception as e:
            # Imprimir el error en la consola del servidor
            print(f"Error al crear usuario: {e}")
            return HttpResponse("Error al crear usuario. Consulta la consola del servidor para más detalles.")
    
    return render(request, 'login.html')

"""

def login_usuario(request):
    pagina_destino = request.GET.get('next', None)
    context = {
        'destino':pagina_destino
    }
    if request.method == 'POST':
        data_usuario= request.POST['usuario']
        data_password=request.POST['password']
        data_destino=request.POST['destino']
        print(data_destino)

        usuario = authenticate(
            request,
            username=data_usuario, 
            password=data_password)
        if  usuario is not None:
            login(request, usuario)
            if data_destino != 'None':
                return redirect(data_destino)
            return redirect('/cuenta')


        else:
            context={
                'destino':data_destino,
                'mensaje_error':'Datos incorrectos'
            }
           
    return render(request, 'login.html',context)

from .forms import ClienteForm

@login_required(login_url='/login')
def cuenta_usuario(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)

        data_cliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':cliente.cliente_direción,
            'telefono':cliente.cliente_telefono,
            'dni':cliente.cliente_dni,
            'fecha_nacimiento':cliente.cliente_fecha_nacimiento
        }
    except:
        data_cliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    form = ClienteForm(data_cliente)
    context = {
        'form':form
    }
    return render(request,'cuenta.html',context)



@login_required(login_url='/login')
def logout_usuario(request):
    logout(request)
    return redirect('/cuenta')



@login_required(login_url='/login')
def actualizar_cliente(request):
    mensaje_confirmacion = ""
    frm_cliente = ClienteForm(request.POST)  
    if frm_cliente.is_valid():
        data_cliente = frm_cliente.cleaned_data
    #actualizar usuario
        usuario = User.objects.get(pk=request.user.id)        
        usuario.first_name = data_cliente['nombre']
        usuario.last_name=data_cliente['apellidos']
        usuario.email = data_cliente['email']
        usuario.save()

    #actualizar o registrar cliente
        try:
            cliente = Cliente.objects.get(usuario=usuario)

        except Exception as error:
            print("error:", error)
            cliente = Cliente()
            cliente.usuario=usuario
        
        cliente.cliente_dni = data_cliente['dni']
        cliente.cliente_direción=data_cliente['direccion']
        cliente.cliente_telefono=data_cliente['telefono']
        cliente.cliente_fecha_nacimiento = data_cliente['fecha_nacimiento']
        cliente.save()
        mensaje_confirmacion = 'DATOS ACTUALIZADOS'


    context = {
        'form':frm_cliente,
        'mensaje':mensaje_confirmacion
    }
    return render(request,'cuenta.html',context)


@login_required(login_url='/login')
def confirmar_pedido(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
        data_cliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':cliente.cliente_direción,
            'telefono':cliente.cliente_telefono,
            'dni':cliente.cliente_dni,
            'fecha_nacimiento':cliente.cliente_fecha_nacimiento
        }
    except:
        data_cliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    form = ClienteForm(data_cliente)
    context = {
        'form':form
    }
    return render(request,'pedido.html',context)

from django.urls import reverse
from datetime import datetime
from paypal.standard.forms import PayPalPaymentsForm
@login_required(login_url='/login')
def registrar_pedido(request):
    context = {}
    if request.method =='POST':
        print("metodo post")
        #gestion de usuario y cliente
        data_cliente = request.POST
        #Actualizar usuario
        usuario = User.objects.get(pk=request.user.id)
        usuario.first_name = data_cliente['nombre']
        usuario.last_name = data_cliente['apellidos']
        usuario.email = data_cliente['email']
        usuario.save()

        try:
            cliente = Cliente.objects.get(usuario=usuario)
            cliente.cliente_telefono = data_cliente['telefono']
            cliente.cliente_direción = data_cliente['direccion']
            cliente.save()
        except:
            cliente = Cliente()
            cliente.usuario = usuario
            cliente.cliente_direción = data_cliente['direccion']
            cliente.cliente_telefono = data_cliente['telefono']
            cliente.save()
                
        pedido = Pedido()
        pedido.cliente = cliente
        pedido.direccion_envio = data_cliente['direccion']
        pedido.save()

        #registrar pedido detalle 
        #carrito = request.session.get('cart')
        carrito = Cart(request)
        for key, value in carrito.cart.items():
            producto = Producto.objects.get(pk=value['producto_id'])
            pedido_detalle=PedidoDetalle()
            pedido_detalle.pedido = pedido
            pedido_detalle.producto = producto
            pedido_detalle.cantidad = int(value['cantidad'])
            pedido_detalle.precio = float(value['precio'])
            pedido_detalle.subtotal = float(value['subtotal'])
            pedido_detalle.save()

            #limpiamos el carrito
        carrito.clear()

        nro_pedido = 'PED' + str(pedido.id)
        pedido.nro_pedido = nro_pedido
        pedido.monto_total = carrito.total
        pedido.save()

        #Configuramos formulario paypal
        paypal_dict = {
            "business": "sb-isgb728657854@business.example.com",
            "amount": pedido.monto_total,
            "item_name": "pedido tienda online",
            "invoice": pedido.nro_pedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/pedido/pagado'),
            "cancel_return": request.build_absolute_uri('/'),
        }

        # Create the instance.
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        request.session['pedido_id']=pedido.id
        context = {
            'pedido':pedido,
            'paypal_form':paypal_form
        }
    return render(request, 'pago.html',context)



@login_required(login_url='/login')
def pedido_pagado(request):
    context = {}
    pedido = Pedido.objects.get(pk=request.session.get('pedido_id'))
    pedido.estado = 'P'
    pedido.save()
    context = {
        'pedido':pedido
    }
    return render(request,'pedidopagado.html',context)
 


    