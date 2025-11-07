#!/usr/bin/env python3
"""
Punto de entrada principal del bot de copy trading
"""
import signal
import sys
from colorama import Fore, Style
from config import load_config
from copy_trading_bot import CopyTradingBot
from logger import setup_logger, log_error

def signal_handler(sig, frame):
    """Maneja señales de terminación"""
    print()
    print(f"{Fore.YELLOW}Señal de terminación recibida...{Style.RESET_ALL}")
    if bot:
        bot.stop()
    sys.exit(0)

def main():
    """Función principal"""
    global bot
    bot = None

    try:
        # Cargar configuración
        config = load_config()

        # Configurar logger con el nivel especificado
        setup_logger(config.log_level)

        # Crear e inicializar el bot
        bot = CopyTradingBot(config)
        bot.initialize()

        # Manejar señales de terminación
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Iniciar el bot
        bot.start()

    except Exception as e:
        log_error('Error fatal en el bot', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
