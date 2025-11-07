# 🧪 Guía de Testing - Bot de Copy Trading

Esta guía te ayudará a probar el bot usando tu propia wallet de Polymarket.

## ✅ Todas las Correcciones Aplicadas

El bot ahora incluye todas las correcciones necesarias:

- ✅ **Error Windows (UnicodeEncodeError)**: Símbolos compatibles con Windows
- ✅ **Error 401 (Unauthorized)**: Usa cliente autenticado py-clob-client
- ✅ **Error Timestamp (KeyError)**: Manejo robusto de campos variables
- ✅ **Test con propia wallet**: Ahora puedes usar tu misma dirección

## 📋 Configuración para Auto-Test

### Paso 1: Editar el archivo `.env`

```bash
# Windows
notepad ..\.env

# Linux/Mac
nano ../.env
```

### Paso 2: Configurar AMBAS direcciones con TU wallet

```env
# USA TU MISMA DIRECCIÓN EN AMBOS CAMPOS:
# Nota: Puedes poner una sola dirección o varias separadas por comas
TARGET_TRADER_ADDRESS=0xTU_DIRECCION_AQUI
YOUR_POLYMARKET_ADDRESS=0xTU_DIRECCION_AQUI
YOUR_PRIVATE_KEY=0xTU_CLAVE_PRIVADA_AQUI

# O para copiar MÚLTIPLES wallets (incluyendo la tuya para testing):
# TARGET_TRADER_ADDRESS=0xTU_DIRECCION,0xOTRA_DIRECCION,0xTERCERA_DIRECCION

# IMPORTANTE: Activar modo DRY RUN para pruebas seguras
DRY_RUN=true

# Modo de copiado (elige uno)
COPY_MODE=fixed
FIXED_STAKE_SIZE=10

# Configuración de detección
MAX_TRADE_AGE_MINUTES=60
POLL_INTERVAL=5000

# Debug para ver más información
LOG_LEVEL=DEBUG
```

### ⚠️ IMPORTANTE: Dónde obtener tu dirección

Hay DOS direcciones en Polymarket, necesitas la **CORRECTA**:

1. **Ve a Polymarket**: https://polymarket.com/
2. **Haz clic en tu wallet** (arriba derecha)
3. **Copia la dirección que aparece** (empieza con 0x)

Esta es tu **Funder Address** (la que necesitas).

**NO uses** la dirección de la blockchain directamente - usa la que aparece en tu perfil de Polymarket.

## 🚀 Paso 3: Ejecutar el Bot

```bash
# Windows
python main.py

# Linux/Mac
python3 main.py
```

### Deberías ver algo como:

```
============================================================
  POLYMARKET COPY TRADING BOT
============================================================

Inicializando cliente de Polymarket...
[OK] Cliente de Polymarket inicializado correctamente
[OK] Configuración cargada correctamente

Configuración:
  Trader objetivo: 0xTU_DIRE...
  Tu dirección: 0xTU_DIRE...
  Modo de copiado: STAKE FIJO ($10 por trade)
  Tamaño min/max: $1 - $1000
  Slippage máximo: 2.0%
  Intervalo de polling: 5000ms
  Modo: DRY RUN (Simulación)

============================================================

[!] MODO TEST: Estas monitoreando tus propios trades
[!] Esto es util para testear el bot. Haz un trade en Polymarket para verlo funcionar.
[!] [!] MODO DRY RUN ACTIVADO - No se ejecutarán trades reales

[OK] Bot iniciado - Monitoreando trades...
```

## 📊 Paso 4: Hacer un Trade de Prueba

1. **Abre Polymarket** en tu navegador: https://polymarket.com/
2. **Encuentra cualquier mercado** (ejemplo: elecciones, deportes, etc.)
3. **Haz un trade pequeño** (ejemplo: $5-$10)
4. **Espera 5-10 segundos**

### El bot debería detectarlo:

```
DEBUG: Obteniendo trades de 0xTU_DIRE... usando py-clob-client
DEBUG: Se obtuvieron 3 trades via py-clob-client
DEBUG: Estructura del primer trade: ['id', 'market', 'asset_id', 'side', 'size', 'price', ...]

📥 Detectados 1 nuevos trades

[TRADE] Trade detectado: BUY 100.0 @ $0.52
DEBUG: Modo stake fijo: $10 ÷ $0.52 = 19.23 tokens
DEBUG: Orden final: 19.23 tokens @ $0.52 = $10.00
[!] [DRY RUN] Simulando: BUY 19.23 @ $0.52
[OK] Orden ejecutada exitosamente! ID: DRY-RUN-1699123456789
```

## ❓ Problemas Comunes

### El bot no detecta mi trade

**Solución 1**: Aumenta `MAX_TRADE_AGE_MINUTES`
```env
MAX_TRADE_AGE_MINUTES=120  # 2 horas
```

**Solución 2**: Verifica la dirección
- Usa la dirección que aparece en tu perfil de Polymarket
- NO la dirección de la blockchain

**Solución 3**: Activa DEBUG
```env
LOG_LEVEL=DEBUG
```

Verás mensajes como:
```
DEBUG: Obteniendo trades de 0x123...
DEBUG: Se obtuvieron 5 trades via py-clob-client
DEBUG: Estructura del primer trade: ['id', 'market', 'side', ...]
```

### Aún veo el error de timestamp

Si ves:
```
[ERROR] [X] Error en el loop principal
[ERROR] 'timestamp'
```

**Ya está arreglado** en la última versión. Descarga el código actualizado:

```bash
git pull origin claude/polymarket-copy-trading-bot-011CUtCzeegna6FnU6VM4yS8
```

### Veo "No se obtuvieron trades"

Esto es normal si:
1. No has hecho ningún trade recientemente
2. Tus trades son muy antiguos (más de `MAX_TRADE_AGE_MINUTES`)
3. La API está tardando en responder

**Haz un trade nuevo** en Polymarket y espera 5-10 segundos.

## 🎯 Pasar a Modo LIVE

Una vez que el bot funciona correctamente en DRY RUN:

### 1. Editar `.env`:

```env
# Cambiar a FALSE para ejecutar trades reales
DRY_RUN=false

# Ajustar límites de seguridad
MIN_ORDER_SIZE=5
MAX_ORDER_SIZE=100

# Cambiar a la dirección del trader que quieres copiar
TARGET_TRADER_ADDRESS=0xDIRECCION_DEL_TRADER_PRO
```

### 2. Ejecutar:

```bash
python main.py
```

Deberías ver:
```
Modo: LIVE TRADING
```

### ⚠️ ADVERTENCIA

- **LIVE TRADING ejecuta trades reales con dinero real**
- Empieza con cantidades pequeñas
- Monitorea el bot constantemente al principio
- Ajusta `MAX_ORDER_SIZE` para limitar el riesgo

## 📝 Revisar Logs

El bot guarda TODO en `bot.log`:

```bash
# Ver últimas 50 líneas
tail -n 50 bot.log

# Buscar errores
grep ERROR bot.log

# Ver en tiempo real
tail -f bot.log
```

## ✅ Checklist de Testing

- [ ] Archivo `.env` configurado con TU dirección en ambos campos
- [ ] `DRY_RUN=true` activado
- [ ] `LOG_LEVEL=DEBUG` activado
- [ ] Bot arranca sin errores
- [ ] Ves mensaje "MODO TEST: Estas monitoreando tus propios trades"
- [ ] Hiciste un trade en Polymarket
- [ ] El bot detectó el trade
- [ ] Ves mensaje "[DRY RUN] Simulando: ..."
- [ ] Orden reportada como exitosa

## 🎉 Siguiente Paso

Si todo funciona:

1. **Encuentra un trader profesional** en: https://polymarket.com/leaderboard
2. **Copia su dirección**
3. **Cambia `TARGET_TRADER_ADDRESS`** en `.env`
4. **Prueba primero con `DRY_RUN=true`**
5. **Luego cambia a `DRY_RUN=false`** para copiar en vivo

## 📚 Más Ayuda

- [README Python](README_PYTHON.md) - Documentación completa
- [TROUBLESHOOTING](TROUBLESHOOTING.md) - Solución de problemas
- [MODOS_COPIADO](../MODOS_COPIADO.md) - Porcentaje vs Fijo

---

**¿Todo funcionando?** ¡Genial! Ahora puedes empezar a copiar traders profesionales en Polymarket.

**¿Problemas?** Revisa `bot.log` y consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
