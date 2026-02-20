from fastapi import APIRouter
from src.api.schemas import ProductoCreateResponse, ProductoCreateRequest
from src.service.service_producto import ProductoService

router = APIRouter(tags=["Productos"])

service : ProductoService = None
def set_service(_service):
    global service
    service = _service
    

@router.post("/productos", status_code=201, response_model=ProductoCreateResponse)
def crear_producto(data : ProductoCreateRequest):
    producto = service.crear_producto(data.nombre, data.precio, data.stock)
    
    return ProductoCreateResponse.from_domain(producto)