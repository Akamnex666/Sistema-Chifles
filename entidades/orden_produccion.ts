import type * as producto from './producto';
import type * as detalleOrden from './detalle_orden_produccion';

export interface IOrdenProduccion {
  id: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  productoId: number;
  cantidad_producir: number;

  producto?: producto.IProducto;
  detallesOrden?: detalleOrden.IDetalleOrdenProduccion[];
}
