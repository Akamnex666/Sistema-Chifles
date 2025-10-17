import type * as cliente from './cliente';
import type * as pedido from './pedido';

export interface IFactura {
  id: number;
  fecha_emision: string;
  total: number;
  estado_pago: string;
  clienteId: number;
  pedidoId: number;

  cliente?: cliente.ICliente;
  pedido?: pedido.IPedido;
}
