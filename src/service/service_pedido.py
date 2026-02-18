from src.domain.pedido import Pedido
from src.domain.producto import Producto
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from psycopg2.extensions import connection
from src.domain.exception import DomainException

class PedidoService:
    def __init__(self, repositorio_pedidios : RepositorioPedidos, repositorio_productos : RepositorioProductos, conn : connection):
        self.repositorio_pedidos = repositorio_pedidios
        self.repositorio_productos = repositorio_productos
        self.conn = conn
    
############### confirmar pedido ################################################    
    
    
    def confirmar_pedido(self, pedido_id):
        try:
            pedido : Pedido= self.repositorio_pedidos.get_pedido(pedido_id)

            for item in pedido.items:
                producto = self.repositorio_productos.get_producto(item.producto_id)
                producto.disponible_para_venta(item.cantidad)
            
            pedido.confirmar_pedido()

            for item in pedido.items:
                producto = self.repositorio_productos.get_producto(item.producto_id)
                producto.descontar_stock(item.cantidad)
                self.repositorio_productos.actualizar_producto(producto)
                
            self.repositorio_pedidos.actualizar_pedido(pedido)
            
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
                
        
############# agregar al carrito ########################################
        
    def agregar_producto(self, pedido_id,producto_id, cantidad):
        pedido : Pedido = self.repositorio_pedidos.get_pedido(pedido_id)
        producto : Producto = self.repositorio_productos.get_producto(producto_id)
        
        producto.disponible_para_venta(cantidad)

        pedido.agregar_producto(producto, cantidad)
                
        self.repositorio_pedidos.actualizar_pedido(pedido)
                
        self.repositorio_pedidos.conn.commit()
        
        