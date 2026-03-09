from fastapi import APIRouter, Depends
from src.api.schemas import PedidoCreadoResponse, ModificarItemsPedidoRequest, PedidoDetalleResponse
from src.service.service_pedido import PedidoService
from src.domain.user import User
from src.api.dependencies.auth import get_current_user

router = APIRouter(tags=["Pedidos"])

service : PedidoService= None
def set_service(_service):
    global service 
    service = _service

@router.post("/pedidos", status_code=200,response_model=PedidoCreadoResponse)
async def iniciar_pedido(user : User = Depends(get_current_user)):
    pedido = service.iniciar_pedido(user.id)
    
    return PedidoCreadoResponse.from_domain(pedido)


@router.patch("/pedidos/{pedido_id}/items", status_code=201, response_model= PedidoDetalleResponse)
async def modificar_items_pedido(data : ModificarItemsPedidoRequest, pedido_id : int, user : User= Depends(get_current_user)):
        
    pedido = service.modificar_items_pedido(pedido_id, data.producto_id, data.cantidad, user.id)
    
    return PedidoDetalleResponse.from_domain(pedido)


@router.get("/pedidos/{pedido_id}", status_code=200, response_model=PedidoDetalleResponse)
def get_pedido(pedido_id : int):
    pedido = service.get_pedido(pedido_id)
    
    return PedidoDetalleResponse.from_domain(pedido)

@router.patch("/pedidos/{pedido_id}/confirmar", status_code=200, response_model=PedidoDetalleResponse)
def confirmar_pedido(pedido_id : int):
    pedido = service.confirmar_pedido(pedido_id)
    
    return PedidoDetalleResponse.from_domain(pedido)

@router.delete("/pedidos/{pedido_id}/items/{producto_id}", status_code= 204)
def eliminar_item(pedido_id : int, producto_id : int):
    service.eliminar_item(pedido_id, producto_id)
    return