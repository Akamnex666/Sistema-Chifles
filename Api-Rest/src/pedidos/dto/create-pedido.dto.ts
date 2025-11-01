import { IsString, IsNumber, IsInt, ValidateNested, IsArray } from 'class-validator';
import { Type } from 'class-transformer';
import { CreateDetalleDto } from './create-detalle.dto';

export class CreatePedidoDto {
  @IsString()
  fecha: string;

  @IsNumber()
  total: number;

  @IsString()
  estado: string;

  @IsInt()
  clienteId: number;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => CreateDetalleDto)
  detalles: CreateDetalleDto[];
}
