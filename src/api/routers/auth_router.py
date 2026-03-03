from fastapi import APIRouter
from src.api.schemas import RegisterRequest, UserRegisted
from src.service.service_auth import AuthService
from src.infrastructure.repositorio_users import User

router = APIRouter(prefix="/auth", tags=["auth"])

service : AuthService= None
def set_service(_service):
    global service
    service = _service

@router.post("/register", response_model=UserRegisted)
def register(data : RegisterRequest):
    user = service.register(data.email, data.nombre,data.password)
    
    return UserRegisted(id = user.id,email= user.email,role= user.role)