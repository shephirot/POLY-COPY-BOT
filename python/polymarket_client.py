"""
Cliente para interactuar con la API de Polymarket
"""
import requests
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from typing import List, Dict, Optional
from logger import get_logger, log_error, log_success

class PolymarketClient:
    """Cliente para interactuar con Polymarket"""

    def __init__(self, config):
        self.config = config
        self.client = None
        self.logger = get_logger()

    def initialize(self):
        """Inicializa el cliente CLOB con autenticación"""
        try:
            self.logger.info('Inicializando cliente de Polymarket...')

            # Crear cliente
            self.client = ClobClient(
                host=self.config.clob_url,
                key=self.config.your_private_key,
                chain_id=self.config.clob_chain_id,
                funder=self.config.your_polymarket_address
            )

            # Derivar o crear API credentials
            self.client.set_api_creds(self.client.create_or_derive_api_creds())

            log_success('Cliente de Polymarket inicializado correctamente')
        except Exception as e:
            log_error('Error al inicializar cliente de Polymarket', e)
            raise

    def get_trader_trades(self, trader_address: str, limit: int = 100) -> List[Dict]:
        """Obtiene los trades recientes de un trader específico"""
        try:
            url = f"{self.config.clob_url}/data/trades"
            params = {
                'maker_address': trader_address.lower(),
                'limit': limit
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_error(f'Error al obtener trades del trader {trader_address}', e)
            return []

    def get_market(self, condition_id: str) -> Optional[Dict]:
        """Obtiene información de un mercado específico"""
        try:
            url = f"{self.config.gamma_api_url}/markets/{condition_id}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_error(f'Error al obtener información del mercado {condition_id}', e)
            return None

    def get_token_price(self, token_id: str) -> Optional[float]:
        """Obtiene el precio actual de un token"""
        try:
            url = f"{self.config.gamma_api_url}/prices"
            response = requests.get(url, params={'token_id': token_id})
            response.raise_for_status()

            data = response.json()
            if token_id in data:
                return float(data[token_id])
            return None
        except Exception as e:
            log_error(f'Error al obtener precio del token {token_id}', e)
            return None

    def create_order(
        self,
        token_id: str,
        price: float,
        side: str,
        size: float,
        tick_size: float,
        neg_risk: bool
    ) -> Dict:
        """Crea y ejecuta una orden en Polymarket"""
        if not self.client:
            return {'success': False, 'error': 'Cliente no inicializado'}

        try:
            self.logger.info(
                f"Creando orden: {side} {size:.2f} @ ${price:.3f} "
                f"(Token: {token_id[:8]}...)"
            )

            # Preparar argumentos de la orden
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=side,
                fee_rate_bps=0,
                nonce=0,
                expiration=0,
            )

            # Crear y postear orden
            signed_order = self.client.create_order(order_args)
            resp = self.client.post_order(signed_order, OrderType.GTC)

            if resp and 'orderID' in resp:
                return {'success': True, 'order_id': resp['orderID']}
            else:
                return {'success': False, 'error': 'No se recibió ID de orden'}

        except Exception as e:
            return {
                'success': False,
                'error': str(e) or 'Error desconocido al crear orden'
            }

    def is_initialized(self) -> bool:
        """Verifica si el cliente está correctamente inicializado"""
        return self.client is not None
