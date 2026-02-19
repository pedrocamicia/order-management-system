class DomainException(Exception):
    pass

class CantidadDeProductoNoDisponibleEnStock(DomainException):
    pass

class ProductoNoDisponible(DomainException):
    pass

class EstadoPedidoInvalido(DomainException):
    pass

class CantidadInvalida(DomainException):
    pass

class PedidoVacioInvalido(DomainException):
    pass



class NotFound(Exception):
    pass

class PedidoNoExistenteError(NotFound):
    pass

class ProductoNoExistenteError(NotFound):
    pass

class ClienteNoExistente(NotFound):
    pass