import type * as cliente from './cliente';
import type * as factura from './factura';
import type * as detallePedido from './detalle_pedido';

export interface IPedido {
  id: number;
  fecha: string;
  total: number;
  estado: string;
  clienteId: number;
  facturaId: number;

  cliente?: cliente.ICliente;
  factura?: factura.IFactura;
  detalles?: detallePedido.IDetallePedido[];
}
