import pytest
from datetime import datetime
from src.domain.pedido import Pedido, Carrito,Confirmado
from src.domain.producto import Producto, NoDisponible, Disponible
from src.domain.item_pedido import ItemPedido
from src.domain.exception import ProductoNoDisponible, CantidadDeProductoNoDisponibleEnStock, CantidadInvalida,EstadoPedidoInvalido,PedidoVacioInvalido


########## agregar producto a pedido ###############

def test_agregar_producto():
    pedido1 = Pedido(1,2)
    banana = Producto(1, "banana",10, 20)
    manzana = Producto(2, "manzana", 5, 10)
    
    pedido1.agregar_producto(banana, 10)
    
    assert pedido1.items[0].producto_id == 1
    assert pedido1.items[0].cantidad == 10
    assert pedido1.items[0].precio_unitario == 10
    assert pedido1.total() ==  100
    
    pedido1.agregar_producto(banana, 1)
    pedido1.agregar_producto(manzana, 3)
    
    assert len(pedido1.items) == 2
    assert pedido1.total() == 125
    assert pedido1.cantidad_de_productos() == 14
    
    banana.disponible_para_venta(1) #no retorna nada pero chequeo que no salte error
    
def test_producto_no_disponible_para_venta():
    producto_no_disponible = Producto(3, "algo", 7, 10)
    producto_no_disponible.estado = NoDisponible()
    banana = Producto(1, "banana",10, 20)

    with pytest.raises(ProductoNoDisponible):
        producto_no_disponible.disponible_para_venta(1)
        
    with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
        banana.disponible_para_venta(999)
        
    with pytest.raises(CantidadDeProductoNoDisponibleEnStock):
        banana.descontar_stock(999)
        
def test_agregar_cantidad_negativa_falla():
    pedido1 = Pedido(1,2)
    manzana = Producto(2, "manzana", 5, 10)
    
    with pytest.raises(CantidadInvalida):
        pedido1.agregar_producto(manzana, -3)
    with pytest.raises(CantidadInvalida):
        pedido1.agregar_producto(manzana, 0)
    assert len(pedido1.items) == 0
    assert pedido1.total() == 0
    
def test_agregar_producto_a_pedido_confirmado_falla():
    pedido1 = Pedido(1,2)
    banana = Producto(1, "banana",10, 20)
    pedido1.estado = Confirmado()
    
    with pytest.raises(EstadoPedidoInvalido):
        pedido1.agregar_producto(banana, 4)
    
    assert len(pedido1.items) == 0
    assert pedido1.total() == 0
    assert pedido1.cantidad_de_productos() == 0
    
############ confirmar pedido ###########################

def test_confirmar_pedido():
    pedido1 = Pedido(1,2)
    banana = Producto(1, "banana",10, 20)
    manzana = Producto(2, "manzana", 5, 10)
    
    pedido1.agregar_producto(manzana, 2)
    pedido1.agregar_producto(banana, 10)
    
    pedido1.confirmar_pedido()
    
    assert isinstance(pedido1.estado, Confirmado)
    # assert pedido1.fecha_confirmacion == datetime.now() teoricamente esta bien, pero falla el test porque el assert se ejecuta unos milisegundos despues
    
def test_descontar_stock():
    manzana = Producto(2, "manzana", 5, 10)

    manzana.descontar_stock(4)
    
    assert manzana.stock == 6


def test_confirmar_pedido_confirmado_falla():
    pedido1 = Pedido(1,2)
    banana = Producto(1, "banana",10, 20)
    manzana = Producto(2, "manzana", 5, 10)
    
    pedido1.agregar_producto(manzana, 2)
    pedido1.agregar_producto(banana, 10)
    
    pedido1.confirmar_pedido()
    
    with pytest.raises(EstadoPedidoInvalido):
        pedido1.confirmar_pedido()
        
    
        
def test_confirmar_pedido_vacio_falla():
    pedido1 = Pedido(1,2)

    with pytest.raises(PedidoVacioInvalido):
        pedido1.confirmar_pedido()

    assert isinstance(pedido1.estado,Carrito)
    assert pedido1.fecha_confirmacion is None