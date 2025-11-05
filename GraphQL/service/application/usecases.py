from typing import List, Dict, Any
from domain.models import Pedido, Cliente, Producto, ProductoInsumo, Insumo, OrdenProduccion


class ReportService:
    def __init__(self, rest):
        # rest is an instance of infrastructure.http_client.RESTClient
        self.rest = rest

    async def pedidos_por_cliente(self, clienteId: int, fechaInicio: str = None, fechaFin: str = None) -> List[Dict[str, Any]]:
        params = {}
        if fechaInicio: params['fechaInicio'] = fechaInicio
        if fechaFin: params['fechaFin'] = fechaFin
        data = await self.rest.get(f'/pedidos', params={**params, 'clienteId': clienteId})
        return data

    async def consumo_insumos(self, fechaInicio: str = None, fechaFin: str = None) -> List[Dict[str, Any]]:
        # Strategy: fetch ordenes-produccion and aggregate detalle ordenes
        params = {}
        if fechaInicio: params['fechaInicio'] = fechaInicio
        if fechaFin: params['fechaFin'] = fechaFin
        ordenes = await self.rest.get('/ordenes-produccion', params=params)
        usage = {}
        for orden in ordenes:
            detalles = orden.get('detalles', [])
            for d in detalles:
                insumoId = d['insumoId']
                cantidad = float(d.get('cantidad_utilizada', 0))
                if insumoId not in usage:
                    usage[insumoId] = {'insumoId': insumoId, 'cantidadTotal': 0}
                usage[insumoId]['cantidadTotal'] += cantidad
        # Enriquecer con nombre y unidad
        results = []
        for insumoId, item in usage.items():
            ins = await self.rest.get(f'/insumos/{insumoId}')
            item['insumoNombre'] = ins.get('nombre')
            item['unidad'] = ins.get('unidad_medida')
            results.append(item)
        return results

    async def productos_mas_vendidos(self, limite: int = 10) -> List[Dict[str, Any]]:
        # Strategy: aggregate from pedidos -> detalles
        pedidos = await self.rest.get('/pedidos')
        counts = {}
        for p in pedidos:
            for d in p.get('detalles', []):
                pid = d['productoId']
                counts.setdefault(pid, 0)
                counts[pid] += int(d.get('cantidad_solicitada', 0))
        items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limite]
        results = []
        for pid, qty in items:
            prod = await self.rest.get(f'/productos/{pid}')
            results.append({'productId': pid, 'productName': prod.get('nombre'), 'totalSold': qty})
        return results

    async def trazabilidad_pedido(self, pedidoId: int) -> Dict[str, Any]:
        pedido = await self.rest.get(f'/pedidos/{pedidoId}')
        trace = []
        for det in pedido.get('detalles', []):
            producto = await self.rest.get(f"/productos/{det['productoId']}")
            # obtener receta
            productos_insumo = await self.rest.get(f"/productos-insumos", params={'productoId': det['productoId']})
            receta = []
            for ri in productos_insumo:
                ins = await self.rest.get(f"/insumos/{ri['insumoId']}")
                receta.append({
                    'insumoId': ri['insumoId'],
                    'insumoNombre': ins.get('nombre'),
                    'cantidadNecesaria': float(ri.get('cantidad_necesaria', 0)),
                    'unidadMedida': ins.get('unidad_medida')
                })
            trace.append({
                'productoId': producto.get('id'),
                'nombre': producto.get('nombre'),
                'cantidadSolicitada': det.get('cantidad_solicitada'),
                'receta': receta
            })
        return {'pedidoId': pedidoId, 'productos': trace}
