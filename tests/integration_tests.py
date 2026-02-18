import pytest
from datetime import datetime
from src.domain.pedido import Pedido, Carrito,Confirmado
from src.domain.producto import Producto, NoDisponible, Disponible
from src.domain.item_pedido import ItemPedido
from src.domain.cliente import Cliente
from src.domain.exception import ProductoNoDisponible, CantidadDeProductoNoDisponibleEnStock, CantidadInvalida,EstadoPedidoInvalido,PedidoVacioInvalido
from src.service.service_pedido import PedidoService
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.infrastructure.repositorio_clientes import RepositorioCliente
from src.infrastructure.db_config import conectar
from psycopg2.extensions import connection
    

def crear_contexto():
    conn : connection= conectar() 

    conn.autocommit = False
    
    repo_pedidos = RepositorioPedidos(conn)
    repo_productos = RepositorioProductos(conn)
    repo_clientes = RepositorioCliente(conn)
    repo_clientes.crear_tabla_clientes()
    repo_pedidos.crear_tabla_pedidos()
    repo_productos.crear_tabla_productos()
    repo_pedidos.crear_tabla_items()

    pedro = Cliente(None,"pedro") #id = 1
    repo_clientes.guardar_cliente(pedro)
    
    pedido = Pedido(None, 1)    #id = 1
    repo_pedidos.crear_pedido(pedido)
    
    pedido2 = Pedido(None, 1)  #id = 2
    pedido2.estado = Confirmado()
    repo_pedidos.crear_pedido(pedido2)
    
    banana = Producto(None, "banana",10, 20) #id = 1
    repo_productos.guardar_producto(banana)
    
    manzana = Producto(None, "manzana", 5, 15) #id = 2
    repo_productos.guardar_producto(manzana)
    
    p_no_disponible = Producto(None, "un producto", 3, 99) #id = 3
    p_no_disponible.estado = NoDisponible()
    repo_productos.guardar_producto(p_no_disponible)
    
    return conn, repo_pedidos, repo_productos, PedidoService(repo_pedidos, repo_productos, conn)



def limpiar_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE items, pedidos, productos, clientes RESTART IDENTITY CASCADE")              

        conn.commit()


############################################################################################ 
 
def test_agregar_producto_a_pedido():
    try:
        conn, repo_pedidos, repo_productos, pedido_service = crear_contexto()
        
        pedido_service.agregar_producto(1, 1, 5)

        pedido_modificado = repo_pedidos.get_pedido(1)
        
        assert pedido_modificado.items[0].cantidad == 5
        assert pedido_modificado.items[0].precio_unitario == 10
        assert pedido_modificado.items[0].producto_id == 1
        
        pedido_service.agregar_producto(1, 1, 10)
        pedido_service.agregar_producto(1,2,1)
        
        pedido_modificado2 = repo_pedidos.get_pedido(1)

        
        assert len(pedido_modificado2.items) == 2
        assert pedido_modificado2.items[0].cantidad == 15
        assert pedido_modificado2.items[0].precio_unitario == 10
        assert pedido_modificado2.items[1].producto_id == 2
        assert pedido_modificado2.total() == 155
        assert pedido_modificado2.cantidad_de_productos() == 16
        
    finally:
        limpiar_db(conn)
        
        

def test_agregar_producto_cantidad_0_o_negativa_falla():
    try:
        conn, repo_pedidos, repo_productos, pedido_service = crear_contexto()
        
        with pytest.raises(CantidadInvalida):
            pedido_service.agregar_producto(1, 1, 0)
        with pytest.raises(CantidadInvalida):
            pedido_service.agregar_producto(1, 1, -5)
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_agregar_producto_no_disponible_falla():
    try:
        conn, repo_pedidos, repo_productos, pedido_service = crear_contexto()
        
        with pytest.raises(ProductoNoDisponible):
            pedido_service.agregar_producto(1, 3, 5)

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_agregar_producto_cantidad_mayor_a_stock_falla():
    try:
        conn, repo_pedidos, repo_productos, pedido_service = crear_contexto()
        
        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.agregar_producto(1, 2, 16)

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        

def test_agregar_producto_a_pedido_confirmado_falla():
    try:
        conn, repo_pedidos, repo_productos, pedido_service = crear_contexto()
        
        with pytest.raises(EstadoPedidoInvalido):
            pedido_service.agregar_producto(2, 2, 1)

            
        pedido = repo_pedidos.get_pedido(2)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
