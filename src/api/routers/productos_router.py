from fastapi import APIRouter
from src.api.schemas import ProductoResponse, ProductoCreateRequest
from src.service.service_producto import ProductoService

router = APIRouter(tags=["Productos"])

service : ProductoService = None
def set_service(_service):
    global service
    service = _service
    

@router.post("/productos", status_code=201, response_model=ProductoResponse)
def crear_producto(data : ProductoCreateRequest):
    producto = service.crear_producto(data.nombre, data.precio, data.stock)
    
    return ProductoResponse.from_domain(producto)

@router.get("/productos/{producto_id}", status_code=200, response_model=ProductoResponse)
def get_producto(producto_id : int):
    producto = service.get_producto(producto_id)
    
    return ProductoResponse.from_domain(producto)