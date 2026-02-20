from pydantic import BaseModel
from src.domain.pedido import Pedido
from src.domain.item_pedido import ItemPedido

class PedidoCreateRequest(BaseModel):
    cliente_id : int

class ClienteCreateRequest(BaseModel):
    nombre : str

class ProductoCreateRequest(BaseModel):
    nombre : str
    precio : int
    stock : int
    
class AgergarProductoAPedidoRequest(BaseModel):
    producto_id : int
    cantidad : int

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
    producto_id : int
    cantidad : int
    precio_unitario : int
    
    @classmethod
    def from_domain(cls, item : ItemPedido):
        return cls(
            producto_id = item.producto_id,
            cantidad = item.cantidad,
            precio_unitario = item.precio_unitario
        )
    
    
class PedidoDetalleResponse(BaseModel):
    id : int
    estado : str
    cliente_id : int
    items : list[ItemResponse]
    total : float
    
    @classmethod
    def from_domain(cls, pedido : Pedido):
        return cls(
            id = pedido.id,
            estado = pedido.estado.codigo(),
            cliente_id = pedido.cliente_id,
            items = [ItemResponse.from_domain(item) for item in pedido.items],
            total = pedido.total()
        )
    
    
class ClienteResponse(BaseModel):
    id : int
    nombre : str
    
    @classmethod
    def from_domain(cls, cliente):
        return cls(
            id = cliente.id,
            nombre = cliente.nombre
        )

class ProductoResponse(BaseModel):
    id : int
    nombre : str
    precio : int
    stock : int 
    estado : str
    
    @classmethod
    def from_domain(cls, producto):
        return cls(
            id = producto.id,
            nombre = producto.nombre,
            precio = producto.precio,
            stock = producto.stock,
            estado = producto.estado.codigo()
        )
        
    