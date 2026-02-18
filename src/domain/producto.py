from src.domain.exception import CantidadDeProductoNoDisponibleEnStock, ProductoNoDisponible

class Producto:
    def __init__(self, id : int | None,nombre: str, precio : int, stock : int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.estado: EstadoProducto = Disponible()


    def disponible_para_venta(self, cantidad):
        if not self.esta_disponible():
            raise ProductoNoDisponible("no se puede agragr al carrito, el prodcuto no esta disponible")
        self.validar_stock(cantidad)
        
        
    def esta_disponible(self):
        return self.estado.disponible()
    
    def validar_stock(self, cantidad):
        if cantidad > self.stock:
            raise CantidadDeProductoNoDisponibleEnStock(f"la cantidad ingresada del prodcuto no esta disponible en stock. Se encuentra disponibles: {self.stock} unidades")



##########################################################
    def descontar_stock(self, cantidad):
        self.validar_stock(cantidad) #para venta se estaria validando stock dos veces. pero lo dejo tambien aca porque quizas se llame a descontar stock desde un cu que no sea venta, y haya que validar
        
        self.stock -= cantidad
     
    def incrementar_stock(self, cantidad):
        self.stock += cantidad



################ estado producto ######################################################################

class EstadoProducto:
    def codigo(self):
        raise NotImplementedError
    
    def disponible(self):
        return False

class Disponible(EstadoProducto):
    def codigo(self):
        return "disponible"
    
    def disponible(self):
        return True

class NoDisponible(EstadoProducto):
    def codigo(self):
        return "no disponible"
