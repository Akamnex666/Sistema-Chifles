import type * as pedido from './pedido';
import type * as factura from './factura';

export interface ICliente {
  id: number;
  nombre: string;
  apellido: string;
  dni: string;
  telefono: string;
  email: string;

  pedidos?: pedido.IPedido[];
  facturas?: factura.IFactura[];
}
