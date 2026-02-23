from psycopg2.extensions import connection
from src.domain.producto import Producto, EstadoProducto, Disponible, NoDisponible
from src.domain.exception import ProductoNoExistenteError

class RepositorioProductos:
    def __init__(self, conn : connection):
        self.conn = conn
        
    def map_estado(self, estado_str):
        if estado_str == "disponible":
            return Disponible()
        if estado_str == "no disponible":
            return NoDisponible()
        
        
    def crear_tabla_productos(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos(
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    precio INTEGER NOT NULL,
                    stock INTEGER NOT NULL,
                    estado TEXT NOT NULL
                );
            """)
        
##########################################################    
    
    def get_producto(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, precio, stock, estado FROM productos WHERE id = %s
            """, (id,))

            row = cursor.fetchone()
        
            if row is None:
                raise ProductoNoExistenteError(f"el producto con id: {id} no existe")
        
            producto = Producto(row[0], row[1], row[2], row[3])
            producto.estado = self.map_estado(row[4])
            
            return producto
####################################################################

    def get_productos(self, limit : int , offset : int, estado = None, min_price = None, max_price = None):
        
        query = "SELECT id, nombre, precio, stock, estado, COUNT(*) OVER() as total FROM productos"
        
        filtros = []
        parametros = []

        if estado:
            filtros.append(" estado = (%s)")
            parametros.append(estado)
        
        if min_price:
            filtros.append(" precio >= (%s)")
            parametros.append(min_price)
            
        if max_price:
            filtros.append(" precio <= (%s)")
            parametros.append(max_price)
            
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
            
        query += " ORDER BY id LIMIT (%s) OFFSET (%s)"
        parametros.extend([limit, offset])
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, parametros)
            
            rows = cursor.fetchall()
            productos = []
            for r in rows:
                producto = Producto(r[0], r[1], r[2], r[3])
                producto.estado = self.map_estado(r[4])
                
                productos.append(producto) 
                
            if rows:
                total = rows[0][5]
            else:
                total = 0
                
            return productos, total
        
        
    def total_registros(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM productos
            """)
            row = cursor.fetchone()
            
            return row[0]
        
####################################################################    
    
    def actualizar_producto(self, producto : Producto):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE productos SET precio = %s, stock = %s, estado = %s WHERE id = %s
            """, (producto.precio, producto.stock, producto.estado.codigo(), producto.id))
            
            
            
            
#################################################################
            
    def guardar_producto(self, producto : Producto):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO productos (nombre,precio , stock, estado) VALUES (%s,%s,%s,%s)
                RETURNING id
            """, (producto.nombre,producto.precio, producto.stock, producto.estado.codigo()))
            
            producto_id = cursor.fetchone()[0]
            
            producto.id = producto_id
            return producto
            