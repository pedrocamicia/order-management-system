from src.infrastructure.security import jwt_handler
from src.api.routers.auth_router import service #ESTO SE DEBE CAMBIAR. LUEGO CENTRALIZAR TODO CON DEPENDENCIAS  
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

service = None
def set_service(_service):
    global service
    service = _service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : str = Depends(oauth2_scheme)):
    
    payload = jwt_handler.decode_access_token(token)
        
    user_id = int(payload["sub"])

    user = service.get_user(user_id)
    
    return user

