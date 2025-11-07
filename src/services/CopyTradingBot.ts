/**
 * Servicio principal del bot de copy trading
 */
import { BotConfig, Trade, OrderToExecute, ExecutionResult, BotStats } from '../types';
import { PolymarketClient } from './PolymarketClient';
import { logger, logSuccess, logError, logWarning, logTrade, logStats } from '../utils/logger';
import chalk from 'chalk';

export class CopyTradingBot {
  private client: PolymarketClient;
  private config: BotConfig;
  private processedTradeIds: Set<string>;
  private lastCheckTimestamp: number;
  private stats: BotStats;
  private isRunning: boolean;

  constructor(config: BotConfig) {
    this.config = config;
    this.client = new PolymarketClient(config);
    this.processedTradeIds = new Set();
    this.lastCheckTimestamp = Date.now();
    this.isRunning = false;

    this.stats = {
      totalTradesDetected: 0,
      totalTradesCopied: 0,
      totalTradesFailed: 0,
      totalVolumeCopied: 0,
      startTime: Date.now()
    };
  }

  /**
   * Inicializa el bot
   */
  async initialize(): Promise<void> {
    logger.info('='.repeat(60));
    logger.info(chalk.bold.cyan('  POLYMARKET COPY TRADING BOT'));
    logger.info('='.repeat(60));
    logger.info('');

    await this.client.initialize();

    logger.info('');
    logger.info(chalk.bold('Configuración:'));
    logger.info(`  Trader objetivo: ${chalk.yellow(this.config.targetTraderAddress.substring(0, 10) + '...')}`);
    logger.info(`  Tu dirección: ${chalk.yellow(this.config.yourPolymarketAddress.substring(0, 10) + '...')}`);
    logger.info(`  Multiplicador de tamaño: ${chalk.yellow(this.config.copySizeMultiplier + 'x')}`);
    logger.info(`  Tamaño min/max: ${chalk.yellow('$' + this.config.minOrderSize + ' - $' + this.config.maxOrderSize)}`);
    logger.info(`  Slippage máximo: ${chalk.yellow((this.config.maxSlippage * 100).toFixed(1) + '%')}`);
    logger.info(`  Intervalo de polling: ${chalk.yellow(this.config.pollInterval + 'ms')}`);
    logger.info(`  Modo: ${this.config.dryRun ? chalk.red.bold('DRY RUN (Simulación)') : chalk.green.bold('LIVE TRADING')}`);
    logger.info('');
    logger.info('='.repeat(60));
    logger.info('');

    if (this.config.dryRun) {
      logWarning('⚠️  MODO DRY RUN ACTIVADO - No se ejecutarán trades reales');
      logger.info('');
    }
  }

  /**
   * Inicia el bot
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      logWarning('El bot ya está en ejecución');
      return;
    }

    this.isRunning = true;
    logSuccess('🚀 Bot iniciado - Monitoreando trades...');
    logger.info('');

    // Loop principal
    while (this.isRunning) {
      try {
        await this.checkForNewTrades();
        await this.sleep(this.config.pollInterval);
      } catch (error: any) {
        logError('Error en el loop principal', error);
        await this.sleep(5000); // Esperar 5s en caso de error
      }
    }
  }

  /**
   * Detiene el bot
   */
  stop(): void {
    logger.info('');
    logger.info('Deteniendo bot...');
    this.isRunning = false;
    this.printStats();
  }

  /**
   * Verifica si hay nuevos trades del trader objetivo
   */
  private async checkForNewTrades(): Promise<void> {
    const trades = await this.client.getTraderTrades(this.config.targetTraderAddress, 50);

    if (!trades || trades.length === 0) {
      return;
    }

    // Filtrar trades nuevos
    const newTrades = trades.filter(trade => {
      // Ya procesado
      if (this.processedTradeIds.has(trade.id)) {
        return false;
      }

      // Muy antiguo
      const tradeAge = Date.now() - trade.timestamp;
      const maxAge = this.config.maxTradeAgeMinutes * 60 * 1000;
      if (tradeAge > maxAge) {
        return false;
      }

      // Después del último check
      return trade.timestamp > this.lastCheckTimestamp;
    });

    if (newTrades.length > 0) {
      logger.info(`📥 Detectados ${chalk.yellow(newTrades.length)} nuevos trades`);
      this.stats.totalTradesDetected += newTrades.length;

      for (const trade of newTrades) {
        await this.processTrade(trade);
        this.processedTradeIds.add(trade.id);
      }
    }

    this.lastCheckTimestamp = Date.now();
  }

  /**
   * Procesa un trade individual
   */
  private async processTrade(trade: Trade): Promise<void> {
    try {
      logTrade(`Trade detectado: ${chalk.cyan(trade.side)} ${trade.size} @ $${trade.price}`);

      // Validar filtros
      if (!this.shouldCopyTrade(trade)) {
        logWarning('  ↳ Trade omitido por filtros');
        return;
      }

      // Obtener información del mercado
      const market = await this.client.getMarket(trade.market);
      if (!market) {
        logError('  ↳ No se pudo obtener información del mercado');
        this.stats.totalTradesFailed++;
        return;
      }

      // Preparar la orden
      const order = this.prepareOrder(trade, market);
      if (!order) {
        logWarning('  ↳ Orden no cumple con los parámetros de riesgo');
        return;
      }

      // Ejecutar la orden
      const result = await this.executeOrder(order);

      if (result.success) {
        logSuccess(`  ↳ Orden ejecutada exitosamente! ID: ${result.orderId}`);
        this.stats.totalTradesCopied++;
        this.stats.totalVolumeCopied += order.size * order.price;
        this.stats.lastTradeTime = Date.now();
      } else {
        logError(`  ↳ Error al ejecutar orden: ${result.error}`);
        this.stats.totalTradesFailed++;
      }

    } catch (error: any) {
      logError('Error al procesar trade', error);
      this.stats.totalTradesFailed++;
    }
  }

  /**
   * Valida si un trade debe ser copiado según los filtros
   */
  private shouldCopyTrade(trade: Trade): boolean {
    // Filtro de lados (BUY/SELL)
    if (!this.config.copySides.includes(trade.side)) {
      return false;
    }

    // Whitelist de mercados
    if (this.config.whitelistMarkets && this.config.whitelistMarkets.length > 0) {
      if (!this.config.whitelistMarkets.includes(trade.market)) {
        return false;
      }
    }

    // Blacklist de mercados
    if (this.config.blacklistMarkets && this.config.blacklistMarkets.length > 0) {
      if (this.config.blacklistMarkets.includes(trade.market)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Prepara una orden para ejecutar basándose en el trade original
   */
  private prepareOrder(trade: Trade, market: any): OrderToExecute | null {
    const originalSize = parseFloat(trade.size);
    const price = parseFloat(trade.price);

    // Calcular el tamaño ajustado
    let adjustedSize = originalSize * this.config.copySizeMultiplier;
    const orderValue = adjustedSize * price;

    // Validar límites de tamaño
    if (orderValue < this.config.minOrderSize) {
      logger.debug(`  ↳ Orden muy pequeña: $${orderValue.toFixed(2)}`);
      return null;
    }

    if (orderValue > this.config.maxOrderSize) {
      logger.debug(`  ↳ Orden muy grande: $${orderValue.toFixed(2)}, ajustando...`);
      adjustedSize = this.config.maxOrderSize / price;
    }

    return {
      tokenId: trade.asset_id,
      price: price,
      side: trade.side,
      size: adjustedSize,
      market: market,
      originalTrade: trade
    };
  }

  /**
   * Ejecuta una orden con reintentos
   */
  private async executeOrder(order: OrderToExecute): Promise<ExecutionResult> {
    const result: ExecutionResult = {
      success: false,
      timestamp: Date.now(),
      originalTradeId: order.originalTrade.id
    };

    // Modo dry run
    if (this.config.dryRun) {
      logger.info(chalk.yellow(`  ↳ [DRY RUN] Simulando: ${order.side} ${order.size.toFixed(2)} @ $${order.price}`));
      result.success = true;
      result.orderId = 'DRY-RUN-' + Date.now();
      return result;
    }

    // Ejecutar con reintentos
    for (let attempt = 1; attempt <= this.config.maxRetries; attempt++) {
      try {
        const response = await this.client.createOrder(
          order.tokenId,
          order.price,
          order.side,
          order.size,
          order.market.min_tick_size || 0.001,
          order.market.neg_risk || false
        );

        if (response.success) {
          result.success = true;
          result.orderId = response.orderId;
          return result;
        } else {
          result.error = response.error;
          if (attempt < this.config.maxRetries) {
            logWarning(`  ↳ Intento ${attempt} fallido, reintentando...`);
            await this.sleep(this.config.retryDelay);
          }
        }
      } catch (error: any) {
        result.error = error.message;
        if (attempt < this.config.maxRetries) {
          logWarning(`  ↳ Intento ${attempt} fallido, reintentando...`);
          await this.sleep(this.config.retryDelay);
        }
      }
    }

    return result;
  }

  /**
   * Imprime estadísticas del bot
   */
  private printStats(): void {
    const runtime = (Date.now() - this.stats.startTime) / 1000 / 60; // minutos

    logger.info('');
    logger.info('='.repeat(60));
    logger.info(chalk.bold.cyan('  ESTADÍSTICAS DEL BOT'));
    logger.info('='.repeat(60));
    logStats(`Tiempo de ejecución: ${runtime.toFixed(1)} minutos`);
    logStats(`Trades detectados: ${chalk.yellow(this.stats.totalTradesDetected)}`);
    logStats(`Trades copiados: ${chalk.green(this.stats.totalTradesCopied)}`);
    logStats(`Trades fallidos: ${chalk.red(this.stats.totalTradesFailed)}`);
    logStats(`Volumen copiado: ${chalk.green('$' + this.stats.totalVolumeCopied.toFixed(2))}`);

    if (this.stats.totalTradesDetected > 0) {
      const successRate = (this.stats.totalTradesCopied / this.stats.totalTradesDetected) * 100;
      logStats(`Tasa de éxito: ${chalk.yellow(successRate.toFixed(1) + '%')}`);
    }

    logger.info('='.repeat(60));
  }

  /**
   * Helper para dormir
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
