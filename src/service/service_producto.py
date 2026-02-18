from src.infrastructure.repositorio_productos import RepositorioProductos

class ProductoService:
    def __init__(self, repositorio_productos : RepositorioProductos):
        self.repositorio_productos = repositorio_productos
        
        
         
    