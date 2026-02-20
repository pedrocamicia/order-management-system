from src.infrastructure.repositorio_productos import RepositorioProductos
from psycopg2.extensions import connection
from src.domain.producto import Producto
class ProductoService:
    def __init__(self, repositorio_productos : RepositorioProductos, conn : connection):
        self.repositorio_productos = repositorio_productos
        self.conn = conn
        
        
    def crear_producto(self, nombre : str, precio:int, stock : int):
        try:
            producto = Producto(None, nombre, precio, stock)

            nuevo_producto = self.repositorio_productos.guardar_producto(producto)
            self.conn.commit()
            
            return nuevo_producto
        
        except Exception:
            self.conn.rollback()
            raise    
    