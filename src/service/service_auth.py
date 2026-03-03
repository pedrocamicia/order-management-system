from src.infrastructure.repositorio_users import RepositorioUser,User
from src.infrastructure.repositorio_clientes import RepositorioCliente,Cliente
from psycopg2.extensions import connection
from src.infrastructure.security import password

class AuthService:
    def __init__(self, repositorio_users : RepositorioUser,repositorio_clientes : RepositorioCliente, conn : connection ):
        self.repositorio_users = repositorio_users
        self.repositorio_clientes = repositorio_clientes
        self.conn = conn
        
    def register(self, email : str, nombre : str,_password : str):
        try:
            #incluir cerificacion de que el user con el mail no exista ya
            
            hashed_password = password.hash_password(_password)
            
            new_user = User(None, email, hashed_password, None)
            user = self.repositorio_users.guardar_user(new_user)
            
            cliente = Cliente(None, nombre)
            self.repositorio_clientes.guardar_cliente(cliente, user.id)
            
            return user
        
        except Exception:
            self.conn.rollback()
            raise
        