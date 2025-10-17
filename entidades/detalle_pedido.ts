import type * as producto from './producto';
import type * as pedido from './pedido';

export interface IDetallePedido {
  id: number;
  cantidad_solicitada: number;
  precio_unitario: number;
  subtotal: number;
  productoId: number;
  pedidoId: number;

  producto?: producto.IProducto;
  pedido?: pedido.IPedido;
}
