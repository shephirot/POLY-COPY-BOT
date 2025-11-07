/**
 * Carga y valida la configuración del bot
 */
import dotenv from 'dotenv';
import { BotConfig } from '../types';
import { logger, logError } from './logger';

dotenv.config();

export function loadConfig(): BotConfig {
  // Validar variables requeridas
  const required = [
    'TARGET_TRADER_ADDRESS',
    'YOUR_POLYMARKET_ADDRESS',
    'YOUR_PRIVATE_KEY'
  ];

  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    logError(`Faltan variables de entorno requeridas: ${missing.join(', ')}`);
    logError('Copia .env.example a .env y configura las variables necesarias');
    process.exit(1);
  }

  // Parsear filtros
  const blacklistMarkets = process.env.BLACKLIST_MARKETS
    ? process.env.BLACKLIST_MARKETS.split(',').map(m => m.trim())
    : undefined;

  const whitelistMarkets = process.env.WHITELIST_MARKETS
    ? process.env.WHITELIST_MARKETS.split(',').map(m => m.trim())
    : undefined;

  const copySides = process.env.COPY_SIDES
    ? process.env.COPY_SIDES.split(',').map(s => s.trim())
    : ['BUY', 'SELL'];

  // Validar y parsear modo de copiado
  const copyMode = (process.env.COPY_MODE || 'percentage').toLowerCase();
  if (copyMode !== 'percentage' && copyMode !== 'fixed') {
    logError('COPY_MODE debe ser "percentage" o "fixed"');
    process.exit(1);
  }

  const config: BotConfig = {
    targetTraderAddress: process.env.TARGET_TRADER_ADDRESS!,
    yourPolymarketAddress: process.env.YOUR_POLYMARKET_ADDRESS!,
    yourPrivateKey: process.env.YOUR_PRIVATE_KEY!,

    clobUrl: process.env.CLOB_URL || 'https://clob.polymarket.com',
    clobChainId: parseInt(process.env.CLOB_CHAIN_ID || '137'),
    gammaApiUrl: process.env.GAMMA_API_URL || 'https://gamma-api.polymarket.com',

    copyMode: copyMode as 'percentage' | 'fixed',
    copySizeMultiplier: parseFloat(process.env.COPY_SIZE_MULTIPLIER || '1.0'),
    fixedStakeSize: parseFloat(process.env.FIXED_STAKE_SIZE || '10'),
    minOrderSize: parseFloat(process.env.MIN_ORDER_SIZE || '1'),
    maxOrderSize: parseFloat(process.env.MAX_ORDER_SIZE || '1000'),
    maxSlippage: parseFloat(process.env.MAX_SLIPPAGE || '0.02'),

    pollInterval: parseInt(process.env.POLL_INTERVAL || '5000'),
    maxTradeAgeMinutes: parseInt(process.env.MAX_TRADE_AGE_MINUTES || '5'),

    maxRetries: parseInt(process.env.MAX_RETRIES || '3'),
    retryDelay: parseInt(process.env.RETRY_DELAY || '2000'),

    dryRun: process.env.DRY_RUN === 'true',
    logLevel: process.env.LOG_LEVEL || 'info',

    blacklistMarkets,
    whitelistMarkets,
    copySides
  };

  // Validaciones
  if (config.copyMode === 'percentage') {
    if (config.copySizeMultiplier <= 0) {
      logError('COPY_SIZE_MULTIPLIER debe ser mayor que 0 (modo percentage)');
      process.exit(1);
    }
  } else if (config.copyMode === 'fixed') {
    if (config.fixedStakeSize <= 0) {
      logError('FIXED_STAKE_SIZE debe ser mayor que 0 (modo fixed)');
      process.exit(1);
    }
  }

  if (config.minOrderSize < 0 || config.maxOrderSize < config.minOrderSize) {
    logError('MIN_ORDER_SIZE y MAX_ORDER_SIZE deben ser válidos');
    process.exit(1);
  }

  if (config.maxSlippage < 0 || config.maxSlippage > 1) {
    logError('MAX_SLIPPAGE debe estar entre 0 y 1');
    process.exit(1);
  }

  logger.info('✓ Configuración cargada correctamente');
  return config;
}
