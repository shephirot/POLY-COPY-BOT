# 🤖 Polymarket Copy Trading Bot

Bot profesional de copy trading para Polymarket que replica automáticamente las operaciones de traders exitosos en tiempo real.

## ✨ Características

- 🔄 **Copy Trading en Tiempo Real**: Monitorea y replica trades automáticamente
- 🎯 **Dos Modos de Copiado**:
  - **Porcentaje**: Copia un % del tamaño del trader (ej: 50%)
  - **Stake Fijo**: Copia siempre con el mismo monto (ej: $10 por trade)
- 🛡️ **Gestión de Riesgo**: Límites configurables de tamaño, slippage y filtros de mercado
- 🎲 **Filtros Avanzados**: Whitelist/Blacklist de mercados, filtros por tipo de operación
- 🔁 **Sistema de Reintentos**: Manejo robusto de errores con reintentos automáticos
- 📊 **Estadísticas en Tiempo Real**: Tracking completo de performance del bot
- 🧪 **Modo Dry Run**: Prueba el bot sin riesgo antes de operar con dinero real
- 📝 **Logging Profesional**: Sistema de logs completo con niveles configurables

## 🚀 Instalación Rápida

### Prerrequisitos

- Node.js v18 o superior
- npm o yarn
- Una wallet de Ethereum/Polygon con USDC
- Acceso a Polymarket (considera usar VPN si hay restricciones geográficas)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**

```bash
git clone <repo-url>
cd POLY-COPY-BOT
```

2. **Instalar dependencias**

```bash
npm install
```

3. **Configurar variables de entorno**

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura las siguientes variables:

```env
# REQUERIDO: Trader que quieres copiar
TARGET_TRADER_ADDRESS=0x1234...

# REQUERIDO: Tu dirección de Polymarket
YOUR_POLYMARKET_ADDRESS=0x5678...

# REQUERIDO: Tu clave privada (¡NUNCA LA COMPARTAS!)
YOUR_PRIVATE_KEY=0xabcd...

# RECOMENDADO: Elige tu modo de copiado
COPY_MODE=percentage       # "percentage" o "fixed"
COPY_SIZE_MULTIPLIER=0.5   # Si usas percentage: 50% del tamaño
FIXED_STAKE_SIZE=10        # Si usas fixed: $10 por trade
MAX_ORDER_SIZE=100         # Máximo $100 por orden
DRY_RUN=true               # Empieza en modo simulación
```

4. **Compilar el proyecto**

```bash
npm run build
```

5. **Iniciar el bot**

```bash
# Modo producción
npm start

# O modo desarrollo (con recarga automática)
npm run dev
```

## ⚙️ Configuración

### Variables de Entorno Principales

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `TARGET_TRADER_ADDRESS` | Dirección del trader a copiar | **REQUERIDO** |
| `YOUR_POLYMARKET_ADDRESS` | Tu dirección de Polymarket | **REQUERIDO** |
| `YOUR_PRIVATE_KEY` | Tu clave privada | **REQUERIDO** |
| `COPY_MODE` | Modo de copiado: `percentage` o `fixed` | percentage |
| `COPY_SIZE_MULTIPLIER` | Multiplicador (modo percentage) | 1.0 |
| `FIXED_STAKE_SIZE` | Stake fijo en USDC (modo fixed) | 10 |
| `MIN_ORDER_SIZE` | Tamaño mínimo de orden (USDC) | 1 |
| `MAX_ORDER_SIZE` | Tamaño máximo de orden (USDC) | 1000 |
| `MAX_SLIPPAGE` | Slippage máximo permitido | 0.02 (2%) |
| `POLL_INTERVAL` | Intervalo de polling (ms) | 5000 |
| `DRY_RUN` | Modo simulación | true |

### 🎯 Modos de Copiado

El bot soporta dos estrategias diferentes:

**Modo Porcentaje** (`COPY_MODE=percentage`):
- Copia un % del tamaño del trader
- Ejemplo: `COPY_SIZE_MULTIPLIER=0.5` = copia el 50%
- Ideal cuando el trader tiene capital similar al tuyo

**Modo Stake Fijo** (`COPY_MODE=fixed`):
- Copia siempre con el mismo monto
- Ejemplo: `FIXED_STAKE_SIZE=10` = siempre $10 por trade
- Ideal para control de riesgo consistente

📖 **[Ver guía completa de modos →](MODOS_COPIADO.md)**

### Filtros Avanzados

```env
# Copiar solo operaciones BUY
COPY_SIDES=BUY

# Copiar solo BUY y SELL (ambas)
COPY_SIDES=BUY,SELL

# Ignorar mercados específicos
BLACKLIST_MARKETS=market_id_1,market_id_2

# Copiar solo mercados específicos
WHITELIST_MARKETS=market_id_3,market_id_4
```

## 🎓 Guía de Uso

### 1. Encuentra un Trader para Copiar

Visita [Polymarket Leaderboard](https://polymarket.com/leaderboard) y busca traders con buen historial. Copia su dirección de wallet.

### 2. Prueba en Modo Dry Run

Antes de arriesgar dinero real, prueba el bot:

```env
DRY_RUN=true
```

Esto te permitirá ver qué operaciones se copiarían sin ejecutarlas realmente.

### 3. Configura tu Gestión de Riesgo

Elige tu modo de copiado:

**Opción A - Modo Porcentaje:**
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.3  # Copia solo 30% del tamaño
MAX_ORDER_SIZE=50          # No más de $50 por operación
```

**Opción B - Modo Stake Fijo:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=15        # Siempre $15 por trade
MAX_ORDER_SIZE=20          # Protección adicional
```

### 4. Activa el Modo Live

Cuando estés listo:

```env
DRY_RUN=false
```

⚠️ **IMPORTANTE**: Asegúrate de tener suficiente USDC en tu wallet de Polymarket.

### 5. Monitorea el Bot

El bot mostrará estadísticas en tiempo real:

```
📊 Trades detectados: 15
📊 Trades copiados: 12
📊 Trades fallidos: 3
📊 Volumen copiado: $156.50
📊 Tasa de éxito: 80.0%
```

## 📊 Ejemplo de Output

```
============================================================
  POLYMARKET COPY TRADING BOT
============================================================

✓ Configuración cargada correctamente
✓ Cliente de Polymarket inicializado correctamente

Configuración:
  Trader objetivo: 0x1234abcd...
  Tu dirección: 0x5678efgh...
  Multiplicador de tamaño: 0.5x
  Tamaño min/max: $1 - $100
  Slippage máximo: 2.0%
  Intervalo de polling: 5000ms
  Modo: DRY RUN (Simulación)

============================================================

⚠️  MODO DRY RUN ACTIVADO - No se ejecutarán trades reales

🚀 Bot iniciado - Monitoreando trades...

📥 Detectados 1 nuevos trades
💱 Trade detectado: BUY 10 @ $0.65
  ↳ [DRY RUN] Simulando: BUY 5.00 @ $0.65
  ✓ Orden ejecutada exitosamente! ID: DRY-RUN-1699123456789
```

## 🔒 Seguridad

### ⚠️ Prácticas Recomendadas

1. **Nunca compartas tu clave privada**: El archivo `.env` debe estar en `.gitignore`
2. **Usa una wallet dedicada**: No uses tu wallet principal
3. **Empieza con poco capital**: Prueba con cantidades pequeñas
4. **Usa límites de riesgo**: Configura `MAX_ORDER_SIZE` conservadoramente
5. **Monitorea regularmente**: No dejes el bot sin supervisión por mucho tiempo
6. **Considera un VPS**: Para mejor uptime y menor latencia

### 🌍 Restricciones Geográficas

Polymarket tiene restricciones en ciertos países. Si tienes problemas de conexión:

- Usa un VPS en una región permitida
- Considera servicios como [TradingVPS](https://tradingvps.io) con servidores optimizados para trading

## 🐛 Solución de Problemas

### Error: "Faltan variables de entorno requeridas"

Asegúrate de haber configurado correctamente el archivo `.env` con todas las variables requeridas.

### Error: "Error al inicializar cliente de Polymarket"

- Verifica que tu clave privada sea válida
- Verifica que tu dirección de Polymarket sea correcta
- Verifica tu conexión a Internet
- Considera usar VPN si hay restricciones geográficas

### No se detectan trades

- Verifica que la dirección del trader sea correcta
- Verifica que el trader haya realizado trades recientemente
- Ajusta `MAX_TRADE_AGE_MINUTES` si es necesario

### Ordenes fallan constantemente

- Verifica que tengas suficiente USDC en tu wallet
- Ajusta `MAX_SLIPPAGE` si los mercados son volátiles
- Reduce `COPY_SIZE_MULTIPLIER` si las órdenes son muy grandes

## 📚 Recursos

- [Documentación oficial de Polymarket](https://docs.polymarket.com/)
- [CLOB Client GitHub](https://github.com/Polymarket/clob-client)
- [Polymarket API](https://docs.polymarket.com/developers/CLOB/introduction)

## ⚖️ Disclaimer

Este bot es para fines educativos y experimentales. El trading conlleva riesgos:

- Puedes perder todo tu capital
- No hay garantía de ganancias
- Los resultados pasados no garantizan resultados futuros
- Usa bajo tu propio riesgo

**No soy responsable de ninguna pérdida financiera que puedas sufrir al usar este bot.**

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 💬 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Busca en los Issues existentes
3. Crea un nuevo Issue con detalles completos

---

**¡Happy Trading! 🚀**
