import strawberry
from typing import List, Optional
from application.usecases import ReportService
from interface.graphql.types import (
    PedidoResumen,
    ConsumoInsumo,
    TrazabilidadProducto,
    InsumoReceta,
    ProductoMasVendido,
)


@strawberry.type
class Query:
    @strawberry.field
    async def pedidosPorCliente(self, info, clienteId: int, fechaInicio: Optional[str] = None, fechaFin: Optional[str] = None) -> List[PedidoResumen]:
        rest = info.context['rest']
        svc = ReportService(rest)
        data = await svc.pedidos_por_cliente(clienteId, fechaInicio, fechaFin)
        return [PedidoResumen(id=int(p['id']), fecha=p['fecha'], total=float(p['total']), estado=p['estado']) for p in data]

    @strawberry.field
    async def consumoInsumos(self, info, fechaInicio: Optional[str] = None, fechaFin: Optional[str] = None) -> List[ConsumoInsumo]:
        rest = info.context['rest']
        svc = ReportService(rest)
        data = await svc.consumo_insumos(fechaInicio, fechaFin)
        return [
            ConsumoInsumo(
                insumoId=int(d['insumoId']),
                insumoNombre=d.get('insumoNombre'),
                cantidadTotal=float(d.get('cantidadTotal', 0)),
                unidad=d.get('unidad'),
            )
            for d in data
        ]

    @strawberry.field
    async def productosMasVendidos(self, info, limite: int = 10) -> List[ProductoMasVendido]:
        rest = info.context['rest']
        svc = ReportService(rest)
        data = await svc.productos_mas_vendidos(limite)
        result: List[ProductoMasVendido] = []
        for item in data:
            result.append(
                ProductoMasVendido(
                    productoId=int(item.get('productId')),
                    productoNombre=item.get('productName'),
                    cantidadVendida=int(item.get('totalSold', 0)),
                )
            )
        return result

    @strawberry.field
    async def trazabilidadPedido(self, info, pedidoId: int) -> List[TrazabilidadProducto]:
        rest = info.context['rest']
        svc = ReportService(rest)
        data = await svc.trazabilidad_pedido(pedidoId)
        res = []
        for p in data.get('productos', []):
            receta_objs = []
            for r in p.get('receta', []):
                receta_objs.append(
                    InsumoReceta(
                        insumoId=int(r['insumoId']),
                        insumoNombre=r.get('insumoNombre'),
                        cantidadNecesaria=float(r.get('cantidadNecesaria', 0)),
                        unidadMedida=r.get('unidadMedida'),
                    )
                )
            res.append(
                TrazabilidadProducto(
                    productoId=int(p['productoId']),
                    nombre=p.get('nombre'),
                    cantidadSolicitada=int(p.get('cantidadSolicitada', 0)),
                    receta=receta_objs,
                )
            )
        return res
