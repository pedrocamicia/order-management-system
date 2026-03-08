from fastapi import Depends
from src.service.service_producto import ProductoService
from src.service.service_auth import AuthService
from src.service.service_cliente import ServiceCliente
from src.service.service_pedido import PedidoService
from .repositorios import get_repositorio_clientes, get_repositorio_pedidos, get_repositorio_productos, get_repositorio_users, get_db

def get_cliente_service(repositorio = Depends(get_repositorio_clientes), conn = Depends(get_db)):
    return ServiceCliente(repositorio, conn)

def get_producto_service(repositorio = Depends(get_repositorio_productos), conn = Depends(get_db)):
    return ProductoService(repositorio, conn)

def get_auth_service(repositorio_users = Depends(get_repositorio_users), repo_clientes = Depends(get_repositorio_clientes) ,conn = Depends(get_db)):
    return PedidoService(repositorio_users,repo_clientes,conn)

def get_pedidos_service(repo_pedidos = Depends(get_repositorio_pedidos), repo_productos = Depends(get_repositorio_productos), repo_clientes = Depends(get_repositorio_clientes),conn = Depends(get_db)):
    return PedidoService(repo_pedidos,repo_productos, repo_clientes, conn)