from fastapi import APIRouter
from src.api.schemas import RegisterRequest, UserResponse,LoginRequest,LoginResponse
from src.service.service_auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

service : AuthService= None
def set_service(_service):
    global service
    service = _service

@router.post("/register", response_model=UserResponse)
def register(data : RegisterRequest):
    user = service.register(data.email, data.nombre,data.password)
    
    return UserResponse(
        id = user.id,
        email= user.email,
        role= user.role
    )


@router.post("/login", response_model=LoginResponse)
def login(data : LoginRequest):
    
    access_token, refresh_token = service.login(data.email, data.password) 
    
    return LoginResponse(
        access_token= access_token,
        refresh_token=refresh_token
    )
    

