from src.infrastructure.repositorio_productos import RepositorioProductos
from psycopg2.extensions import connection
from src.domain.producto import Producto
from src.domain.exception import PaginaInvalidaError, LimiteInvalidoError
import math


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

    def get_productos(self, page : int, limit : int):
        if page < 1:
            raise PaginaInvalidaError("se ingreso una pagina negativa o 0")
        if limit < 1 or limit > 100:
            raise LimiteInvalidoError("se ingreso un limite invalido, menor a 1 o mayor a 100 no esta permitido") 
        
        offset = (page - 1) * limit
        
        productos= self.repositorio_productos.get_productos(limit , offset)
        
        total = self.repositorio_productos.total_registros()
        
        total_pages = math.ceil(total / limit) 
        
        return productos, total, total_pages
