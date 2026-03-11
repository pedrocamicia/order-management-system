from src.infrastructure.repositorio_clientes import RepositorioCliente
from psycopg2.extensions import connection
from src.domain.cliente import Cliente
from src.service.pagination import Page, restricciones_paginacion
from src.domain.exception import AuthorizationError, NoEsDuenoDeRecursoError

class ServiceCliente:
    def __init__(self, repositorio_cliente : RepositorioCliente, conn : connection):
        self.repositorio_cliente = repositorio_cliente
        self.conn = conn
        
    def _require_role(self, user):
        if not user.role != "admin":
            raise AuthorizationError("se requiere rol admin para acceder")
    
    def crear_cliente(self, cliente_nombre):
        try:
            nuevo_cliente = Cliente(None, cliente_nombre)
            cliente = self.repositorio_cliente.guardar_cliente(nuevo_cliente)
            
            self.conn.commit()
            
            return cliente
        except Exception:
            self.conn.rollback()
            raise
        
    
    def get_cliente(self, cliente_id : int, user):
        try:
            cliente = self.repositorio_cliente.get_cliente(cliente_id)
            
            if cliente_id != user.id and user.role != "admin":
                raise NoEsDuenoDeRecursoError("no puede acceder si no es su perfil o su rol no es admin")
            
            return cliente
        
        except:
            raise
    
    def get_clientes(self, limit, page, nombre, user):
        
        self._require_role(user)
        
        restricciones_paginacion(page, limit)
        offset = (page - 1)* limit
        
        clientes, total = self.repositorio_cliente.get_clientes(limit, offset, nombre)
        
        return Page(clientes, total, page,limit)