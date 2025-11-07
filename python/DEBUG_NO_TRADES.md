# 🔍 Debugging: Bot No Detecta Trades

Esta guía te ayuda a resolver el problema cuando el bot NO está detectando/copiando trades aunque el trader sí está operando.

## 🎯 Síntoma

- El trader está haciendo trades en Polymarket
- El bot está ejecutándose sin errores
- Pero NO detecta ni copia los trades
- Ves mensajes como "No se obtuvieron trades de ningún trader"

## ✅ Checklist Rápido

Antes de hacer debugging profundo, verifica esto:

```bash
# 1. Asegúrate de estar usando LOG_LEVEL=DEBUG
# Edita tu .env:
LOG_LEVEL=DEBUG

# 2. Aumenta MAX_TRADE_AGE_MINUTES temporalmente
MAX_TRADE_AGE_MINUTES=120  # 2 horas en lugar de 5 minutos

# 3. Reinicia el bot
python main.py
```

## 🔍 Paso 1: Verificar la Dirección del Trader

### Problema Común: Dirección Incorrecta

Polymarket tiene DOS tipos de direcciones:

1. **Funder Address** (la correcta) ✅
2. **Blockchain Address** (la incorrecta) ❌

### Cómo Obtener la Dirección Correcta

1. Ve a Polymarket: https://polymarket.com/
2. Busca el perfil del trader que quieres copiar
3. Haz clic en su perfil
4. **Copia la dirección que aparece en la URL o en su perfil**

Ejemplo:
```
URL: https://polymarket.com/profile/0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                 Esta es la dirección correcta
```

### Verificar tu Configuración

```bash
# Windows
notepad ..\.env

# Linux/Mac
nano ../.env
```

Verifica que `TARGET_TRADER_ADDRESS` sea exactamente la dirección del perfil:

```env
# CORRECTO:
TARGET_TRADER_ADDRESS=0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1

# INCORRECTO (dirección de blockchain):
TARGET_TRADER_ADDRESS=0x...otra_direccion...
```

## 🔍 Paso 2: Verificar MAX_TRADE_AGE_MINUTES

### Problema: Ventana de Tiempo Muy Pequeña

Por defecto, el bot solo busca trades de los últimos **5 minutos**.

Si:
- El trader hizo un trade hace 10 minutos
- Inicias el bot ahora
- El bot NO lo detectará (demasiado antiguo)

### Solución: Aumentar la Ventana

```env
# En .env, aumenta este valor:
MAX_TRADE_AGE_MINUTES=60  # 1 hora
# o incluso
MAX_TRADE_AGE_MINUTES=120  # 2 horas
```

**Nota:** Una vez que el bot detecte un trade, seguirá monitoreando y detectará trades nuevos automáticamente. Este parámetro es principalmente para el **inicio** del bot.

## 🔍 Paso 3: Analizar los Logs con DEBUG

### Activar Modo DEBUG

```env
# En .env:
LOG_LEVEL=DEBUG
```

### Ejecutar el Bot

```bash
python main.py
```

### Qué Buscar en los Logs

#### Log Normal (Sin Trades):

```
DEBUG: Consultando trades de 0x44c1dfe4...
DEBUG:   → Obtenidos 0 trades  ← PROBLEMA: No encuentra trades
DEBUG: No se obtuvieron trades de ningún trader
```

**Esto significa:** La API no devuelve trades para esa dirección.

**Causas posibles:**
1. Dirección incorrecta
2. El trader no ha operado recientemente
3. Problema con la API de Polymarket

#### Log Normal (Con Trades Detectados):

```
DEBUG: Consultando trades de 0x44c1dfe4...
DEBUG:   → Obtenidos 15 trades
DEBUG: Total de trades obtenidos: 15
DEBUG: Estructura del primer trade: ['id', 'market', 'side', 'size', 'price', ...]
DEBUG: ==================================================
DEBUG: RESUMEN DEL FILTRADO:
DEBUG:   Total trades obtenidos: 15
DEBUG:   Omitidos (ya procesados): 0
DEBUG:   Omitidos (muy antiguos): 12  ← PROBLEMA: Todos muy antiguos
DEBUG:   Omitidos (ya verificados): 0
DEBUG:   Trades NUEVOS detectados: 3
DEBUG: ==================================================

📥 Detectados 3 nuevos trades
```

Si ves "Omitidos (muy antiguos): 12", significa:
- ✅ La dirección es correcta
- ✅ Se están obteniendo trades
- ❌ Pero son demasiado antiguos (más de MAX_TRADE_AGE_MINUTES)

**Solución:** Aumenta `MAX_TRADE_AGE_MINUTES` o espera a que el trader haga un trade nuevo.

## 🔍 Paso 4: Verificar Filtros

### Filtros que Pueden Bloquear Trades

```env
# ¿Estás filtrando solo BUY o SELL?
COPY_SIDES=BUY,SELL  # Debe incluir ambos o el que necesitas

# ¿Tienes una whitelist de mercados?
# WHITELIST_MARKETS=0xmarket1...  ← Si está activado, solo copiará estos mercados

# ¿Tienes una blacklist?
# BLACKLIST_MARKETS=0xmarket1...  ← Si está activado, ignorará estos mercados
```

### Verificar en los Logs

Si ves:
```
[TRADE] Trade detectado: BUY 100.0 @ $0.52
[!] Trade omitido por filtros
```

Entonces el trade fue detectado pero bloqueado por un filtro.

**Solución:** Revisa tus filtros en `.env` y ajústalos.

## 🔍 Paso 5: Verificar Conectividad con Polymarket

### Test Manual

Abre Python y prueba manualmente:

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import TradeParams

# Reemplaza con tu configuración
client = ClobClient(
    host="https://clob.polymarket.com",
    key="0xTU_PRIVATE_KEY",
    chain_id=137,
    funder="0xTU_POLYMARKET_ADDRESS"
)

client.set_api_creds(client.create_or_derive_api_creds())

# Reemplaza con la dirección del trader
trader_address = "0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1"

trade_params = TradeParams(maker_address=trader_address.lower())
trades = client.get_trades(trade_params)

print(f"Trades obtenidos: {len(trades)}")
if trades:
    print(f"Primer trade: {trades[0]}")
```

**Resultado esperado:**
```
Trades obtenidos: 15
Primer trade: {'id': '...', 'market': '...', 'side': 'BUY', ...}
```

Si obtienes 0 trades:
- La dirección está mal
- O el trader no ha operado nunca
- O hay un problema con la API

## 🔍 Paso 6: Verificar Timestamp del Último Trade

A veces el problema es que todos los trades son antiguos.

### Ver Cuándo Fue el Último Trade

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import TradeParams
from datetime import datetime

# ... (configuración del cliente igual que arriba)

trades = client.get_trades(trade_params)

if trades:
    first_trade = trades[0]
    timestamp = first_trade.get('timestamp') or first_trade.get('created_at')

    if timestamp:
        # Convertir a fecha legible
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp / 1000)  # Si está en ms
        print(f"Último trade fue: {dt}")

        # Calcular hace cuánto fue
        now = datetime.now()
        diff = now - dt
        print(f"Hace {diff.total_seconds() / 60:.1f} minutos")
```

Si ves "Hace 180 minutos" (3 horas), y tu `MAX_TRADE_AGE_MINUTES=60`, entonces el bot no lo detectará.

**Solución:**
1. Aumenta `MAX_TRADE_AGE_MINUTES=200`
2. O espera a que el trader haga un trade nuevo

## 📋 Resumen de Parámetros Importantes

```env
# Dirección del trader (CRÍTICO - debe ser correcta)
TARGET_TRADER_ADDRESS=0x...

# Ventana de tiempo (aumentar si no detecta trades existentes)
MAX_TRADE_AGE_MINUTES=120  # 2 horas recomendado para testing

# Intervalo de consulta (no cambiar esto)
POLL_INTERVAL=5000  # 5 segundos

# Logging (SIEMPRE usa DEBUG cuando debugueas)
LOG_LEVEL=DEBUG
```

## 🎯 Casos Comunes Resueltos

### Caso 1: "No se obtuvieron trades de ningún trader"

**Causa:** Dirección incorrecta o trader no ha operado

**Solución:**
1. Verifica la dirección en Polymarket
2. Confirma que el trader ha hecho trades recientemente
3. Prueba con otro trader conocido del leaderboard

### Caso 2: "Omitidos (muy antiguos): 15"

**Causa:** `MAX_TRADE_AGE_MINUTES` muy bajo

**Solución:**
```env
MAX_TRADE_AGE_MINUTES=120  # Aumentar a 2 horas
```

### Caso 3: "Trade omitido por filtros"

**Causa:** Filtros demasiado restrictivos

**Solución:**
```env
COPY_SIDES=BUY,SELL  # Permitir ambos lados
# Comentar WHITELIST_MARKETS si existe
# Comentar BLACKLIST_MARKETS si existe
```

### Caso 4: Detecta trades pero no los copia

**Ver logs:**
```
[TRADE] Trade detectado: BUY 100.0 @ $0.52
  ↳ Trade sin información de mercado
```

**Causa:** El trade no tiene `market_id`

**Solución:** Esto es un problema con los datos de Polymarket. Prueba con otro trader o espera a que el trader haga un trade nuevo.

## 🚀 Configuración Recomendada para Testing

Cuando estés debugueando, usa esta configuración:

```env
# Dirección del trader
TARGET_TRADER_ADDRESS=0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1

# O tu propia dirección para auto-test
# TARGET_TRADER_ADDRESS=0xTU_DIRECCION

# Parámetros amplios para testing
MAX_TRADE_AGE_MINUTES=120  # 2 horas
MIN_ORDER_SIZE=1
MAX_ORDER_SIZE=1000
COPY_SIDES=BUY,SELL

# Modo seguro
DRY_RUN=true

# Logging detallado
LOG_LEVEL=DEBUG

# Sin filtros
# (comenta WHITELIST_MARKETS y BLACKLIST_MARKETS)
```

## 📞 Siguiente Paso

Si después de seguir todos estos pasos el bot aún no detecta trades:

1. **Copia los logs completos** de una ejecución con `LOG_LEVEL=DEBUG`
2. **Verifica** que el trader realmente hizo un trade recientemente en Polymarket
3. **Prueba** con tu propia dirección haciendo un trade pequeño

## 💡 Tips Profesionales

### 1. Usar un Trader Conocido para Testing

En lugar de usar un trader aleatorio, prueba con uno del leaderboard:

```env
# Top trader conocido de Polymarket
TARGET_TRADER_ADDRESS=0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1
```

### 2. Auto-Test

La forma más rápida de confirmar que el bot funciona:

```env
TARGET_TRADER_ADDRESS=0xTU_DIRECCION
YOUR_POLYMARKET_ADDRESS=0xTU_DIRECCION
DRY_RUN=true
LOG_LEVEL=DEBUG
MAX_TRADE_AGE_MINUTES=120
```

Luego haz un trade pequeño en Polymarket y el bot debería detectarlo en 5-10 segundos.

### 3. Revisar bot.log

Todos los logs se guardan en `bot.log`:

```bash
# Ver últimas líneas
tail -n 100 bot.log

# Buscar errores
grep ERROR bot.log

# Buscar trades detectados
grep "Trade detectado" bot.log

# Ver resumen de filtrado
grep "RESUMEN DEL FILTRADO" bot.log -A 6
```

---

**¿Sigue sin funcionar?** Comparte tus logs de DEBUG (sin tus claves privadas) para análisis más profundo.
