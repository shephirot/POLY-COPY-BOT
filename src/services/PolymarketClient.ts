/**
 * Cliente para interactuar con la API de Polymarket
 */
import { ClobClient } from '@polymarket/clob-client';
import { Wallet } from 'ethers';
import axios from 'axios';
import { BotConfig, Trade, Market } from '../types';
import { logger, logError, logSuccess } from '../utils/logger';

export class PolymarketClient {
  private clobClient: ClobClient | null = null;
  private wallet: Wallet;
  private config: BotConfig;
  private apiCreds: any = null;

  constructor(config: BotConfig) {
    this.config = config;
    this.wallet = new Wallet(config.yourPrivateKey);
  }

  /**
   * Inicializa el cliente CLOB con autenticación
   */
  async initialize(): Promise<void> {
    try {
      logger.info('Inicializando cliente de Polymarket...');

      // Crear cliente L1 para generar API keys
      const l1Client = new ClobClient(
        this.config.clobUrl,
        this.config.clobChainId,
        this.wallet
      );

      // Derivar o crear API credentials
      this.apiCreds = await l1Client.createOrDeriveApiKey();

      // Crear cliente L2 con las credenciales
      this.clobClient = new ClobClient(
        this.config.clobUrl,
        this.config.clobChainId,
        this.wallet,
        this.apiCreds,
        1, // Signature type (1 = EOA wallet)
        this.config.yourPolymarketAddress
      );

      logSuccess('Cliente de Polymarket inicializado correctamente');
    } catch (error: any) {
      logError('Error al inicializar cliente de Polymarket', error);
      throw error;
    }
  }

  /**
   * Obtiene los trades recientes de un trader específico
   */
  async getTraderTrades(traderAddress: string, limit: number = 100): Promise<Trade[]> {
    try {
      const url = `${this.config.clobUrl}/data/trades`;
      const params = {
        maker_address: traderAddress.toLowerCase(),
        limit: limit
      };

      const response = await axios.get(url, { params });
      return response.data as Trade[];
    } catch (error: any) {
      logError(`Error al obtener trades del trader ${traderAddress}`, error);
      return [];
    }
  }

  /**
   * Obtiene información de un mercado específico
   */
  async getMarket(conditionId: string): Promise<Market | null> {
    try {
      const url = `${this.config.gammaApiUrl}/markets/${conditionId}`;
      const response = await axios.get(url);
      return response.data as Market;
    } catch (error: any) {
      logError(`Error al obtener información del mercado ${conditionId}`, error);
      return null;
    }
  }

  /**
   * Obtiene el precio actual de un token
   */
  async getTokenPrice(tokenId: string): Promise<number | null> {
    try {
      const url = `${this.config.gammaApiUrl}/prices`;
      const response = await axios.get(url, {
        params: { token_id: tokenId }
      });

      if (response.data && response.data[tokenId]) {
        return parseFloat(response.data[tokenId]);
      }
      return null;
    } catch (error: any) {
      logError(`Error al obtener precio del token ${tokenId}`, error);
      return null;
    }
  }

  /**
   * Crea y ejecuta una orden en Polymarket
   */
  async createOrder(
    tokenId: string,
    price: number,
    side: 'BUY' | 'SELL',
    size: number,
    tickSize: number,
    negRisk: boolean
  ): Promise<{ success: boolean; orderId?: string; error?: string }> {
    if (!this.clobClient) {
      return { success: false, error: 'Cliente no inicializado' };
    }

    try {
      logger.info(`Creando orden: ${side} ${size} @ $${price} (Token: ${tokenId.substring(0, 8)}...)`);

      const orderArgs = {
        tokenID: tokenId,
        price: price,
        side: side === 'BUY' ? 'BUY' : 'SELL',
        size: size
      };

      const orderOptions = {
        tickSize: tickSize.toString(),
        negRisk: negRisk
      };

      const response = await this.clobClient.createAndPostOrder(
        orderArgs as any,
        orderOptions
      );

      if (response && response.orderID) {
        return { success: true, orderId: response.orderID };
      } else {
        return { success: false, error: 'No se recibió ID de orden' };
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Error desconocido al crear orden'
      };
    }
  }

  /**
   * Obtiene el balance de USDC del usuario
   */
  async getUSDCBalance(): Promise<number> {
    try {
      // Esto requeriría consultar el contrato de USDC en Polygon
      // Por simplicidad, retornamos un valor dummy
      // En producción, deberías implementar esto correctamente
      logger.debug('Verificando balance de USDC...');
      return 1000; // Placeholder
    } catch (error: any) {
      logError('Error al obtener balance de USDC', error);
      return 0;
    }
  }

  /**
   * Verifica si el cliente está correctamente inicializado
   */
  isInitialized(): boolean {
    return this.clobClient !== null;
  }
}
