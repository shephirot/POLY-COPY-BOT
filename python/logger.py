"""
Sistema de logging profesional con colores
Compatible con Windows y Unix
"""
import logging
import sys
import platform
from datetime import datetime
from colorama import Fore, Style, init

# Inicializar colorama para Windows
init(autoreset=True, strip=False)

# Detectar si estamos en Windows
IS_WINDOWS = platform.system() == 'Windows'

# Símbolos compatibles con Windows
if IS_WINDOWS:
    SYMBOL_SUCCESS = '[OK]'
    SYMBOL_ERROR = '[X]'
    SYMBOL_WARNING = '[!]'
    SYMBOL_TRADE = '[TRADE]'
    SYMBOL_STATS = '[STATS]'
else:
    SYMBOL_SUCCESS = '✓'
    SYMBOL_ERROR = '✗'
    SYMBOL_WARNING = '⚠'
    SYMBOL_TRADE = '💱'
    SYMBOL_STATS = '📊'

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

class SafeFileHandler(logging.FileHandler):
    """File handler que maneja encoding correctamente"""

    def __init__(self, filename, mode='a', encoding='utf-8', delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        try:
            super().emit(record)
        except UnicodeEncodeError:
            # Si falla, intentar sin caracteres especiales
            record.msg = self._remove_special_chars(str(record.msg))
            super().emit(record)

    def _remove_special_chars(self, text):
        """Remueve caracteres Unicode problemáticos"""
        replacements = {
            '✓': '[OK]',
            '✗': '[X]',
            '⚠': '[!]',
            '💱': '[TRADE]',
            '📊': '[STATS]',
            '🚀': '[START]',
            '📥': '[IN]',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

def setup_logger(log_level='INFO'):
    """Configura el logger principal"""
    logger = logging.getLogger('PolymarketBot')
    logger.setLevel(getattr(logging, log_level.upper()))

    # Limpiar handlers existentes
    logger.handlers.clear()

    # Handler para consola con encoding UTF-8
    if IS_WINDOWS:
        # En Windows, intentar configurar UTF-8
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Formato
    formatter = ColoredFormatter(
        f'{Fore.WHITE}%(asctime)s{Style.RESET_ALL} [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Handler para archivo con encoding UTF-8
    file_handler = SafeFileHandler('bot.log', encoding='utf-8')
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
    get_logger().info(f"{Fore.GREEN}{SYMBOL_SUCCESS} {message}{Style.RESET_ALL}")

def log_error(message, error=None):
    """Log de error con símbolo rojo"""
    get_logger().error(f"{Fore.RED}{SYMBOL_ERROR} {message}{Style.RESET_ALL}")
    if error:
        error_msg = str(error)
        # Limpiar el mensaje de error si tiene caracteres problemáticos
        get_logger().error(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")

def log_warning(message):
    """Log de advertencia con símbolo amarillo"""
    get_logger().warning(f"{Fore.YELLOW}{SYMBOL_WARNING} {message}{Style.RESET_ALL}")

def log_trade(message):
    """Log de trade con símbolo cyan"""
    get_logger().info(f"{Fore.CYAN}{SYMBOL_TRADE} {message}{Style.RESET_ALL}")

def log_stats(message):
    """Log de estadísticas con símbolo magenta"""
    get_logger().info(f"{Fore.MAGENTA}{SYMBOL_STATS} {message}{Style.RESET_ALL}")
