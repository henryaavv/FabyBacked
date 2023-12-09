class Cart:

    def __init__(self,request):
        self.request = request
        self.session = request.session
        
        cart = self.session.get('cart')
        total = self.session.get('total')
        if not cart:
            cart = self.session['cart']={}
            total = self.session['total']='0'
        self.cart=cart
        self.total=float(total)

    def add(self,producto,cantidad):
        if(str(producto.id) not in self.cart.keys()):
            self.cart[producto.id]={
                'producto_id':producto.id,
                'nombre':producto.produc_nombre,
                'cantidad':cantidad,
                'precio':str(producto.produc_precio),
                'imagen':producto.produc_imagen.url,
                'categoria':producto.categoria.catego_nombre,
                'subtotal':str(cantidad * producto.produc_precio)
            }
        else:
            for key,value in self.cart.items():
                if key == str(producto.id):
                    value['cantidad']=str(int(value['cantidad'])+cantidad)
                    value['subtotal']=str(float(value['cantidad'])*float(value['precio']))
                    break
        self.save()
        #self.session['cart']=self.cart
        #self.session.modified = True

    
    def delete(self,producto):
        producto_id= str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def clear(self):
        self.session['cart']={} 
        self.session['total']= '0'

    def save(self):
        total = 0
        for key,value in self.cart.items():
            total += round(float(value['subtotal']),2)

        self.session['cart'] = self.cart
        self.session['total'] = total
        self.session.modified= True
     