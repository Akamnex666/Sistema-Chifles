import type * as productoInsumo from './producto_insumo';
import type * as detalleOrden from './detalle_orden_produccion';

export interface IInsumo {
  id: number;
  nombre: string;
  unidad_medida: string;
  stock: number;
  estado: string;

  productosInsumos?: productoInsumo.IProductoInsumo[];
  detallesOrden?: detalleOrden.IDetalleOrdenProduccion[];
}
