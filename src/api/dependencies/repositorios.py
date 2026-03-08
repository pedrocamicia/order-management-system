from src.infrastructure.repositorio_clientes import RepositorioCliente
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.infrastructure.repositorio_users import RepositorioUser
from fastapi import Depends
from .db import get_db

def get_repositorio_clientes(conn = Depends(get_db)):
    return RepositorioCliente(conn)

def get_repositorio_pedidos(conn = Depends(get_db)):
    return RepositorioPedidos(conn)

def get_repositorio_productos(conn = Depends(get_db)):
    return RepositorioProductos(conn)

def get_repositorio_users(conn = Depends(get_db)):
    return RepositorioUser(conn)