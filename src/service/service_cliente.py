from src.infrastructure.repositorio_clientes import RepositorioCliente
from psycopg2.extensions import connection


class ServiceCliente:
    def __init__(self, repositorio_cliente : RepositorioCliente, conn : connection):
        pass