import type * as ordenProduccion from './orden_produccion';
import type * as insumo from './insumo';

export interface IDetalleOrdenProduccion {
  id: number;
  ordenProduccionId: number;
  insumoId: number;
  cantidad_utilizada: number;

  ordenProduccion?: ordenProduccion.IOrdenProduccion;
  insumo?: insumo.IInsumo;
}
