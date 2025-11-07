"""
Carga y valida la configuración del bot
"""
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional, List
from logger import log_error, get_logger

# Cargar variables de entorno
load_dotenv()

@dataclass
class BotConfig:
    """Configuración del bot"""
    # Credenciales
    target_trader_addresses: List[str]  # Lista de direcciones a copiar
    your_polymarket_address: str
    your_private_key: str

    # URLs
    clob_url: str
    clob_chain_id: int
    gamma_api_url: str

    # Parámetros de trading
    copy_mode: str  # 'percentage' o 'fixed'
    copy_size_multiplier: float
    fixed_stake_size: float
    min_order_size: float
    max_order_size: float
    max_slippage: float

    # Monitoreo
    poll_interval: int
    max_trade_age_minutes: int

    # Reintentos
    max_retries: int
    retry_delay: int

    # Operación
    dry_run: bool
    log_level: str

    # Filtros
    blacklist_markets: Optional[List[str]] = None
    whitelist_markets: Optional[List[str]] = None
    copy_sides: List[str] = None

def load_config() -> BotConfig:
    """Carga y valida la configuración"""
    logger = get_logger()

    # Validar variables requeridas
    required = [
        'TARGET_TRADER_ADDRESS',
        'YOUR_POLYMARKET_ADDRESS',
        'YOUR_PRIVATE_KEY'
    ]

    missing = [key for key in required if not os.getenv(key)]
    if missing:
        log_error(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
        log_error("Copia .env.example a .env y configura las variables necesarias")
        exit(1)

    # Parsear direcciones de traders (puede ser una o varias separadas por coma)
    target_addresses_raw = os.getenv('TARGET_TRADER_ADDRESS', '')
    target_addresses = [addr.strip() for addr in target_addresses_raw.split(',') if addr.strip()]

    if not target_addresses:
        log_error("TARGET_TRADER_ADDRESS está vacío")
        exit(1)

    # Validar formato de direcciones
    for addr in target_addresses:
        if not addr.startswith('0x') or len(addr) != 42:
            log_error(f"Dirección inválida: {addr}")
            log_error("Las direcciones deben empezar con 0x y tener 42 caracteres")
            exit(1)

    logger.info(f'Se monitorearan {len(target_addresses)} trader(s)')

    # Parsear filtros
    blacklist_markets = None
    if os.getenv('BLACKLIST_MARKETS'):
        blacklist_markets = [m.strip() for m in os.getenv('BLACKLIST_MARKETS').split(',')]

    whitelist_markets = None
    if os.getenv('WHITELIST_MARKETS'):
        whitelist_markets = [m.strip() for m in os.getenv('WHITELIST_MARKETS').split(',')]

    copy_sides = ['BUY', 'SELL']
    if os.getenv('COPY_SIDES'):
        copy_sides = [s.strip() for s in os.getenv('COPY_SIDES').split(',')]

    # Validar y parsear modo de copiado
    copy_mode = os.getenv('COPY_MODE', 'percentage').lower()
    if copy_mode not in ['percentage', 'fixed']:
        log_error('COPY_MODE debe ser "percentage" o "fixed"')
        exit(1)

    config = BotConfig(
        target_trader_addresses=target_addresses,
        your_polymarket_address=os.getenv('YOUR_POLYMARKET_ADDRESS'),
        your_private_key=os.getenv('YOUR_PRIVATE_KEY'),

        clob_url=os.getenv('CLOB_URL', 'https://clob.polymarket.com'),
        clob_chain_id=int(os.getenv('CLOB_CHAIN_ID', '137')),
        gamma_api_url=os.getenv('GAMMA_API_URL', 'https://gamma-api.polymarket.com'),

        copy_mode=copy_mode,
        copy_size_multiplier=float(os.getenv('COPY_SIZE_MULTIPLIER', '1.0')),
        fixed_stake_size=float(os.getenv('FIXED_STAKE_SIZE', '10')),
        min_order_size=float(os.getenv('MIN_ORDER_SIZE', '1')),
        max_order_size=float(os.getenv('MAX_ORDER_SIZE', '1000')),
        max_slippage=float(os.getenv('MAX_SLIPPAGE', '0.02')),

        poll_interval=int(os.getenv('POLL_INTERVAL', '5000')),
        max_trade_age_minutes=int(os.getenv('MAX_TRADE_AGE_MINUTES', '5')),

        max_retries=int(os.getenv('MAX_RETRIES', '3')),
        retry_delay=int(os.getenv('RETRY_DELAY', '2000')),

        dry_run=os.getenv('DRY_RUN', 'true').lower() == 'true',
        log_level=os.getenv('LOG_LEVEL', 'INFO'),

        blacklist_markets=blacklist_markets,
        whitelist_markets=whitelist_markets,
        copy_sides=copy_sides
    )

    # Validaciones
    if config.copy_mode == 'percentage':
        if config.copy_size_multiplier <= 0:
            log_error('COPY_SIZE_MULTIPLIER debe ser mayor que 0 (modo percentage)')
            exit(1)
    elif config.copy_mode == 'fixed':
        if config.fixed_stake_size <= 0:
            log_error('FIXED_STAKE_SIZE debe ser mayor que 0 (modo fixed)')
            exit(1)

    if config.min_order_size < 0 or config.max_order_size < config.min_order_size:
        log_error('MIN_ORDER_SIZE y MAX_ORDER_SIZE deben ser válidos')
        exit(1)

    if config.max_slippage < 0 or config.max_slippage > 1:
        log_error('MAX_SLIPPAGE debe estar entre 0 y 1')
        exit(1)

    # Información si está usando su propia wallet
    if config.your_polymarket_address.lower() in [addr.lower() for addr in config.target_trader_addresses]:
        from logger import log_warning
        log_warning('MODO TEST: Estas monitoreando tus propios trades')
        log_warning('Esto es util para testear el bot. Haz un trade en Polymarket para verlo funcionar.')

    logger.info('✓ Configuración cargada correctamente')
    return config
