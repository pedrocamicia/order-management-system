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

class LimiteInvalidoError(DomainException):
    pass

class PaginaInvalidaError(DomainException):
    pass

class ExistentEmailError(DomainException):
    pass



###########################################

class NotFound(Exception):
    pass

class PedidoNoExistenteError(NotFound):
    pass

class ProductoNoExistenteError(NotFound):
    pass

class ClienteNoExistente(NotFound):
    pass

class UserNotFound(NotFound):
    pass
    
################################################

class AuthException(Exception):
    pass

class InvalidCredentials(AuthException):
    pass

class ExpiredTokenError(AuthException):
    pass

class InvalidTokenError(AuthException):
    pass


##################################################

class AuthorizationError(Exception):
    pass

class NoEsDuenoDeRecursoError(AuthorizationError):
    pass