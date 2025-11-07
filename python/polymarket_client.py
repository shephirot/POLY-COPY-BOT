"""
Cliente para interactuar con la API de Polymarket
"""
import requests
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType, TradeParams
from typing import List, Dict, Optional
from logger import get_logger, log_error, log_success, log_warning

class PolymarketClient:
    """Cliente para interactuar con Polymarket"""

    def __init__(self, config):
        self.config = config
        self.client = None
        self.logger = get_logger()

        # Headers para requests públicas
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }

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
        """
        Obtiene los trades recientes de un trader específico
        Usa el cliente autenticado de py-clob-client
        """
        try:
            self.logger.debug(f"Obteniendo trades de {trader_address[:10]}... usando py-clob-client")

            # Método 1: Usar el cliente py-clob-client autenticado
            if self.client:
                try:
                    # Crear parámetros de trade
                    trade_params = TradeParams(
                        maker_address=trader_address.lower()
                    )

                    # Obtener trades usando el cliente autenticado
                    trades = self.client.get_trades(trade_params)

                    if trades:
                        self.logger.debug(f"Se obtuvieron {len(trades)} trades via py-clob-client")
                        return trades[:limit]  # Limitar resultados
                    else:
                        self.logger.debug("No se encontraron trades para este trader")
                        return []

                except AttributeError:
                    # Si get_trades no existe, intentar método alternativo
                    self.logger.debug("get_trades() no disponible, intentando método HTTP...")
                    return self._get_trades_http(trader_address, limit)
                except Exception as e:
                    self.logger.debug(f"Error con py-clob-client: {e}, intentando HTTP...")
                    return self._get_trades_http(trader_address, limit)
            else:
                return self._get_trades_http(trader_address, limit)

        except Exception as e:
            log_error(f'Error inesperado al obtener trades', e)
            return []

    def _get_trades_http(self, trader_address: str, limit: int) -> List[Dict]:
        """
        Método alternativo: obtener trades via HTTP directo
        """
        try:
            # Intentar endpoint público primero
            url = f"{self.config.clob_url}/data/trades"
            params = {
                'maker_address': trader_address.lower(),
                'limit': limit
            }

            self.logger.debug(f"Intentando endpoint HTTP: {url}")
            response = requests.get(url, params=params, headers=self.headers, timeout=10)

            # Manejar diferentes códigos de error
            if response.status_code == 401:
                log_warning(
                    "Endpoint /data/trades requiere autenticacion. "
                    "El endpoint puede haber cambiado."
                )
                # Intentar endpoint alternativo
                return self._get_trades_alternative(trader_address, limit)
            elif response.status_code == 403:
                log_error("Error 403: Acceso prohibido")
                log_warning("Posibles causas:")
                log_warning("  1. Restriccion IP/pais (poco probable en Espana)")
                log_warning("  2. El endpoint cambio o ya no esta disponible")
                log_warning("  3. Se requiere autenticacion adicional")
                return []
            elif response.status_code == 429:
                log_error("Error 429: Demasiadas peticiones")
                return []

            response.raise_for_status()
            data = response.json()

            if data:
                self.logger.debug(f"Se obtuvieron {len(data)} trades via HTTP")

            return data

        except requests.exceptions.Timeout:
            log_error("Timeout al conectar - verifica tu conexion")
            return []
        except requests.exceptions.ConnectionError:
            log_error("Error de conexion - verifica tu internet")
            return []
        except requests.exceptions.RequestException as e:
            log_error(f"Error HTTP: {type(e).__name__}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.debug(f"Status: {e.response.status_code}")
            return []
        except Exception as e:
            self.logger.debug(f'Error en _get_trades_http: {e}')
            return []

    def _get_trades_alternative(self, trader_address: str, limit: int) -> List[Dict]:
        """
        Método alternativo: obtener trades del usuario desde sus órdenes
        """
        try:
            log_warning("Intentando metodo alternativo para obtener trades...")

            # Si el usuario tiene el cliente autenticado, podemos intentar
            # obtener las órdenes y trades de otra forma
            if not self.client:
                log_error("No se puede usar metodo alternativo sin cliente autenticado")
                return []

            # Nota: Este método depende de la API de py-clob-client
            # Si falla, no hay forma de obtener los trades del trader objetivo
            log_warning(
                "IMPORTANTE: El endpoint de trades publico ya no esta disponible. "
                "Opciones:"
            )
            log_warning("  1. Contacta al trader y pidele que comparta sus trades")
            log_warning("  2. Monitorea los mercados directamente en lugar del trader")
            log_warning("  3. Espera a que Polymarket restaure el endpoint publico")

            return []

        except Exception as e:
            self.logger.debug(f"Error en metodo alternativo: {e}")
            return []

    def get_market(self, condition_id: str) -> Optional[Dict]:
        """Obtiene información de un mercado específico"""
        try:
            url = f"{self.config.gamma_api_url}/markets/{condition_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            log_error(f"Timeout al obtener mercado {condition_id[:10]}...")
            return None
        except requests.exceptions.RequestException as e:
            log_error(f'Error al obtener mercado', e)
            return None
        except Exception as e:
            log_error(f'Error inesperado al obtener mercado', e)
            return None

    def get_token_price(self, token_id: str) -> Optional[float]:
        """Obtiene el precio actual de un token"""
        try:
            url = f"{self.config.gamma_api_url}/prices"
            response = requests.get(
                url,
                params={'token_id': token_id},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if token_id in data:
                return float(data[token_id])
            return None
        except Exception as e:
            self.logger.debug(f'Error al obtener precio: {e}')
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
            error_msg = str(e) or 'Error desconocido al crear orden'
            return {
                'success': False,
                'error': error_msg
            }

    def is_initialized(self) -> bool:
        """Verifica si el cliente está correctamente inicializado"""
        return self.client is not None
