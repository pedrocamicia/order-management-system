import math
from src.domain.exception import PaginaInvalidaError, LimiteInvalidoError


class Page:
    def __init__(self, items, total, page, limit):
        self.items = items
        self.total = total
        self.page = page
        self.limit = limit
        self.total_pages = math.ceil(total / limit) if total > 0 else 0
        
    
def restricciones_paginacion(page, limit):
    if page < 1:
        raise PaginaInvalidaError("se ingreso una pagina negativa o 0")
    if limit < 1 or limit > 100:
        raise LimiteInvalidoError("se ingreso un limite invalido, menor a 1 o mayor a 100 no esta permitido") 