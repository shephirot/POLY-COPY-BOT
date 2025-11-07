# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a poner en marcha el bot en menos de 10 minutos.

## Paso 1: Preparar el Entorno

```bash
# Instalar dependencias
npm install

# Copiar el archivo de configuración
cp .env.example .env
```

## Paso 2: Encontrar un Trader

Tienes dos opciones:

### Opción A: Usar el Leaderboard de Polymarket

1. Ve a https://polymarket.com/leaderboard
2. Encuentra un trader con buen historial
3. Copia su dirección de wallet (ejemplo: `0x1234...abcd`)

### Opción B: Usar Nuestro Script de Análisis

```bash
# Analizar un trader específico
npm run analyze-trader 0x1234567890abcdef1234567890abcdef12345678
```

Este script te mostrará:
- Total de trades del trader
- Volumen operado
- Tamaño promedio de órdenes
- Mercados más operados
- Configuración recomendada

## Paso 3: Configurar el Bot

Edita el archivo `.env`:

```env
# 1. Dirección del trader que quieres copiar
TARGET_TRADER_ADDRESS=0x1234567890abcdef1234567890abcdef12345678

# 2. Tu dirección de Polymarket (donde tienes USDC)
YOUR_POLYMARKET_ADDRESS=0xabcdefabcdefabcdefabcdefabcdefabcdefabcd

# 3. Tu clave privada (LA MÁS IMPORTANTE - ¡NO LA COMPARTAS!)
YOUR_PRIVATE_KEY=0xfedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210

# 4. Configuración de riesgo (IMPORTANTE)
# Elige entre modo porcentaje o stake fijo:

# OPCIÓN A - Modo Porcentaje (copia un % del trader)
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.3    # Copia solo el 30% del tamaño del trader

# OPCIÓN B - Modo Stake Fijo (copia siempre con el mismo monto)
# COPY_MODE=fixed
# FIXED_STAKE_SIZE=10        # Siempre apuestas $10 por trade

# Límites de protección
MIN_ORDER_SIZE=1            # Mínimo $1
MAX_ORDER_SIZE=50           # Máximo $50 (protección de riesgo)
MAX_SLIPPAGE=0.02          # 2% de slippage máximo

# 5. Modo de operación
DRY_RUN=true               # Empieza en modo simulación
LOG_LEVEL=info
```

## Paso 4: Probar en Modo Dry Run

```bash
# Compilar el proyecto
npm run build

# Iniciar en modo simulación
npm start
```

Verás algo como:

```
============================================================
  POLYMARKET COPY TRADING BOT
============================================================

✓ Configuración cargada correctamente
✓ Cliente de Polymarket inicializado correctamente

Configuración:
  Trader objetivo: 0x1234abcd...
  Modo de copiado: PORCENTAJE (0.3x del tamaño del trader)
  Modo: DRY RUN (Simulación)

⚠️  MODO DRY RUN ACTIVADO - No se ejecutarán trades reales

🚀 Bot iniciado - Monitoreando trades...
```

Deja que el bot corra durante 10-30 minutos para ver cómo funcionaría.

## Paso 5: Activar el Modo Real (Cuando Estés Listo)

⚠️ **IMPORTANTE**: Solo haz esto cuando:
- Hayas probado suficientemente en modo dry run
- Tengas USDC en tu wallet de Polymarket
- Estés cómodo con los parámetros de riesgo

Edita `.env`:

```env
DRY_RUN=false
```

Y reinicia el bot:

```bash
npm start
```

## 📊 Monitorear el Bot

El bot muestra información en tiempo real:

```
📥 Detectados 1 nuevos trades
💱 Trade detectado: BUY 10 @ $0.65
  ✓ Orden ejecutada exitosamente! ID: 0xabc123...
```

Para ver estadísticas, presiona `Ctrl+C` para detener el bot:

```
============================================================
  ESTADÍSTICAS DEL BOT
============================================================
📊 Tiempo de ejecución: 45.2 minutos
📊 Trades detectados: 8
📊 Trades copiados: 7
📊 Trades fallidos: 1
📊 Volumen copiado: $156.50
📊 Tasa de éxito: 87.5%
============================================================
```

## ⚠️ Consejos Importantes

### Seguridad

1. **Nunca compartas tu clave privada**: Ni en GitHub, Discord, Telegram, etc.
2. **Usa una wallet dedicada**: No uses tu wallet principal
3. **Empieza con poco**: Prueba con cantidades pequeñas primero

### Configuración de Riesgo

**Modo Porcentaje - Para seguir proporcionalmente al trader:**
```env
COPY_MODE=percentage

# Para traders conservadores
COPY_SIZE_MULTIPLIER=0.2    # Solo 20% del tamaño
MAX_ORDER_SIZE=25           # Máximo $25

# Para traders más agresivos
COPY_SIZE_MULTIPLIER=0.5    # 50% del tamaño
MAX_ORDER_SIZE=100          # Máximo $100

# Para traders experimentados
COPY_SIZE_MULTIPLIER=1.0    # 100% del tamaño
MAX_ORDER_SIZE=500          # Máximo $500
```

**Modo Stake Fijo - Para control total del riesgo:**
```env
COPY_MODE=fixed

# Para traders conservadores
FIXED_STAKE_SIZE=5          # $5 por trade
MAX_ORDER_SIZE=10           # Máximo $10

# Para traders balanceados
FIXED_STAKE_SIZE=15         # $15 por trade
MAX_ORDER_SIZE=20           # Máximo $20

# Para traders agresivos
FIXED_STAKE_SIZE=50         # $50 por trade
MAX_ORDER_SIZE=75           # Máximo $75
```

📖 **[Guía completa de modos →](MODOS_COPIADO.md)** - Aprende cuál modo es mejor para ti

### Filtros Útiles

```env
# Copiar solo operaciones de compra
COPY_SIDES=BUY

# Ignorar mercados específicos
BLACKLIST_MARKETS=market_id_1,market_id_2

# Copiar solo mercados específicos
WHITELIST_MARKETS=market_id_3,market_id_4
```

## 🆘 Problemas Comunes

### "Error al inicializar cliente"

- Verifica que tu `PRIVATE_KEY` sea correcta (debe empezar con 0x)
- Verifica que tu `YOUR_POLYMARKET_ADDRESS` sea correcta
- Intenta usar una VPN si estás en un país con restricciones

### "No se detectan trades"

- Verifica que la dirección del trader sea correcta
- Asegúrate de que el trader esté activo (usa el script de análisis)
- Ajusta `MAX_TRADE_AGE_MINUTES` a un valor mayor (ejemplo: 60)

### "Todas las órdenes fallan"

- Verifica que tengas suficiente USDC en tu wallet
- Reduce `COPY_SIZE_MULTIPLIER`
- Aumenta `MAX_SLIPPAGE` un poco (ejemplo: 0.03 = 3%)

## 🔧 Scripts Útiles

```bash
# Analizar un trader antes de copiarlo
npm run analyze-trader 0x...

# Modo desarrollo (recarga automática)
npm run dev

# Ver logs de errores
cat bot-error.log

# Ver todos los logs
cat bot-combined.log

# Formatear código
npm run format

# Linter
npm run lint
```

## 📚 Próximos Pasos

1. Lee el [README completo](README.md) para entender todas las características
2. Experimenta con diferentes traders
3. Ajusta los parámetros de riesgo según tu estrategia
4. Monitorea regularmente el bot
5. Considera usar un VPS para tener el bot 24/7

## 💬 ¿Necesitas Ayuda?

- Revisa el [README.md](README.md) completo
- Busca en los Issues del repositorio
- Crea un nuevo Issue con tu pregunta

---

**¡Buena suerte con tu copy trading! 📈**

*Recuerda: El trading conlleva riesgos. Nunca inviertas más de lo que puedas permitirte perder.*
