import strawberry
from typing import List, Optional


@strawberry.type
class InsumoReceta:
    insumoId: int
    insumoNombre: Optional[str]
    cantidadNecesaria: float
    unidadMedida: Optional[str]


@strawberry.type
class TrazabilidadProducto:
    productoId: int
    nombre: Optional[str]
    cantidadSolicitada: int
    receta: List[InsumoReceta]


@strawberry.type
class ConsumoInsumo:
    insumoId: int
    insumoNombre: Optional[str]
    cantidadTotal: float
    unidad: Optional[str]


@strawberry.type
class PedidoResumen:
    id: int
    fecha: str
    total: float
    estado: str


@strawberry.type
class ProductoMasVendido:
    productoId: int
    productoNombre: Optional[str]
    cantidadVendida: int
