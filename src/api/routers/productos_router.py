from fastapi import APIRouter
from src.api.schemas import ProductoResponse, ProductoCreateRequest,ProductoPaginationResponse
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

@router.get("/productos", status_code=200, response_model= ProductoPaginationResponse) #agregar: que pasa si no hay registros. y que pasa si page > pages_total
def get_productos(page : int, limit : int):
    
    productos,total,total_pages = service.get_productos(page, limit)
    
    return ProductoPaginationResponse(
        productos = [ProductoResponse.from_domain(producto) for producto in productos],
        total = total,
        page = page,
        limit = limit,
        total_pages = total_pages
    )