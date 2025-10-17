import type * as detallePedido from './detalle_pedido';
import type * as productoInsumo from './producto_insumo';
import type * as ordenProduccion from './orden_produccion';

export interface IProducto {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  categoria: string;
  unidad_medida: string;
  estado: string;

  detallesPedidos?: detallePedido.IDetallePedido[];
  productosInsumos?: productoInsumo.IProductoInsumo[];
  ordenesProduccion?: ordenProduccion.IOrdenProduccion[];
}
