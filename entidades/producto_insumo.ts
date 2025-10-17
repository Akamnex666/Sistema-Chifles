import type * as producto from './producto';
import type * as insumo from './insumo';

export interface IProductoInsumo {
  id: number;
  productoId: number;
  insumoId: number;
  cantidad_necesaria: number;

  producto?: producto.IProducto;
  insumo?: insumo.IInsumo;
}
