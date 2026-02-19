from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.infrastructure.db_config import conectar
from src.api.routers.pedidos_router import set_service
from src.api.routers.clientes_router import set_service
from src.api.routers import pedidos_router, clientes_router
from src.infrastructure.repositorio_clientes import RepositorioCliente
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.service.service_pedido import PedidoService
from src.service.service_cliente import ServiceCliente
from src.domain.exception import DomainException, NotFound

app = FastAPI()
app.include_router(pedidos_router.router)
app.include_router(clientes_router.router)

conn = conectar()

repositorio_clientes = RepositorioCliente(conn)
repositorio_pedidos = RepositorioPedidos(conn)
repositorio_productos = RepositorioProductos(conn)

repositorio_clientes.crear_tabla_clientes()
repositorio_pedidos.crear_tabla_pedidos()
repositorio_productos.crear_tabla_productos()
repositorio_pedidos.crear_tabla_items()

pedido_service = PedidoService(repositorio_pedidos, repositorio_productos, repositorio_clientes, conn)
cliente_service = ServiceCliente(repositorio_clientes, conn)

pedidos_router.set_service(pedido_service)
clientes_router.set_service(cliente_service)


#### handlers ########

@app.exception_handler(DomainException)
async def domain_exception_handler(request : Request, exc : DomainException):
    return JSONResponse(
        status_code = 400,
        content = {"detail" : str(exc)}
    )

@app.exception_handler(NotFound)
async def not_found_exception_handler(request : Request, exc : NotFound):
    return JSONResponse(
        status_code=404,
        content={"detail" : str(exc)}
    )
    
