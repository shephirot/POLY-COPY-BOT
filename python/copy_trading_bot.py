"""
Servicio principal del bot de copy trading
"""
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Set, Optional, Dict
from colorama import Fore, Style
from polymarket_client import PolymarketClient
from logger import (
    get_logger, log_success, log_error, log_warning,
    log_trade, log_stats
)

@dataclass
class BotStats:
    """Estadísticas del bot"""
    total_trades_detected: int = 0
    total_trades_copied: int = 0
    total_trades_failed: int = 0
    total_volume_copied: float = 0.0
    start_time: float = 0.0
    last_trade_time: Optional[float] = None

class CopyTradingBot:
    """Bot de copy trading para Polymarket"""

    def __init__(self, config):
        self.config = config
        self.client = PolymarketClient(config)
        self.processed_trade_ids: Set[str] = set()
        # Inicializar timestamp atrás en el tiempo para detectar trades recientes al inicio
        # Retroceder el doble del max_trade_age para asegurar que detecte trades recientes
        self.last_check_timestamp = (time.time() * 1000) - (config.max_trade_age_minutes * 60 * 1000 * 2)
        self.is_running = False
        self.stats = BotStats(start_time=time.time())
        self.logger = get_logger()

    def initialize(self):
        """Inicializa el bot"""
        print('=' * 60)
        print(f"{Fore.CYAN}{Style.BRIGHT}  POLYMARKET COPY TRADING BOT{Style.RESET_ALL}")
        print('=' * 60)
        print()

        self.client.initialize()

        print()
        print(f"{Style.BRIGHT}Configuración:{Style.RESET_ALL}")

        if len(self.config.target_trader_addresses) == 1:
            print(f"  Trader objetivo: {Fore.YELLOW}{self.config.target_trader_addresses[0][:10]}...{Style.RESET_ALL}")
        else:
            print(f"  Traders objetivo: {Fore.YELLOW}{len(self.config.target_trader_addresses)} traders{Style.RESET_ALL}")
            for i, addr in enumerate(self.config.target_trader_addresses, 1):
                print(f"    {i}. {Fore.YELLOW}{addr[:10]}...{addr[-8:]}{Style.RESET_ALL}")

        print(f"  Tu dirección: {Fore.YELLOW}{self.config.your_polymarket_address[:10]}...{Style.RESET_ALL}")

        if self.config.copy_mode == 'percentage':
            print(f"  Modo de copiado: {Fore.CYAN}PORCENTAJE{Style.RESET_ALL} "
                  f"({Fore.YELLOW}{self.config.copy_size_multiplier}x{Style.RESET_ALL} del tamaño del trader)")
        else:
            print(f"  Modo de copiado: {Fore.CYAN}STAKE FIJO{Style.RESET_ALL} "
                  f"({Fore.YELLOW}${self.config.fixed_stake_size}{Style.RESET_ALL} por trade)")

        print(f"  Tamaño min/max: {Fore.YELLOW}${self.config.min_order_size} - ${self.config.max_order_size}{Style.RESET_ALL}")
        print(f"  Slippage máximo: {Fore.YELLOW}{self.config.max_slippage * 100:.1f}%{Style.RESET_ALL}")
        print(f"  Intervalo de polling: {Fore.YELLOW}{self.config.poll_interval}ms{Style.RESET_ALL}")
        print(f"  Max edad de trades: {Fore.YELLOW}{self.config.max_trade_age_minutes} minutos{Style.RESET_ALL}")

        if self.config.dry_run:
            print(f"  Modo: {Fore.RED}{Style.BRIGHT}DRY RUN (Simulación){Style.RESET_ALL}")
        else:
            print(f"  Modo: {Fore.GREEN}{Style.BRIGHT}LIVE TRADING{Style.RESET_ALL}")

        print()
        print('=' * 60)
        print()

        if self.config.dry_run:
            log_warning('⚠️  MODO DRY RUN ACTIVADO - No se ejecutarán trades reales')
            print()

    def start(self):
        """Inicia el bot"""
        if self.is_running:
            log_warning('El bot ya está en ejecución')
            return

        self.is_running = True
        log_success('🚀 Bot iniciado - Monitoreando trades...')
        print()

        # Loop principal
        while self.is_running:
            try:
                self.check_for_new_trades()
                time.sleep(self.config.poll_interval / 1000)
            except KeyboardInterrupt:
                break
            except Exception as e:
                log_error('Error en el loop principal', e)
                self.logger.debug(f"Detalles del error: {type(e).__name__}: {str(e)}")
                time.sleep(5)

    def stop(self):
        """Detiene el bot"""
        print()
        self.logger.info('Deteniendo bot...')
        self.is_running = False
        self.print_stats()

    def check_for_new_trades(self):
        """Verifica si hay nuevos trades de los traders objetivo"""
        all_trades = []

        # Obtener trades de cada trader
        for trader_address in self.config.target_trader_addresses:
            self.logger.debug(f"Consultando trades de {trader_address[:10]}...")
            trades = self.client.get_trader_trades(trader_address, 50)

            if trades:
                # Agregar información del trader a cada trade
                for trade in trades:
                    trade['_trader_address'] = trader_address
                all_trades.extend(trades)
                self.logger.debug(f"  → Obtenidos {len(trades)} trades")

        if not all_trades:
            self.logger.debug("No se obtuvieron trades de ningún trader")
            return

        # Debug: mostrar estructura del primer trade
        if all_trades and len(all_trades) > 0:
            self.logger.debug(f"Total de trades obtenidos: {len(all_trades)}")
            self.logger.debug(f"Estructura del primer trade: {list(all_trades[0].keys())}")

        # Usar all_trades en lugar de trades
        trades = all_trades

        # Filtrar trades nuevos con manejo robusto de campos
        current_time = time.time() * 1000
        max_age = self.config.max_trade_age_minutes * 60 * 1000

        self.logger.debug(f"Tiempo actual: {current_time}")
        self.logger.debug(f"Último check: {self.last_check_timestamp}")
        self.logger.debug(f"Max age permitido: {max_age / 1000 / 60} minutos")

        new_trades = []
        skipped_by_id = 0
        skipped_by_age = 0
        skipped_by_timestamp = 0

        for trade in trades:
            try:
                # Obtener ID del trade (puede estar en diferentes campos)
                trade_id = trade.get('id') or trade.get('trade_id') or trade.get('tradeId')
                if not trade_id:
                    self.logger.debug("Trade sin ID, saltando...")
                    continue

                # Ya procesado
                if trade_id in self.processed_trade_ids:
                    skipped_by_id += 1
                    self.logger.debug(f"Trade {trade_id[:8]}... ya procesado anteriormente")
                    continue

                # Obtener timestamp (puede estar en diferentes campos o formatos)
                timestamp = trade.get('timestamp') or trade.get('created_at') or trade.get('time')

                if timestamp is None:
                    # Si no tiene timestamp, asumimos que es reciente
                    self.logger.debug(f"Trade {trade_id[:8]}... sin timestamp, asumiendo reciente")
                    new_trades.append(trade)
                    continue

                # Convertir timestamp si es necesario
                if isinstance(timestamp, str):
                    # Intentar parsear timestamp string
                    try:
                        from dateutil import parser
                        dt = parser.parse(timestamp)
                        timestamp = int(dt.timestamp() * 1000)
                    except:
                        self.logger.debug(f"No se pudo parsear timestamp: {timestamp}")
                        continue

                # Calcular edad del trade
                trade_age_ms = current_time - timestamp
                trade_age_minutes = trade_age_ms / 1000 / 60

                # Verificar antigüedad
                if trade_age_ms >= max_age:
                    skipped_by_age += 1
                    self.logger.debug(
                        f"Trade {trade_id[:8]}... muy antiguo "
                        f"(edad: {trade_age_minutes:.1f}min, max: {max_age / 1000 / 60}min)"
                    )
                    continue

                if timestamp <= self.last_check_timestamp:
                    skipped_by_timestamp += 1
                    self.logger.debug(
                        f"Trade {trade_id[:8]}... ya fue verificado en check anterior "
                        f"(timestamp: {timestamp}, último check: {self.last_check_timestamp})"
                    )
                    continue

                # Trade es nuevo y reciente
                self.logger.debug(
                    f"Trade {trade_id[:8]}... es NUEVO y RECIENTE (edad: {trade_age_minutes:.1f}min)"
                )
                new_trades.append(trade)

            except Exception as e:
                self.logger.debug(f"Error procesando trade: {e}")
                continue

        # Resumen del filtrado
        if len(trades) > 0:
            self.logger.debug("=" * 50)
            self.logger.debug(f"RESUMEN DEL FILTRADO:")
            self.logger.debug(f"  Total trades obtenidos: {len(trades)}")
            self.logger.debug(f"  Omitidos (ya procesados): {skipped_by_id}")
            self.logger.debug(f"  Omitidos (muy antiguos): {skipped_by_age}")
            self.logger.debug(f"  Omitidos (ya verificados): {skipped_by_timestamp}")
            self.logger.debug(f"  Trades NUEVOS detectados: {len(new_trades)}")
            self.logger.debug("=" * 50)

        if new_trades:
            self.logger.info(
                f"📥 Detectados {Fore.YELLOW}{len(new_trades)}{Style.RESET_ALL} nuevos trades"
            )
            self.stats.total_trades_detected += len(new_trades)

            for trade in new_trades:
                self.process_trade(trade)
                trade_id = trade.get('id') or trade.get('trade_id') or trade.get('tradeId')
                if trade_id:
                    self.processed_trade_ids.add(trade_id)

        self.last_check_timestamp = current_time

    def process_trade(self, trade: Dict):
        """Procesa un trade individual"""
        try:
            # Obtener datos del trade con valores por defecto
            side = trade.get('side', 'UNKNOWN')
            size = trade.get('size', trade.get('amount', '0'))
            price = trade.get('price', '0')
            trader_addr = trade.get('_trader_address', 'unknown')

            # Mostrar información del trader si hay múltiples
            trader_info = ""
            if len(self.config.target_trader_addresses) > 1:
                trader_info = f" [{Fore.MAGENTA}{trader_addr[:8]}...{Style.RESET_ALL}]"

            log_trade(
                f"Trade detectado{trader_info}: {Fore.CYAN}{side}{Style.RESET_ALL} "
                f"{size} @ ${price}"
            )

            # Validar filtros
            if not self.should_copy_trade(trade):
                log_warning('  ↳ Trade omitido por filtros')
                return

            # Obtener información del mercado
            market_id = trade.get('market') or trade.get('market_id') or trade.get('condition_id')
            if not market_id:
                log_error('  ↳ Trade sin información de mercado')
                self.stats.total_trades_failed += 1
                return

            market = self.client.get_market(market_id)
            if not market:
                log_error('  ↳ No se pudo obtener información del mercado')
                self.stats.total_trades_failed += 1
                return

            # Preparar la orden
            order = self.prepare_order(trade, market)
            if not order:
                log_warning('  ↳ Orden no cumple con los parámetros de riesgo')
                return

            # Ejecutar la orden
            result = self.execute_order(order)

            if result['success']:
                log_success(f"  ↳ Orden ejecutada exitosamente! ID: {result.get('order_id', 'N/A')}")
                self.stats.total_trades_copied += 1
                self.stats.total_volume_copied += order['size'] * order['price']
                self.stats.last_trade_time = time.time()
            else:
                log_error(f"  ↳ Error al ejecutar orden: {result.get('error', 'Unknown')}")
                self.stats.total_trades_failed += 1

        except Exception as e:
            log_error('Error al procesar trade', e)
            self.logger.debug(f"Datos del trade: {trade}")
            self.stats.total_trades_failed += 1

    def should_copy_trade(self, trade: Dict) -> bool:
        """Valida si un trade debe ser copiado según los filtros"""
        # Filtro de lados (BUY/SELL)
        side = trade.get('side', '')
        if side and side not in self.config.copy_sides:
            return False

        # Whitelist de mercados
        market_id = trade.get('market') or trade.get('market_id') or trade.get('condition_id')
        if (self.config.whitelistMarkets and
            len(self.config.whitelistMarkets) > 0):
            if market_id not in self.config.whitelistMarkets:
                return False

        # Blacklist de mercados
        if (self.config.blacklistMarkets and
            len(self.config.blacklistMarkets) > 0):
            if market_id in self.config.blacklistMarkets:
                return False

        return True

    def prepare_order(self, trade: Dict, market: Dict) -> Optional[Dict]:
        """Prepara una orden para ejecutar basándose en el trade original"""
        try:
            original_size = float(trade.get('size', trade.get('amount', 0)))
            price = float(trade.get('price', 0))

            if original_size == 0 or price == 0:
                self.logger.debug("Trade con size o price = 0, saltando")
                return None

            # Calcular el tamaño ajustado según el modo
            if self.config.copy_mode == 'percentage':
                # Modo porcentaje: copiar un % del tamaño del trader
                adjusted_size = original_size * self.config.copy_size_multiplier
                order_value = adjusted_size * price
                self.logger.debug(
                    f"  ↳ Modo porcentaje: {original_size} × {self.config.copy_size_multiplier} "
                    f"= {adjusted_size:.2f} tokens"
                )
            else:
                # Modo fixed: usar un stake fijo en USDC
                order_value = self.config.fixed_stake_size
                adjusted_size = order_value / price
                self.logger.debug(
                    f"  ↳ Modo stake fijo: ${self.config.fixed_stake_size} ÷ ${price} "
                    f"= {adjusted_size:.2f} tokens"
                )

            # Validar límites de tamaño
            if order_value < self.config.min_order_size:
                self.logger.debug(
                    f"  ↳ Orden muy pequeña: ${order_value:.2f} "
                    f"(mínimo: ${self.config.min_order_size})"
                )
                return None

            if order_value > self.config.max_order_size:
                self.logger.debug(
                    f"  ↳ Orden muy grande: ${order_value:.2f}, "
                    f"ajustando a máximo: ${self.config.max_order_size}"
                )
                adjusted_size = self.config.max_order_size / price
                order_value = self.config.max_order_size

            self.logger.debug(
                f"  ↳ Orden final: {adjusted_size:.2f} tokens @ ${price} = ${order_value:.2f}"
            )

            return {
                'token_id': trade.get('asset_id') or trade.get('token_id'),
                'price': price,
                'side': trade.get('side', 'BUY'),
                'size': adjusted_size,
                'market': market,
                'original_trade': trade
            }
        except Exception as e:
            self.logger.debug(f"Error en prepare_order: {e}")
            return None

    def execute_order(self, order: Dict) -> Dict:
        """Ejecuta una orden con reintentos"""
        result = {
            'success': False,
            'timestamp': time.time(),
            'original_trade_id': order['original_trade'].get('id', 'unknown')
        }

        # Modo dry run
        if self.config.dry_run:
            self.logger.info(
                f"{Fore.YELLOW}  ↳ [DRY RUN] Simulando: {order['side']} "
                f"{order['size']:.2f} @ ${order['price']}{Style.RESET_ALL}"
            )
            result['success'] = True
            result['order_id'] = f"DRY-RUN-{int(time.time() * 1000)}"
            return result

        # Ejecutar con reintentos
        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = self.client.create_order(
                    order['token_id'],
                    order['price'],
                    order['side'],
                    order['size'],
                    order['market'].get('min_tick_size', 0.001),
                    order['market'].get('neg_risk', False)
                )

                if response['success']:
                    result['success'] = True
                    result['order_id'] = response.get('order_id')
                    return result
                else:
                    result['error'] = response.get('error')
                    if attempt < self.config.max_retries:
                        log_warning(f"  ↳ Intento {attempt} fallido, reintentando...")
                        time.sleep(self.config.retry_delay / 1000)

            except Exception as e:
                result['error'] = str(e)
                if attempt < self.config.max_retries:
                    log_warning(f"  ↳ Intento {attempt} fallido, reintentando...")
                    time.sleep(self.config.retry_delay / 1000)

        return result

    def print_stats(self):
        """Imprime estadísticas del bot"""
        runtime = (time.time() - self.stats.start_time) / 60  # minutos

        print()
        print('=' * 60)
        print(f"{Fore.CYAN}{Style.BRIGHT}  ESTADÍSTICAS DEL BOT{Style.RESET_ALL}")
        print('=' * 60)
        log_stats(f"Tiempo de ejecución: {runtime:.1f} minutos")
        log_stats(f"Trades detectados: {Fore.YELLOW}{self.stats.total_trades_detected}{Style.RESET_ALL}")
        log_stats(f"Trades copiados: {Fore.GREEN}{self.stats.total_trades_copied}{Style.RESET_ALL}")
        log_stats(f"Trades fallidos: {Fore.RED}{self.stats.total_trades_failed}{Style.RESET_ALL}")
        log_stats(f"Volumen copiado: {Fore.GREEN}${self.stats.total_volume_copied:.2f}{Style.RESET_ALL}")

        if self.stats.total_trades_detected > 0:
            success_rate = (self.stats.total_trades_copied / self.stats.total_trades_detected) * 100
            log_stats(f"Tasa de éxito: {Fore.YELLOW}{success_rate:.1f}%{Style.RESET_ALL}")

        print('=' * 60)
