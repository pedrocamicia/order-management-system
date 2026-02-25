from src.infrastructure.repositorio_productos import RepositorioProductos
from psycopg2.extensions import connection
from src.domain.producto import Producto
import math
from src.service.pagination import Page, restricciones_paginacion

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
    
######### get producto ###################

    def get_producto(self, producto_id):
        try:
            producto = self.repositorio_productos.get_producto(producto_id)
            
            return producto
        except:
            raise

####################################################################

    def get_productos(self, page : int, limit : int, estado : str, min_price : int, max_price : int):
        restricciones_paginacion(page, limit)
        
        offset = (page - 1) * limit
        
        productos, total= self.repositorio_productos.get_productos(limit , offset, estado, min_price, max_price)
        
        return Page(productos, total, page, limit)

