from psycopg2.extensions import connection
from src.domain.cliente import Cliente
from src.domain.exception import ClienteNoExistente

class RepositorioCliente:
    def __init__(self, conn : connection):
        self.conn = conn
        
        
        
        
        
#esto fue agregado para test, luego borrar y mejorar si hace falta

    def crear_tabla_clientes(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes(
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL
                );
            """)
            
    def guardar_cliente(self, cliente : Cliente):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO clientes (nombre) VALUES (%s)
                RETURNING id
            """, (cliente.nombre,))
            
            cliente_id = cursor.fetchone()[0]
            
            cliente.id = cliente_id
            return cliente
            
    def get_cliente(self, cliente_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM clientes WHERE id = %s", (cliente_id,))
            
            row = cursor.fetchone()
            if row is None:
                raise ClienteNoExistente(f"el id del cliente ingresado: {cliente_id} no existe")
            
            return Cliente(*row)
        
        
        
    def get_clientes(self, limit, offset , nombre):
        
        query = "SELECT id, nombre, COUNT(*) OVER() as total from clientes"
        
        filters = []
        params = []
        
        if nombre:
            filters.append("nombre = (%s)")
            params.append(nombre)
            
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += " ORDER BY id LIMIT (%s) OFFSET (%s)"
        
        params.extend([limit, offset])
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            
            rows = cursor.fetchall()
            
            clientes = []
            for r in rows:
                cliente = Cliente(r[0], r[1])
                clientes.append(cliente)
                
            total = rows[0][2]
            
            return clientes, total