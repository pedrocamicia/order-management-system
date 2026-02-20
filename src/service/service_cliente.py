from src.infrastructure.repositorio_clientes import RepositorioCliente
from psycopg2.extensions import connection
from src.domain.cliente import Cliente

class ServiceCliente:
    def __init__(self, repositorio_cliente : RepositorioCliente, conn : connection):
        self.repositorio_cliente = repositorio_cliente
        self.conn = conn
        
    
    def crear_cliente(self, cliente_nombre):
        try:
            nuevo_cliente = Cliente(None, cliente_nombre)
            cliente = self.repositorio_cliente.guardar_cliente(nuevo_cliente)
            
            self.conn.commit()
            
            return cliente
        except Exception:
            self.conn.rollback()
            raise
        
    
    def get_cliente(self, cliente_id : int):
        try:
            cliente = self.repositorio_cliente.get_cliente(cliente_id)
            
            return cliente
        
        except:
            raise