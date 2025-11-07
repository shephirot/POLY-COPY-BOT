/**
 * Tipos y interfaces para el bot de copy trading
 */

export interface BotConfig {
  // Credenciales
  targetTraderAddress: string;
  yourPolymarketAddress: string;
  yourPrivateKey: string;

  // URLs
  clobUrl: string;
  clobChainId: number;
  gammaApiUrl: string;

  // Parámetros de trading
  copyMode: 'percentage' | 'fixed';
  copySizeMultiplier: number; // Para modo percentage
  fixedStakeSize: number; // Para modo fixed (en USDC)
  minOrderSize: number;
  maxOrderSize: number;
  maxSlippage: number;

  // Monitoreo
  pollInterval: number;
  maxTradeAgeMinutes: number;

  // Reintentos
  maxRetries: number;
  retryDelay: number;

  // Operación
  dryRun: boolean;
  logLevel: string;

  // Filtros
  blacklistMarkets?: string[];
  whitelistMarkets?: string[];
  copySides: string[];
}

export interface Trade {
  id: string;
  market: string;
  asset_id: string;
  side: 'BUY' | 'SELL';
  size: string;
  price: string;
  timestamp: number;
  maker_address: string;
  trader_side: 'MAKER' | 'TAKER';
  fee_rate_bps: string;
  status?: string;
}

export interface Market {
  condition_id: string;
  question_id: string;
  tokens: Token[];
  description: string;
  end_date_iso: string;
  question: string;
  market_slug: string;
  min_tick_size: number;
  neg_risk: boolean;
}

export interface Token {
  token_id: string;
  outcome: string;
  price: number;
  winner?: boolean;
}

export interface OrderToExecute {
  tokenId: string;
  price: number;
  side: 'BUY' | 'SELL';
  size: number;
  market: Market;
  originalTrade: Trade;
}

export interface ExecutionResult {
  success: boolean;
  orderId?: string;
  error?: string;
  timestamp: number;
  originalTradeId: string;
}

export interface BotStats {
  totalTradesDetected: number;
  totalTradesCopied: number;
  totalTradesFailed: number;
  totalVolumeCopied: number;
  startTime: number;
  lastTradeTime?: number;
}
