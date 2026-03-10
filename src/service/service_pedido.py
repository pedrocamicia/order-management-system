from src.domain.pedido import Pedido
from src.domain.producto import Producto
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.infrastructure.repositorio_clientes import RepositorioCliente
from psycopg2.extensions import connection
from src.domain.exception import DomainException

class PedidoService:
    def __init__(self, repositorio_pedidios : RepositorioPedidos, repositorio_productos : RepositorioProductos, repositorio_clientes : RepositorioCliente,conn : connection):
        self.repositorio_pedidos = repositorio_pedidios
        self.repositorio_productos = repositorio_productos
        self.repositorio_clientes = repositorio_clientes
        self.conn = conn
    
############ get pedido #########################################################

    def get_pedido(self, pedido_id : int, user):
        try:
            pedido = self.repositorio_pedidos.get_pedido(pedido_id)
            
            pedido.verify_access(user.id , user.role)

            return pedido
        except:
            raise
    
############# iniciar pedido ###################################################

    def iniciar_pedido(self, cliente_id):
        try:
            self.repositorio_clientes.get_cliente(cliente_id)

            pedido = self.repositorio_pedidos.crear_pedido(Pedido(None, cliente_id))        
            
            self.conn.commit()
            
            return pedido
        except Exception:
            self.conn.rollback()
            raise
    
############### confirmar pedido ################################################    
    
    
    def confirmar_pedido(self, pedido_id, user):
        try:
            pedido : Pedido= self.repositorio_pedidos.get_pedido(pedido_id)

            pedido.verify_access(user.id , user.role)
            
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
            
            return pedido   
        
        except Exception:
            self.conn.rollback()
            raise
                
        
############# agregar al carrito ########################################
        
    def modificar_items_pedido(self, pedido_id,producto_id, cantidad, user):
        try:
            pedido : Pedido = self.repositorio_pedidos.get_pedido(pedido_id)
            producto : Producto = self.repositorio_productos.get_producto(producto_id)
                        
            pedido.verify_access(user.id , user.role)
                        
            producto.disponible_para_venta(cantidad)

            pedido.set_cantidad(producto, cantidad)
                    
            self.repositorio_pedidos.actualizar_pedido(pedido)
                    
            self.conn.commit()
            
            return pedido
        
        except Exception:
            self.conn.rollback()
            raise

##########  eliminar producto ####################

    def eliminar_item(self, pedido_id, producto_id, user): 
        try:
            producto = self.repositorio_productos.get_producto(producto_id)
            pedido = self.repositorio_pedidos.get_pedido(pedido_id)
            
            pedido.verify_access(user.id , user.role)
            
            pedido.eliminar_item(producto_id)
            
            self.repositorio_pedidos.actualizar_pedido(pedido)
            
            self.conn.commit()
        except:
            self.conn.rollback()
            raise