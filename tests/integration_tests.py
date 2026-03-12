import pytest
from datetime import datetime
from src.domain.pedido import Pedido, Carrito,Confirmado
from src.domain.producto import Producto, NoDisponible, Disponible
from src.domain.item_pedido import ItemPedido
from src.domain.cliente import Cliente
from src.domain.exception import ProductoNoDisponible, CantidadDeProductoNoDisponibleEnStock, CantidadInvalida,EstadoPedidoInvalido,PedidoVacioInvalido, NoEsDuenoDeRecursoError, AuthorizationError
from src.service.service_pedido import PedidoService
from src.service.service_cliente import ServiceCliente
from src.service.service_producto import ProductoService
from src.infrastructure.repositorio_pedidos import RepositorioPedidos
from src.infrastructure.repositorio_productos import RepositorioProductos
from src.infrastructure.repositorio_clientes import RepositorioCliente
from src.infrastructure.db_config import conectar
from psycopg2.extensions import connection
from src.infrastructure.repositorio_users import RepositorioUser
from src.domain.user import User

CLIENTE_PEDRO_ID = 1
CLIENTE_JUAN_ID = 2
USER_PEDRO_ID = 1
USER_JUAN_ID = 2
USER_ADMIN_ID = 3


def build_user_pedro():
    return User(USER_PEDRO_ID, "mail", "1234", "customer")


def build_user_juan():
    return User(USER_JUAN_ID, "mail2", "1234", "customer")


def build_user_admin():
    return User(USER_ADMIN_ID, "admin@mail", "1234", "admin")


def build_user_inexistente():
    return User(999, "ghost@mail", "1234", "customer")

def crear_contexto():
    conn : connection= conectar() 

    conn.autocommit = False
    
    repo_users = RepositorioUser(conn)
    repo_pedidos = RepositorioPedidos(conn)
    repo_productos = RepositorioProductos(conn)
    repo_clientes = RepositorioCliente(conn)
    repo_users.create_table()
    repo_clientes.crear_tabla_clientes()
    repo_pedidos.crear_tabla_pedidos()
    repo_productos.crear_tabla_productos()
    repo_pedidos.crear_tabla_items()

    _user_pedro = User(None, "mail", "1234", None)
    user_pedro = repo_users.guardar_user(_user_pedro)

    _pedro = Cliente(None,"pedro") #id = 1
    pedro = repo_clientes.guardar_cliente(_pedro, user_pedro.id)

    _user_juan = User(None, "mail2", "1234", None)
    user_juan = repo_users.guardar_user(_user_juan)

    _juan = Cliente(None, "juan") #id = 2
    repo_clientes.guardar_cliente(_juan, user_juan.id)

    _admin = User(None, "admin@mail", "1234", None)
    admin = repo_users.guardar_user(_admin)
    admin.role = "admin"
    with conn.cursor() as cursor:
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", ("admin", admin.id))
    
    pedido = Pedido(None, pedro.id)    #id = 1
    repo_pedidos.crear_pedido(pedido)
    
    pedido2 = Pedido(None, pedro.id)  #id = 2
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
        cursor.execute("TRUNCATE TABLE users,items, pedidos, productos, clientes RESTART IDENTITY CASCADE")              

        conn.commit()


############################################################################################ 
 
def test_modificar_items_pedido_a_pedido():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 5, build_user_pedro())

        pedido_modificado = repo_pedidos.get_pedido(1)
        
        assert pedido_modificado.items[0].cantidad == 5
        assert pedido_modificado.items[0].precio_unitario == 10
        assert pedido_modificado.items[0].producto_id == 1
        
        pedido_service.modificar_items_pedido(1, 1, 10, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 1, build_user_pedro())
        
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
            pedido_service.modificar_items_pedido(1, 1, -5, build_user_pedro())
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_modificar_items_pedido_producto_no_disponible_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(ProductoNoDisponible):
            pedido_service.modificar_items_pedido(1, 3, 5, build_user_pedro())

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
        
def test_modificar_items_pedido_a_cantidad_mayor_a_stock_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.modificar_items_pedido(1, 2, 16, build_user_pedro())

            
        pedido = repo_pedidos.get_pedido(1)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        

def test_modificar_items_pedido_a_pedido_confirmado_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        with pytest.raises(EstadoPedidoInvalido):
            pedido_service.modificar_items_pedido(2, 2, 1, build_user_pedro())

            
        pedido = repo_pedidos.get_pedido(2)
        
        assert len(pedido.items) == 0
        assert pedido.total() == 0
        
    finally:
        limpiar_db(conn)
        
        
def test_modificar_con_cantidad_0_elimina_item():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3, build_user_pedro())

        pedido = pedido_service.get_pedido(1, build_user_pedro())
        assert pedido.items[0].cantidad == 3
        
        pedido_service.modificar_items_pedido(1, 1, 0, build_user_pedro())
            
        pedido_actualizado = pedido_service.get_pedido(1, build_user_pedro())
        
        assert len(pedido_actualizado.items) == 0
        assert pedido_actualizado.total() == 0
        
    finally:
        limpiar_db(conn)
        
def test_modificar_item_existente_en_pedido_falla_por_stock():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3, build_user_pedro())

        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.modificar_items_pedido(1, 1, 999, build_user_pedro())
            
        pedido = pedido_service.get_pedido(1, build_user_pedro())
        assert pedido.items[0].cantidad == 3
        
    finally:
        limpiar_db(conn)
        
        
def test_modificar_item_existente_reduce_cantidad_en_pedido():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes,pedido_service = crear_contexto()
        
        pedido_service.modificar_items_pedido(1, 1, 3, build_user_pedro())

        pedido_service.modificar_items_pedido(1, 1, 2, build_user_pedro())
            
        pedido = pedido_service.get_pedido(1, build_user_pedro())
        assert pedido.items[0].cantidad == 2
        
    finally:
        limpiar_db(conn)
    
def test_modificar_items_pedido_con_pedido_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import PedidoNoExistenteError
        with pytest.raises(PedidoNoExistenteError):
            pedido_service.modificar_items_pedido(999, 1, 1, build_user_pedro())

    finally:
        limpiar_db(conn)


def test_modificar_items_pedido_con_producto_inexistente_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        from src.domain.exception import ProductoNoExistenteError
        with pytest.raises(ProductoNoExistenteError):
            pedido_service.modificar_items_pedido(1, 999, 1, build_user_pedro())

    finally:
        limpiar_db(conn)


def test_modificar_items_pedido_pisa_cantidad_sin_acumular_varias_veces():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido_service.modificar_items_pedido(1, 1, 7, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 1, 2, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 1, 6, build_user_pedro())

        pedido = pedido_service.get_pedido(1, build_user_pedro())
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
        
        pedido_service.modificar_items_pedido(1, 1, 10, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 5, build_user_pedro())

        pedido_service.confirmar_pedido(1, build_user_pedro())
        
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
        
        pedido_service.modificar_items_pedido(1, 1, 10, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 5, build_user_pedro())

        #### seteo manzana no disponible
        manzana = repo_productos.get_producto(2)
        manzana.estado = NoDisponible()
        repo_productos.actualizar_producto(manzana)
        ####
        
        with pytest.raises(ProductoNoDisponible):
            pedido_service.confirmar_pedido(1, build_user_pedro())
        
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
        
        pedido_service.modificar_items_pedido(1, 1, 10, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 5, build_user_pedro())

        #### descontar stock de manzana
        manzana = repo_productos.get_producto(2)
        manzana.descontar_stock(11)
        repo_productos.actualizar_producto(manzana)
        ############
        
        with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
            pedido_service.confirmar_pedido(1, build_user_pedro())

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
            pedido_service.confirmar_pedido(1, build_user_pedro())

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
        
        pedido_service.modificar_items_pedido(1, 1, 5, build_user_pedro())
        
        pedido_service.confirmar_pedido(1, build_user_pedro())
        
        with pytest.raises(EstadoPedidoInvalido):
            pedido_service.confirmar_pedido(1, build_user_pedro())

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
            pedido_service.get_pedido(999, build_user_pedro())

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
        
############### eliminar item #################

def test_eliminar_item():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido_service.modificar_items_pedido(1, 1, 3, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 2, build_user_pedro())

        pedido_service.eliminar_item(1, 1, build_user_pedro())

        pedido_actualizado = repo_pedidos.get_pedido(1)
        assert len(pedido_actualizado.items) == 1
        assert pedido_actualizado.items[0].producto_id == 2
        assert pedido_actualizado.items[0].cantidad == 2
        assert pedido_actualizado.total() == 10

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM items WHERE pedido_id = %s AND producto_id = %s",
                (1, 1),
            )
            cantidad_items_producto_eliminado = cursor.fetchone()[0]

        assert cantidad_items_producto_eliminado == 0

    finally:
        limpiar_db(conn)


def test_modificar_items_pedido_con_cliente_que_no_es_dueno_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        with pytest.raises(NoEsDuenoDeRecursoError):
            pedido_service.modificar_items_pedido(1, 1, 3, build_user_inexistente())

        pedido = repo_pedidos.get_pedido(1)
        assert len(pedido.items) == 0
        assert pedido.total() == 0

    finally:
        limpiar_db(conn)


def test_get_pedido_con_cliente_que_no_es_dueno_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        with pytest.raises(NoEsDuenoDeRecursoError):
            pedido_service.get_pedido(1, build_user_inexistente())

    finally:
        limpiar_db(conn)


def test_confirmar_pedido_con_cliente_que_no_es_dueno_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido_service.modificar_items_pedido(1, 1, 5, build_user_pedro())

        with pytest.raises(NoEsDuenoDeRecursoError):
            pedido_service.confirmar_pedido(1, build_user_inexistente())

        pedido = repo_pedidos.get_pedido(1)
        assert isinstance(pedido.estado, Carrito)
        assert pedido.fecha_confirmacion is None

        banana = repo_productos.get_producto(1)
        assert banana.stock == 20

    finally:
        limpiar_db(conn)


def test_eliminar_item_con_cliente_que_no_es_dueno_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()

        pedido_service.modificar_items_pedido(1, 1, 3, build_user_pedro())
        pedido_service.modificar_items_pedido(1, 2, 2, build_user_pedro())

        with pytest.raises(NoEsDuenoDeRecursoError):
            pedido_service.eliminar_item(1, 1, build_user_inexistente())

        pedido_actualizado = repo_pedidos.get_pedido(1)
        assert len(pedido_actualizado.items) == 2
        assert pedido_actualizado.total() == 40

    finally:
        limpiar_db(conn)


######## clientes ###########################################################

def test_get_cliente_dueno_puede_ver_su_perfil():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        cliente_service = ServiceCliente(repo_clientes, conn)
        user_pedro = build_user_pedro()

        cliente = cliente_service.get_cliente(CLIENTE_PEDRO_ID, user_pedro)

        assert cliente.id == CLIENTE_PEDRO_ID
        assert cliente.nombre == "pedro"

    finally:
        limpiar_db(conn)


def test_get_cliente_no_dueno_no_admin_falla():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        cliente_service = ServiceCliente(repo_clientes, conn)
        user_juan = build_user_juan()

        with pytest.raises(NoEsDuenoDeRecursoError):
            cliente_service.get_cliente(CLIENTE_PEDRO_ID, user_juan)

    finally:
        limpiar_db(conn)


def test_get_cliente_admin_puede_ver_cualquier_perfil():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        cliente_service = ServiceCliente(repo_clientes, conn)
        admin = build_user_admin()

        cliente = cliente_service.get_cliente(CLIENTE_PEDRO_ID, admin)

        assert cliente.id == CLIENTE_PEDRO_ID
        assert cliente.nombre == "pedro"

    finally:
        limpiar_db(conn)


def test_get_clientes_admin_puede_listar():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        cliente_service = ServiceCliente(repo_clientes, conn)
        admin = build_user_admin()

        page = cliente_service.get_clientes(10, 1, None, admin)

        assert page.total == 2
        assert page.page == 1
        assert page.limit == 10
        assert len(page.items) == 2
        assert page.items[0].nombre == "pedro"
        assert page.items[1].nombre == "juan"

    finally:
        limpiar_db(conn)


def test_get_clientes_customer_falla_por_autorizacion():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        cliente_service = ServiceCliente(repo_clientes, conn)
        user_pedro = build_user_pedro()

        with pytest.raises(AuthorizationError):
            cliente_service.get_clientes(10, 1, None, user_pedro)

    finally:
        limpiar_db(conn)


######## productos ##########################################################

def test_crear_producto_admin_puede_crear():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        producto_service = ProductoService(repo_productos, conn)
        admin = build_user_admin()

        producto = producto_service.crear_producto("pera", 7, 30, admin)

        assert producto.id is not None
        assert producto.nombre == "pera"
        assert producto.precio == 7
        assert producto.stock == 30

        producto_guardado = repo_productos.get_producto(producto.id)
        assert producto_guardado.nombre == "pera"
        assert producto_guardado.precio == 7
        assert producto_guardado.stock == 30

    finally:
        limpiar_db(conn)


def test_crear_producto_customer_falla_por_autorizacion():
    try:
        conn, repo_pedidos, repo_productos, repo_clientes, pedido_service = crear_contexto()
        producto_service = ProductoService(repo_productos, conn)
        user_pedro = build_user_pedro()

        with pytest.raises(AuthorizationError):
            producto_service.crear_producto("pera", 7, 30, user_pedro)

        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM productos WHERE nombre = %s", ("pera",))
            cantidad = cursor.fetchone()[0]

        assert cantidad == 0

    finally:
        limpiar_db(conn)
