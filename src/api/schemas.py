from pydantic import BaseModel


class PedidoCreateRequest(BaseModel):
    cliente_id : int



##### response


class PedidoCreadoResponse(BaseModel):
    id : int
    estado : str
    cliente_id : int

    @classmethod
    def from_domain(cls, pedido):
        return cls(
            id = pedido.id,
            estado = pedido.estado.codigo(),
            cliente_id = pedido.cliente_id
        )
        
        
class ItemResponse(BaseModel):
    producto_id : str
    cantidad : int
    precio_unitario : int
    
class PedidoDetalleResponse(BaseModel):
    id : int
    estado : str
    cliente_id : str
    items : list[ItemResponse]
    total : float
    
