#!/usr/bin/env python3
"""
Script de validación de configuración para el bot de copy trading
Ejecuta este script antes de iniciar el bot para verificar que todo esté configurado correctamente
"""
import os
import sys
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

def print_header():
    print("=" * 70)
    print(f"{Fore.CYAN}{Style.BRIGHT}  VALIDADOR DE CONFIGURACIÓN - BOT COPY TRADING{Style.RESET_ALL}")
    print("=" * 70)
    print()

def check_env_file():
    """Verifica que existe el archivo .env"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

    if not os.path.exists(env_path):
        print(f"{Fore.RED}✗ FALTA: Archivo .env no encontrado{Style.RESET_ALL}")
        print(f"  → Ubicación esperada: {env_path}")
        print(f"  → Solución: cp ../.env.example ../.env")
        return False

    print(f"{Fore.GREEN}✓ Archivo .env encontrado{Style.RESET_ALL}")
    return True

def validate_address(address, name):
    """Valida una dirección de Ethereum"""
    if not address:
        print(f"{Fore.RED}✗ FALTA: {name} no está configurado{Style.RESET_ALL}")
        return False

    if not address.startswith('0x'):
        print(f"{Fore.RED}✗ ERROR: {name} debe empezar con '0x'{Style.RESET_ALL}")
        print(f"  → Valor actual: {address}")
        return False

    if len(address) != 42:
        print(f"{Fore.YELLOW}⚠ ADVERTENCIA: {name} tiene longitud incorrecta{Style.RESET_ALL}")
        print(f"  → Longitud esperada: 42 caracteres (incluye '0x'))")
        print(f"  → Longitud actual: {len(address)}")
        return False

    print(f"{Fore.GREEN}✓ {name}: {address[:10]}...{address[-8:]}{Style.RESET_ALL}")
    return True

def validate_private_key(key):
    """Valida la clave privada"""
    if not key:
        print(f"{Fore.RED}✗ FALTA: YOUR_PRIVATE_KEY no está configurado{Style.RESET_ALL}")
        return False

    if not key.startswith('0x'):
        print(f"{Fore.RED}✗ ERROR: YOUR_PRIVATE_KEY debe empezar con '0x'{Style.RESET_ALL}")
        return False

    if len(key) != 66:
        print(f"{Fore.YELLOW}⚠ ADVERTENCIA: YOUR_PRIVATE_KEY tiene longitud incorrecta{Style.RESET_ALL}")
        print(f"  → Longitud esperada: 66 caracteres")
        print(f"  → Longitud actual: {len(key)}")
        return False

    print(f"{Fore.GREEN}✓ YOUR_PRIVATE_KEY: {key[:6]}...{key[-4:]} (longitud correcta){Style.RESET_ALL}")
    return True

def validate_copy_mode(mode, multiplier, fixed_size):
    """Valida el modo de copiado"""
    if mode not in ['percentage', 'fixed']:
        print(f"{Fore.RED}✗ ERROR: COPY_MODE debe ser 'percentage' o 'fixed'{Style.RESET_ALL}")
        print(f"  → Valor actual: {mode}")
        return False

    print(f"{Fore.GREEN}✓ COPY_MODE: {mode}{Style.RESET_ALL}")

    if mode == 'percentage':
        try:
            mult = float(multiplier)
            if mult <= 0:
                print(f"{Fore.RED}✗ ERROR: COPY_SIZE_MULTIPLIER debe ser mayor que 0{Style.RESET_ALL}")
                return False
            print(f"{Fore.GREEN}  → Multiplicador: {mult}x del tamaño del trader{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}✗ ERROR: COPY_SIZE_MULTIPLIER debe ser un número{Style.RESET_ALL}")
            return False

    if mode == 'fixed':
        try:
            size = float(fixed_size)
            if size <= 0:
                print(f"{Fore.RED}✗ ERROR: FIXED_STAKE_SIZE debe ser mayor que 0{Style.RESET_ALL}")
                return False
            print(f"{Fore.GREEN}  → Stake fijo: ${size} por trade{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}✗ ERROR: FIXED_STAKE_SIZE debe ser un número{Style.RESET_ALL}")
            return False

    return True

def validate_numeric(value, name, min_val=None, max_val=None):
    """Valida un valor numérico"""
    try:
        num = float(value)

        if min_val is not None and num < min_val:
            print(f"{Fore.RED}✗ ERROR: {name} debe ser >= {min_val}{Style.RESET_ALL}")
            return False

        if max_val is not None and num > max_val:
            print(f"{Fore.RED}✗ ERROR: {name} debe ser <= {max_val}{Style.RESET_ALL}")
            return False

        print(f"{Fore.GREEN}✓ {name}: {num}{Style.RESET_ALL}")
        return True
    except ValueError:
        print(f"{Fore.RED}✗ ERROR: {name} debe ser un número{Style.RESET_ALL}")
        return False

def check_self_test_mode(target, your):
    """Verifica si está en modo de auto-test"""
    if target.lower() == your.lower():
        print()
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ℹ️  MODO AUTO-TEST DETECTADO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print()
        print(f"  Estás monitoreando tus propios trades.")
        print(f"  Esto es perfecto para probar el bot.")
        print()
        print(f"  {Fore.CYAN}Para probar:{Style.RESET_ALL}")
        print(f"  1. Asegúrate de que DRY_RUN=true")
        print(f"  2. Ejecuta el bot: python main.py")
        print(f"  3. Haz un trade en Polymarket")
        print(f"  4. El bot debería detectarlo en 5-10 segundos")
        print()
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print()

def main():
    print_header()

    # Cargar .env
    if not check_env_file():
        print()
        print(f"{Fore.RED}FALLO: No se puede continuar sin archivo .env{Style.RESET_ALL}")
        sys.exit(1)

    # Cargar variables de entorno
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path)

    print()
    print(f"{Style.BRIGHT}1. Validando direcciones y claves...{Style.RESET_ALL}")
    print()

    target_addresses_raw = os.getenv('TARGET_TRADER_ADDRESS', '')
    target_addresses = [addr.strip() for addr in target_addresses_raw.split(',') if addr.strip()]
    your_address = os.getenv('YOUR_POLYMARKET_ADDRESS', '')
    private_key = os.getenv('YOUR_PRIVATE_KEY', '')

    valid = True

    # Validar cada dirección de trader
    if not target_addresses:
        print(f"{Fore.RED}✗ FALTA: TARGET_TRADER_ADDRESS no está configurado{Style.RESET_ALL}")
        valid = False
    else:
        if len(target_addresses) == 1:
            print(f"{Fore.CYAN}Modo: 1 trader{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Modo: {len(target_addresses)} traders (multi-wallet){Style.RESET_ALL}")
        print()

        for i, addr in enumerate(target_addresses, 1):
            if len(target_addresses) > 1:
                print(f"  Trader #{i}:")
            valid &= validate_address(addr, f'TARGET_TRADER_ADDRESS[{i}]' if len(target_addresses) > 1 else 'TARGET_TRADER_ADDRESS')

        print()

    valid &= validate_address(your_address, 'YOUR_POLYMARKET_ADDRESS')
    valid &= validate_private_key(private_key)

    # Verificar modo auto-test
    if target_addresses and your_address:
        for target_address in target_addresses:
            if target_address.lower() == your_address.lower():
                check_self_test_mode(target_address, your_address)
                break

    print()
    print(f"{Style.BRIGHT}2. Validando configuración de trading...{Style.RESET_ALL}")
    print()

    copy_mode = os.getenv('COPY_MODE', 'percentage').lower()
    copy_size_multiplier = os.getenv('COPY_SIZE_MULTIPLIER', '1.0')
    fixed_stake_size = os.getenv('FIXED_STAKE_SIZE', '10')

    valid &= validate_copy_mode(copy_mode, copy_size_multiplier, fixed_stake_size)

    print()
    print(f"{Style.BRIGHT}3. Validando límites de riesgo...{Style.RESET_ALL}")
    print()

    min_order = os.getenv('MIN_ORDER_SIZE', '1')
    max_order = os.getenv('MAX_ORDER_SIZE', '1000')
    max_slippage = os.getenv('MAX_SLIPPAGE', '0.02')

    valid &= validate_numeric(min_order, 'MIN_ORDER_SIZE', min_val=0)
    valid &= validate_numeric(max_order, 'MAX_ORDER_SIZE', min_val=0)
    valid &= validate_numeric(max_slippage, 'MAX_SLIPPAGE', min_val=0, max_val=1)

    # Validar que max > min
    if float(max_order) < float(min_order):
        print(f"{Fore.RED}✗ ERROR: MAX_ORDER_SIZE debe ser mayor que MIN_ORDER_SIZE{Style.RESET_ALL}")
        valid = False

    print()
    print(f"{Style.BRIGHT}4. Validando configuración de operación...{Style.RESET_ALL}")
    print()

    dry_run = os.getenv('DRY_RUN', 'true').lower()

    if dry_run == 'true':
        print(f"{Fore.YELLOW}✓ DRY_RUN: Activado (Simulación - Seguro){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}⚠ DRY_RUN: Desactivado (¡TRADES REALES!){Style.RESET_ALL}")
        print(f"  → {Fore.RED}Se ejecutarán trades reales con dinero real{Style.RESET_ALL}")

    log_level = os.getenv('LOG_LEVEL', 'INFO')
    print(f"{Fore.GREEN}✓ LOG_LEVEL: {log_level}{Style.RESET_ALL}")

    if log_level.upper() == 'DEBUG':
        print(f"  → Verás información detallada de debug")

    # Resumen final
    print()
    print("=" * 70)

    if valid:
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ VALIDACIÓN EXITOSA{Style.RESET_ALL}")
        print()
        print("Todas las configuraciones son válidas.")
        print()
        print(f"{Fore.CYAN}Siguiente paso:{Style.RESET_ALL}")
        print("  python main.py")
        print()

        if dry_run == 'true':
            print(f"{Fore.YELLOW}Recuerda:{Style.RESET_ALL} Estás en modo DRY RUN (simulación)")
            print("Para ver el bot en acción, haz un trade en Polymarket.")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}¡ADVERTENCIA!{Style.RESET_ALL} Estás en modo LIVE")
            print("El bot ejecutará trades reales. Monitorea cuidadosamente.")

        print()
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"{Fore.RED}{Style.BRIGHT}✗ VALIDACIÓN FALLIDA{Style.RESET_ALL}")
        print()
        print("Por favor, corrige los errores anteriores en tu archivo .env")
        print()
        print(f"{Fore.CYAN}Para editar .env:{Style.RESET_ALL}")
        print("  Windows: notepad ../.env")
        print("  Linux/Mac: nano ../.env")
        print()
        print("Luego ejecuta este validador nuevamente:")
        print("  python validate_config.py")
        print()
        print("=" * 70)
        sys.exit(1)

if __name__ == '__main__':
    main()
