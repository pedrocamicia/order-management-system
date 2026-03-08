from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.infrastructure.db_config import conectar
from src.api.routers import pedidos_router, clientes_router, productos_router, auth_router
from src.infrastructure.repositorio_clientes import RepositorioCliente
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.service.service_pedido import PedidoService
from src.service.service_cliente import ServiceCliente
from src.service.service_producto import ProductoService
from src.domain.exception import DomainException, NotFound, AuthException
from src.infrastructure.repositorio_users import RepositorioUser
from src.service.service_auth import AuthService
from src.api.dependencies import auth

app = FastAPI()
app.include_router(pedidos_router.router)
app.include_router(clientes_router.router)
app.include_router(productos_router.router)
app.include_router(auth_router.router)

conn = conectar()

repositorio_users = RepositorioUser(conn)
repositorio_clientes = RepositorioCliente(conn)
repositorio_pedidos = RepositorioPedidos(conn)
repositorio_productos = RepositorioProductos(conn)

repositorio_users.create_table()
repositorio_clientes.crear_tabla_clientes()
repositorio_pedidos.crear_tabla_pedidos()
repositorio_productos.crear_tabla_productos()
repositorio_pedidos.crear_tabla_items()

pedido_service = PedidoService(repositorio_pedidos, repositorio_productos, repositorio_clientes, conn)
cliente_service = ServiceCliente(repositorio_clientes, conn)
productos_service = ProductoService(repositorio_productos, conn)
auth_service = AuthService(repositorio_users , repositorio_clientes , conn)

pedidos_router.set_service(pedido_service)
clientes_router.set_service(cliente_service)
productos_router.set_service(productos_service)
auth_router.set_service(auth_service)
auth.set_service(auth_service)

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
    
@app.exception_handler(AuthException)
async def auth_exception_handler(request : Request, exc : AuthException):
    return JSONResponse(
        status_code=401,
        content= {"detail": str(exc)}
    )
