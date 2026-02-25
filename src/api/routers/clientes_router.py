from fastapi import APIRouter
from src.api.schemas import ClienteCreateRequest,ClienteResponse,PaginationResponse
from src.service.service_cliente import ServiceCliente

router = APIRouter(tags=["Cllientes"])

service : ServiceCliente= None
def set_service(_service):
    global service
    service = _service
    

@router.post("/clientes", status_code=201, response_model= ClienteResponse)
def crear_cliente(data: ClienteCreateRequest):
    cliente = service.crear_cliente(data.nombre)
    
    return ClienteResponse.from_domain(cliente)

@router.get("/clientes/{cliente_id}", status_code=200, response_model=ClienteResponse)
def get_cliente(cliente_id : int):
    cliente = service.get_cliente(cliente_id)
    
    return ClienteResponse.from_domain(cliente)

@router.get("/clientes", status_code=200,response_model=PaginationResponse[ClienteResponse])
def get_clientes(limit : int, page : int, nombre : str | None = None):
    _page = service.get_clientes(limit, page, nombre)
    
    return PaginationResponse(
        items = [ClienteResponse.from_domain(cliente) for cliente in _page.items],
        total = _page.total,
        page = _page.page,
        limit = _page.limit,
        total_pages = _page.total_pages
    )