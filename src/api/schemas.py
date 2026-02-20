from pydantic import BaseModel


class PedidoCreateRequest(BaseModel):
    cliente_id : int

class ClienteCreateRequest(BaseModel):
    nombre : str

class ProductoCreateRequest(BaseModel):
    nombre : str
    precio : int
    stock : int
    


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
    
class ClienteCreateResponse(BaseModel):
    id : int
    nombre : str
    
    @classmethod
    def from_domain(cls, cliente):
        return cls(
            id = cliente.id,
            nombre = cliente.nombre
        )

class ProductoCreateResponse(BaseModel):
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