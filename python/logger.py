"""
Sistema de logging profesional con colores
"""
import logging
from datetime import datetime
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Formatter personalizado con colores"""

    COLORS = {
        'DEBUG': Fore.MAGENTA,
        'INFO': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Agregar color al nivel
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"

        return super().format(record)

def setup_logger(log_level='INFO'):
    """Configura el logger principal"""
    logger = logging.getLogger('PolymarketBot')
    logger.setLevel(getattr(logging, log_level.upper()))

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Formato
    formatter = ColoredFormatter(
        f'{Fore.WHITE}%(asctime)s{Style.RESET_ALL} [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Handler para archivo
    file_handler = logging.FileHandler('bot.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Agregar handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Logger global
logger = None

def get_logger():
    """Obtiene el logger global"""
    global logger
    if logger is None:
        logger = setup_logger()
    return logger

def log_success(message):
    """Log de éxito con símbolo verde"""
    get_logger().info(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def log_error(message, error=None):
    """Log de error con símbolo rojo"""
    get_logger().error(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    if error:
        get_logger().error(f"{Fore.RED}{str(error)}{Style.RESET_ALL}")

def log_warning(message):
    """Log de advertencia con símbolo amarillo"""
    get_logger().warning(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def log_trade(message):
    """Log de trade con símbolo cyan"""
    get_logger().info(f"{Fore.CYAN}💱 {message}{Style.RESET_ALL}")

def log_stats(message):
    """Log de estadísticas con símbolo magenta"""
    get_logger().info(f"{Fore.MAGENTA}📊 {message}{Style.RESET_ALL}")
