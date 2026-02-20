from fastapi import APIRouter
from src.api.schemas import ClienteCreateRequest,ClienteCreateResponse
from src.service.service_cliente import ServiceCliente

router = APIRouter(tags=["Cllientes"])

service : ServiceCliente= None
def set_service(_service):
    global service
    service = _service
    

@router.post("/clientes", status_code=201, response_model= ClienteCreateResponse)
def crear_cliente(data: ClienteCreateRequest):
    cliente = service.crear_cliente(data.nombre)
    
    return ClienteCreateResponse.from_domain(cliente)