from datetime import datetime, date, timedelta
from src.domain.item_pedido import ItemPedido
from src.domain.exception import EstadoPedidoInvalido,CantidadInvalida,PedidoVacioInvalido

class Pedido:
    def __init__(self, id : int | None,cliente_id : int):
        self.id = id
        self.estado : EstadoPedido = Carrito()
        self.fecha_confirmacion = None
        self.cliente_id = cliente_id
        self.items : list[ItemPedido] = []
        
        
#################################################################

    def agregar_producto(self,producto, cantidad):
        
        self.validar_agregar_producto(producto, cantidad)
        
        if self.hay_producto(producto.id):
            self.sumar_cantidad_de_producto(producto.id, cantidad)
            return
        
        item = ItemPedido(producto.id, cantidad, producto.precio)
        self.items.append(item) 
        
    def validar_agregar_producto(self, producto, cantidad):
        if not self.estado.puede_agregarse_producto():
            raise EstadoPedidoInvalido(f"no se puede agregar un producto al pedido desde el estado actual: {self.estado.codigo()}")
        if cantidad <= 0:
            raise CantidadInvalida("no se puede agregar una cantidad 0 o negativa de profuctos")
        
    
    def sumar_cantidad_de_producto(self, producto_id, cantidad):
        item = next((i for i in self.items if i.producto_id == producto_id ), None)
        item.cantidad += cantidad
    
    def hay_producto(self, producto_id):
        for item in self.items:
            if item.producto_id == producto_id:
                return True
        return False
    
#####################################################
    
    def confirmar_pedido(self):
        
        self.validar_confirmacion()
        
        self.fecha_confirmacion = datetime.now()
        self.estado = Confirmado()      
    
    
    def validar_confirmacion(self):
        if not self.estado.puede_confirmarse():
            raise EstadoPedidoInvalido(f"no se puede confirmar el pedido desde el estado acutal: {self.estado.codigo()}")
        
        self.contenido_valido()
            
    def contenido_valido(self):
        if not self.items:
            raise PedidoVacioInvalido("no se puede confirmar el pedido, esta vacio")
        
######################################################

    def total(self):
        total = 0
        for item in self.items:
            total += item.subtotal()
        return total
    
    def cantidad_de_productos(self):
        cantidad = 0
        for i in self.items:
            cantidad += i.cantidad
        return cantidad
    
    
    
####################### estado pedido ########################   
 
class EstadoPedido:
    def codigo(self):
        raise NotImplementedError()
    
    def puede_agregarse_producto(self):
        return False

    def puede_confirmarse(self):
        return False
        
class Carrito(EstadoPedido):
    def codigo(self):
        return "carrito"
    
    def puede_agregarse_producto(self):
        return True
    
    def puede_confirmarse(self):
        return True
    
    
class Confirmado(EstadoPedido):
    def codigo(self):
        return "confirmado"