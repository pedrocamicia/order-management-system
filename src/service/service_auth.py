from src.infrastructure.repositorio_users import RepositorioUser,User
from src.infrastructure.repositorio_clientes import RepositorioCliente,Cliente
from psycopg2.extensions import connection
from src.infrastructure.security import password, jwt_handler
from src.domain.exception import ExistentEmailError, InvalidCredentials,UserNotFound


class AuthService:
    def __init__(self, repositorio_users : RepositorioUser,repositorio_clientes : RepositorioCliente, conn : connection ):
        self.repositorio_users = repositorio_users
        self.repositorio_clientes = repositorio_clientes
        self.conn = conn
       
    ################################################   
        
    def register(self, email : str, nombre : str,_password : str):
        try:
            _user = self.repositorio_users.get_user_by_mail(email)
            if _user:
                raise ExistentEmailError("el mail ingersado ya se encuentra registrado en otra cuenta")
            
            hashed_password = password.hash_password(_password)
            
            new_user = User(None, email, hashed_password, None)
            user = self.repositorio_users.guardar_user(new_user)
            
            cliente = Cliente(None, nombre)
            self.repositorio_clientes.guardar_cliente(cliente, user.id)
            
            return user
        
        except Exception:
            self.conn.rollback()
            raise
        
        
    ##############################################
    
    def login(self, email : str, _password : str):
        
        user = self.repositorio_users.get_user_by_mail(email)
        if not user:
            raise InvalidCredentials("credenciales invalidas")
        
        password_valid = password.verify_password(_password, user.hashed_password)
        
        if not password_valid:
            raise InvalidCredentials("credenciales invalidas")


        access_token = jwt_handler.create_access_token(user.id)
        refresh_token = jwt_handler.create_refresh_token(user.id)
        
        return access_token, refresh_token
    
    #############################################################
    
    def get_user(self, id):
        try:
            user = self.repositorio_users.get_user_by_id(id)
            
            if user is None:
                raise UserNotFound("usuario no encontrado")
            
            return user
        except Exception:
            raise 
      
    #################################################################
    
    def refresh_token(self, refresh_token : str):
        try:
            payload = jwt_handler.decode_access_token(refresh_token)
            
            if payload.get("type") != "refresh":
                raise InvalidCredentials("token invalido")
            
            user_id = int(payload["sub"])
                    
            new_access_token = jwt_handler.create_access_token(user_id)
            
            return new_access_token
        
        except:
            raise