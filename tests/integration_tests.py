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
    
    conn.commit()
    
    return conn, repo_pedidos, repo_productos,repo_clientes, PedidoService(repo_pedidos, repo_productos,repo_clientes, conn)



def limpiar_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE items, pedidos, productos, clientes RESTART IDENTITY CASCADE")              

        conn.commit()


############################################################################################ 
 
def test_modificar_items_pedido_a_pedido():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido (1, 1, 5)

        pedido_modificado = repo_pedidos.get_pedido(1)
        
        assert pedido_modificado.items[0].cantidad == 5
        assert pedido_modificado.items[0].precio_unitario == 10
        assert pedido_modificado.items[0].producto_id == 1
        
        pedido_service.modificar_items_pedido (1, 1, 10)
        pedido_service.modificar_items_pedido (1,2,1)
        
        pedido_modificado2 = repo_pedidos.get_pedido(1)

        
        assert len(pedido_modificado2.items) == 2
        assert pedido_modificado2.items[0].cantidad == 10
        assert pedido_modificado2.items[0].precio_unitario == 10
        assert pedido_modificado2.items[1].producto_id == 2
        assert pedido_modificado2.total() == 105
        assert pedido_modificado2.cantidad_de_productos() == 11
        
    finally:
        limpiar_db(conn)
        
        

def test_modificar_items_pedido_cantidad_negativa_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        

        with pytest.raises(CantidadInvalida):
            pedido_service.modificar_items_pedido (1, 1, -5)
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_modificar_items_pedido_producto_no_disponible_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(ProductoNoDisponible):
            pedido_service.modificar_items_pedido(1, 3, 5)

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_modificar_items_pedido_a_cantidad_mayor_a_stock_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.modificar_items_pedido(1, 2, 16)

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        

def test_modificar_items_pedido_a_pedido_confirmado_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(EstadoPedidoInvalido):
            pedido_service.modificar_items_pedido(2, 2, 1)

            
        pedido = repo_pedidos.get_pedido(2)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
def test_modificar_con_cantidad_0_elimina_item():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3)

        pedido = pedido_service.get_pedido(1)
        assert pedido.items[0].cantidad == 3
        
        pedido_service.modificar_items_pedido(1, 1, 0)
            
        pedido_actualizado = pedido_service.get_pedido(1)
        
        assert len(pedido_actualizado.items) == 0
        assert pedido_actualizado.total() == 0
        
    finally:
        limpiar_db(conn)
        
def test_modificar_item_existente_en_pedido_falla_por_stock():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3)

        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.modificar_items_pedido(1, 1, 999)
            
        pedido = pedido_service.get_pedido(1)
        assert pedido.items[0].cantidad == 3
        
    finally:
        limpiar_db(conn)
        
        
def test_modificar_item_existente_reduce_cantidad_en_pedido():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3)

        pedido_service.modificar_items_pedido(1, 1, 2)
            
        pedido = pedido_service.get_pedido(1)
        assert pedido.items[0].cantidad == 2
        
    finally:
        limpiar_db(conn)
    
def test_modificar_items_pedido_con_pedido_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import PedidoNoExistenteError
        with pytest.raises(PedidoNoExistenteError):
            pedido_service.modificar_items_pedido(999, 1, 1)

    finally:
        limpiar_db(conn)


def test_modificar_items_pedido_con_producto_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import ProductoNoExistenteError
        with pytest.raises(ProductoNoExistenteError):
            pedido_service.modificar_items_pedido(1, 999, 1)

    finally:
        limpiar_db(conn)


def test_modificar_items_pedido_pisa_cantidad_sin_acumular_varias_veces():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido_service.modificar_items_pedido(1, 1, 7)
        pedido_service.modificar_items_pedido(1, 1, 2)
        pedido_service.modificar_items_pedido(1, 1, 6)

        pedido = pedido_service.get_pedido(1)
        assert len(pedido.items) == 1
        assert pedido.items[0].producto_id == 1
        assert pedido.items[0].cantidad == 6
        assert pedido.total() == 60

    finally:
        limpiar_db(conn)
######## confirmar pedido ###################################################

def test_confirmar_pedido():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1,1,10) 
        pedido_service.modificar_items_pedido(1,2,5)

        pedido_service.confirmar_pedido(1)
        
        pedido = repo_pedidos.get_pedido(1)
        
        assert isinstance(pedido.estado, Confirmado)
        assert pedido.fecha_confirmacion is not None
        assert pedido.total() == 125
        
        banana = repo_productos.get_producto(1)
        manzana = repo_productos.get_producto(2)
        
        assert banana.stock == 10
        assert manzana.stock == 10
        
    finally:
        limpiar_db(conn)


def test_confirmar_pedido_con_producto_no_disponible_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1,1,10) 
        pedido_service.modificar_items_pedido(1,2,5)

        #### seteo manzana no disponible
        manzana = repo_productos.get_producto(2)
        manzana.estado = NoDisponible()
        repo_productos.actualizar_producto(manzana)
        ####
        
        with pytest.raises(ProductoNoDisponible):
            pedido_service.confirmar_pedido(1)
        
        pedido = repo_pedidos.get_pedido(1)
        
        assert isinstance(pedido.estado, Carrito)
        assert pedido.fecha_confirmacion is None
        assert pedido.total() == 125
        
        banana = repo_productos.get_producto(1)
        manzana = repo_productos.get_producto(2)
        
        assert banana.stock == 20
        assert manzana.stock == 15
        
    finally:
        limpiar_db(conn)


def test_confirmar_pedido_falta_stock_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1,1,10) 
        pedido_service.modificar_items_pedido(1,2,5)

        #### descontar stock de manzana
        manzana = repo_productos.get_producto(2)
        manzana.descontar_stock(11)
        repo_productos.actualizar_producto(manzana)
        ############
        
        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.confirmar_pedido(1)

        pedido = repo_pedidos.get_pedido(1)
        
        assert isinstance(pedido.estado, Carrito)
        assert pedido.fecha_confirmacion is None
        assert pedido.total() == 125
        
        banana = repo_productos.get_producto(1)
        
        assert banana.stock == 20
        
    finally:
        limpiar_db(conn)
        
    
        
def test_confirmar_pedido_vacio_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(PedidoVacioInvalido):
            pedido_service.confirmar_pedido(1)

        pedido = repo_pedidos.get_pedido(1)
        
        assert isinstance(pedido.estado, Carrito)
        assert pedido.fecha_confirmacion is None
        assert pedido.total() == 0
        
        banana = repo_productos.get_producto(1)
        manzana_actualizada = repo_productos.get_producto(2)
        
        assert banana.stock == 20
        assert manzana_actualizada.stock == 15
        
    finally:
        limpiar_db(conn)
        
def test_confirmar_pedido_confirmado_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1,1,5)
        
        pedido_service.confirmar_pedido(1)
        
        with pytest.raises(EstadoPedidoInvalido):
            pedido_service.confirmar_pedido(1)

        pedido = repo_pedidos.get_pedido(1)
        
        assert isinstance(pedido.estado, Confirmado)
        assert pedido.fecha_confirmacion is not None
        assert pedido.total() == 50
        
        banana = repo_productos.get_producto(1)
        manzana = repo_productos.get_producto(2)
        
        assert banana.stock == 15
        assert manzana.stock == 15
        
    finally:
        limpiar_db(conn)
        
        
########### not found #######

def test_get_pedido_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import PedidoNoExistenteError
        with pytest.raises(PedidoNoExistenteError):
            pedido_service.get_pedido(999)

    finally:
        limpiar_db(conn)


########## iniciar pedido #############
  
def test_iniciar_pedido_cliente_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import ClienteNoExistente
        with pytest.raises(ClienteNoExistente):
            pedido_service.iniciar_pedido(999)

    finally:
        limpiar_db(conn)
        
def test_iniciar_pedido_con_exito():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido = pedido_service.iniciar_pedido(1)

        assert pedido.id is not None
        assert pedido.cliente_id == 1
        assert isinstance(pedido.estado, Carrito)
        assert pedido.fecha_confirmacion is None
        assert len(pedido.items) == 0
        assert pedido.total() == 0

        pedido_guardado = repo_pedidos.get_pedido(pedido.id)
        assert pedido_guardado.id == pedido.id
        assert pedido_guardado.cliente_id == 1
        assert isinstance(pedido_guardado.estado, Carrito)
        assert pedido_guardado.fecha_confirmacion is None
        assert len(pedido_guardado.items) == 0

    finally:
        limpiar_db(conn)