
class ItemPedido:
    def __init__(self, producto_id : int, cantidad : int, precio_unitario : int):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        
    def subtotal(self): #esta bien q precio ingerse por parametro? no es raro? si es entidad intermedia no deberia ya conocer el precio? o poder preguntarlo difrectamente? ver eso
        return self.cantidad * self.precio_unitario