from psycopg2.extensions import connection
from src.domain.pedido import Pedido, Carrito, Confirmado
from src.domain.item_pedido import ItemPedido
from src.domain.exception import PedidoNoExistenteError

class RepositorioPedidos:
    def __init__(self, conn : connection):
        self.conn = conn
    
    ##########################################
    
    def map_estado(self, estado_str):
        if estado_str == "carrito":
            return Carrito()
        if estado_str == "confirmado":
            return Confirmado()
        
    def map_pedido(self, id, cliente_id, estado, fecha_confirmacion):
        pedido = Pedido(id, cliente_id)
        
        pedido.estado =self.map_estado(estado)
        pedido.fecha_confirmacion = fecha_confirmacion
        return pedido
    
    #########################################
    
    def crear_tabla_pedidos(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos(
                    id SERIAL PRIMARY KEY,
                    estado TEXT NOT NULL,
                    cliente_id INTEGER NOT NULL,
                    fecha_confirmacion TIMESTAMP,
                    
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                );
            """)

    def crear_tabla_items(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items(
                    pedido_id INTEGER,
                    producto_id INTEGER,
                    cantidad INTEGER NOT NULL,
                    precio_unitario INTEGER NOT NULL,
                    
                    FOREIGN KEY (producto_id) REFERENCES productos(id),
                    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                    
                    PRIMARY KEY (pedido_id, producto_id)
                );
            """)
        

################## actualizar ############################

    def actualizar_pedido(self, pedido : Pedido):
        self.actualizar_estado_pedido(pedido)
        self.actualizar_items(pedido)   


    def actualizar_estado_pedido(self, pedido : Pedido):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE pedidos SET estado = %s, fecha_confirmacion = %s WHERE id = %s
            """, (pedido.estado.codigo(), pedido.fecha_confirmacion, pedido.id))
        
    def actualizar_items(self, pedido : Pedido):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM items WHERE pedido_id = %s
            """, (pedido.id,))
            for i in pedido.items:
                cursor.execute("""
                    INSERT INTO items (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s,%s)
                """, (pedido.id, i.producto_id, i.cantidad, i.precio_unitario))
                
####### get #################################
    
    def get_pedido(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, cliente_id, estado, fecha_confirmacion FROM pedidos WHERE id = %s
            """, (id,))
            
            row = cursor.fetchone()
            
            if row is None:
                raise PedidoNoExistenteError(f"el pedido con id: {id} no existe")
            
            pedido = self.map_pedido(*row)
            
            cursor.execute("""
                SELECT producto_id, cantidad, precio_unitario FROM items WHERE pedido_id = %s
            """, (id,))
            
            rows = cursor.fetchall()
            
            for r in rows:
                item = ItemPedido(*r)
                pedido.items.append(item)
                
            return pedido

########################################################

    def crear_pedido(self, pedido : Pedido):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO pedidos (estado, cliente_id, fecha_confirmacion) VALUES (%s, %s, %s)
                RETURNING id
                """,(pedido.estado.codigo(), pedido.cliente_id, pedido.fecha_confirmacion))
            
            pedido_id  = cursor.fetchone()[0]
            
            pedido.id = pedido_id

            return pedido