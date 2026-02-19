from fastapi import APIRouter
from src.api.schemas import PedidoCreadoResponse, PedidoCreateRequest
from src.service.service_pedido import PedidoService

router = APIRouter(tags=["Pedidos"])

service : PedidoService= None
def set_service(_service):
    global service 
    service = _service

@router.post("/pedidos", status_code=201,response_model=PedidoCreadoResponse)
async def iniciar_pedido(data : PedidoCreateRequest):
    pedido = service.iniciar_pedido(data.cliente_id)
    
    return PedidoCreadoResponse.from_domain(pedido)

