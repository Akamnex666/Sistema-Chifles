import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Pedido } from './entities/pedido.entity';
import { DetallePedido } from '../detalles-pedido/entities/detalles-pedido.entity';
import { PedidosService } from './pedidos.service';
import { PedidosController } from './pedidos.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Pedido, DetallePedido])],
  providers: [PedidosService],
  controllers: [PedidosController],
})
export class PedidosModule {}
