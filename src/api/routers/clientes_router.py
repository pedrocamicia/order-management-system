from fastapi import APIRouter, Depends
from src.api.schemas import ClienteCreateRequest,ClienteResponse,PaginationResponse
from src.service.service_cliente import ServiceCliente
from src.api.dependencies.auth import get_current_user

router = APIRouter(tags=["Cllientes"])

service : ServiceCliente= None
def set_service(_service):
    global service
    service = _service

@router.get("/clientes/{cliente_id}", status_code=200, response_model=ClienteResponse)
def get_cliente(cliente_id : int, user = Depends(get_current_user)):
    cliente = service.get_cliente(cliente_id, user)
    
    return ClienteResponse.from_domain(cliente)

@router.get("/clientes", status_code=200,response_model=PaginationResponse[ClienteResponse])
def get_clientes(limit : int, page : int, nombre : str | None = None, user = Depends(get_current_user)):
    _page = service.get_clientes(limit, page, nombre, user)
    
    return PaginationResponse(
        items = [ClienteResponse.from_domain(cliente) for cliente in _page.items],
        total = _page.total,
        page = _page.page,
        limit = _page.limit,
        total_pages = _page.total_pages
    )