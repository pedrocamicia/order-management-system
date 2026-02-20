from fastapi import APIRouter
from src.api.schemas import PedidoCreadoResponse, PedidoCreateRequest, AgergarProductoAPedidoRequest, PedidoDetalleResponse
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

@router.post("/pedidos/{pedido_id}/items", status_code=201, response_model= PedidoDetalleResponse)
async def agregar_producto(data : AgergarProductoAPedidoRequest, pedido_id : int):
    
    pedido = service.agregar_producto(pedido_id, data.producto_id, data.cantidad)
    
    return PedidoDetalleResponse.from_domain(pedido)

@router.get("/pedidos/{pedido_id}", status_code=200, response_model=PedidoDetalleResponse)
def get_pedido(pedido_id : int):
    pedido = service.get_pedido(pedido_id)
    
    return PedidoDetalleResponse.from_domain(pedido)