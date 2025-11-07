# 🎯 Copiar Múltiples Wallets Simultáneamente

Esta guía explica cómo configurar el bot para copiar varios traders profesionales al mismo tiempo.

## ✨ Ventajas de Multi-Wallet

- ✅ **Diversificación**: No dependes de un solo trader
- ✅ **Más oportunidades**: Detectas trades de varios profesionales
- ✅ **Menos riesgo**: Si un trader tiene un mal día, los otros pueden compensar
- ✅ **Eficiencia**: Un solo bot monitorea múltiples fuentes

## 📋 Configuración Básica

### Editar el archivo `.env`

```bash
# Windows
notepad ..\.env

# Linux/Mac
nano ../.env
```

### Configurar múltiples direcciones

Simplemente separa las direcciones con comas:

```env
# Copiar 3 traders diferentes
TARGET_TRADER_ADDRESS=0x123abc...,0x456def...,0x789ghi...

# Tu dirección (una sola)
YOUR_POLYMARKET_ADDRESS=0xTU_DIRECCION
YOUR_PRIVATE_KEY=0xTU_CLAVE
```

## 🎓 Ejemplos Prácticos

### Ejemplo 1: Copiar 2 traders profesionales

```env
# Trader 1: Especialista en política
# Trader 2: Especialista en deportes
TARGET_TRADER_ADDRESS=0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1,0x8b3b3b624c3c0397d3da8fd861512393d51dcbac

YOUR_POLYMARKET_ADDRESS=0xTU_DIRECCION_AQUI
YOUR_PRIVATE_KEY=0xTU_CLAVE_AQUI

# Usar stake fijo para ambos
COPY_MODE=fixed
FIXED_STAKE_SIZE=10

# Esto copiará $10 de cada trade que hagan CUALQUIERA de los dos traders
```

### Ejemplo 2: Copiar 5 traders con modo porcentaje

```env
TARGET_TRADER_ADDRESS=0xabc...,0xdef...,0xghi...,0xjkl...,0xmno...

COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.2

# Esto copiará el 20% del tamaño de cada trade de los 5 traders
```

### Ejemplo 3: Auto-test + Traders reales

```env
# Incluye tu propia wallet para testing junto con traders reales
TARGET_TRADER_ADDRESS=0xTU_DIRECCION,0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1

# Así puedes testear haciendo un trade tú mismo
# Y al mismo tiempo monitorear al trader profesional
```

## 🚀 Ejecutar el Bot

Una vez configurado, ejecuta normalmente:

```bash
python main.py
```

### Salida Esperada con Múltiples Traders

```
============================================================
  POLYMARKET COPY TRADING BOT
============================================================

Configuración:
  Traders objetivo: 3 traders
    1. 0x44c1dfe4...fb113ebc1
    2. 0x8b3b3b62...d51dcbac
    3. 0xa5f8c721...e89b42af
  Tu dirección: 0x1234abcd...
  Modo de copiado: STAKE FIJO ($10 por trade)

[OK] Bot iniciado - Monitoreando trades...
```

## 📊 Logs con Múltiples Traders

Cuando detecta un trade, el bot muestra de qué trader viene:

```
DEBUG: Consultando trades de 0x44c1dfe4...
DEBUG:   → Obtenidos 5 trades
DEBUG: Consultando trades de 0x8b3b3b62...
DEBUG:   → Obtenidos 3 trades
DEBUG: Total de trades obtenidos: 8

📥 Detectados 2 nuevos trades

[TRADE] Trade detectado [0x44c1df...]: BUY 100.0 @ $0.52
[!] [DRY RUN] Simulando: BUY 19.23 @ $0.52
[OK] Orden ejecutada exitosamente!

[TRADE] Trade detectado [0x8b3b3b...]: SELL 50.0 @ $0.65
[!] [DRY RUN] Simulando: SELL 15.38 @ $0.65
[OK] Orden ejecutada exitosamente!
```

El código entre corchetes `[0x44c1df...]` indica de qué trader viene cada trade.

## 🎯 Estrategias Recomendadas

### 1. Diversificación por Categoría

Elige traders especializados en diferentes áreas:

```env
# Trader 1: Política USA
# Trader 2: Deportes
# Trader 3: Crypto
# Trader 4: Economía
TARGET_TRADER_ADDRESS=0xabc...,0xdef...,0xghi...,0xjkl...
```

### 2. Top Performers del Leaderboard

Ve a https://polymarket.com/leaderboard y copia los top 5:

```env
TARGET_TRADER_ADDRESS=0xtop1...,0xtop2...,0xtop3...,0xtop4...,0xtop5...

# Usa stake fijo para limitar riesgo
COPY_MODE=fixed
FIXED_STAKE_SIZE=5
MAX_ORDER_SIZE=50
```

### 3. Modo Conservador

Pocos traders, stake bajo:

```env
TARGET_TRADER_ADDRESS=0xabc...,0xdef...

COPY_MODE=fixed
FIXED_STAKE_SIZE=5
MIN_ORDER_SIZE=5
MAX_ORDER_SIZE=25
```

### 4. Modo Agresivo

Muchos traders, stake más alto:

```env
TARGET_TRADER_ADDRESS=0xa...,0xb...,0xc...,0xd...,0xe...,0xf...,0xg...

COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.5
MAX_ORDER_SIZE=200
```

## ⚙️ Filtros con Multi-Wallet

Todos los filtros se aplican a TODOS los traders:

```env
# Copiar solo BUY de todos los traders
COPY_SIDES=BUY

# Ignorar ciertos mercados para todos
BLACKLIST_MARKETS=0xmarket1...,0xmarket2...

# Solo copiar estos mercados específicos
WHITELIST_MARKETS=0xmarket1...,0xmarket2...
```

## ⚠️ Consideraciones Importantes

### 1. Volumen de Trades

Con múltiples traders, recibirás más trades. Asegúrate de:
- Tener suficiente balance en tu wallet
- Ajustar `MAX_ORDER_SIZE` apropiadamente
- Monitorear activamente al principio

### 2. Deduplicación Automática

El bot automáticamente evita copiar el mismo trade dos veces:
- Usa el ID único del trade
- Si dos traders hacen el mismo trade, solo se copia una vez

### 3. Performance

El bot consulta cada trader secuencialmente:
- Con 5 traders: ~5 segundos por ciclo
- Con 10 traders: ~10 segundos por ciclo

**Recomendación:** No uses más de 10 traders simultáneos.

### 4. Rate Limits

Polymarket puede tener límites de peticiones:
- El bot incluye delays automáticos
- Si ves errores 429, reduce el número de traders
- O aumenta `POLL_INTERVAL`

## 🔍 Validar Configuración

Antes de ejecutar, valida tu configuración multi-wallet:

```bash
python validate_config.py
```

Salida esperada:

```
✓ Archivo .env encontrado

Modo: 3 traders (multi-wallet)

  Trader #1:
✓ TARGET_TRADER_ADDRESS[1]: 0x44c1dfe4...fb113ebc1
  Trader #2:
✓ TARGET_TRADER_ADDRESS[2]: 0x8b3b3b62...d51dcbac
  Trader #3:
✓ TARGET_TRADER_ADDRESS[3]: 0xa5f8c721...e89b42af

✓ YOUR_POLYMARKET_ADDRESS: 0x1234...
✓ VALIDACIÓN EXITOSA
```

## 📈 Estadísticas con Multi-Wallet

Al finalizar, las estadísticas muestran el total de todos los traders:

```
============================================================
  ESTADÍSTICAS DEL BOT
============================================================
Tiempo de ejecución: 120.5 minutos
Trades detectados: 47 (de 3 traders)
Trades copiados: 42
Trades fallidos: 5
Volumen copiado: $420.50
Tasa de éxito: 89.4%
============================================================
```

## 🐛 Troubleshooting Multi-Wallet

### No detecta trades de algunos traders

**Solución:**
1. Verifica que las direcciones sean correctas
2. Aumenta `MAX_TRADE_AGE_MINUTES`
3. Activa DEBUG: `LOG_LEVEL=DEBUG`

```bash
python main.py
```

Deberías ver:

```
DEBUG: Consultando trades de 0x44c1dfe4...
DEBUG:   → Obtenidos 5 trades
DEBUG: Consultando trades de 0x8b3b3b62...
DEBUG:   → Obtenidos 0 trades  ← Este trader no ha operado
```

### Demasiados trades

Si recibes más trades de los que puedes manejar:

```env
# Opción 1: Reducir el número de traders
TARGET_TRADER_ADDRESS=0xabc...,0xdef...  # Solo 2 en lugar de 5

# Opción 2: Aumentar el mínimo
MIN_ORDER_SIZE=10

# Opción 3: Filtrar por lado
COPY_SIDES=BUY  # Solo compras

# Opción 4: Usar whitelist
WHITELIST_MARKETS=0xmarket1...  # Solo mercados específicos
```

### Errores de rate limit (429)

```env
# Aumentar intervalo entre consultas
POLL_INTERVAL=10000  # 10 segundos en lugar de 5

# O reducir el número de traders
TARGET_TRADER_ADDRESS=0xabc...,0xdef...,0xghi...  # Solo 3
```

## 💡 Tips Profesionales

### 1. Empezar Pequeño

```env
# Primer día: 2 traders, stake bajo
TARGET_TRADER_ADDRESS=0xabc...,0xdef...
FIXED_STAKE_SIZE=5
DRY_RUN=true  # Simulación
```

### 2. Escalar Gradualmente

```env
# Después de 1 semana: 4 traders, stake medio
TARGET_TRADER_ADDRESS=0xabc...,0xdef...,0xghi...,0xjkl...
FIXED_STAKE_SIZE=10
DRY_RUN=false  # Live
```

### 3. Monitorear Regularmente

```bash
# Ver logs en tiempo real
tail -f bot.log

# Buscar trades copiados
grep "Orden ejecutada" bot.log

# Ver de qué trader vienen
grep "Trade detectado" bot.log
```

### 4. Ajustar según Resultados

Después de una semana, analiza:
- ¿Qué trader tiene mejor tasa de éxito?
- ¿Alguno hace demasiados trades?
- ¿Los tamaños son apropiados?

Ajusta tu configuración basándote en los resultados.

## 📚 Recursos Adicionales

- [GUIA_TEST.md](GUIA_TEST.md) - Cómo probar el bot
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas
- [MODOS_COPIADO.md](../MODOS_COPIADO.md) - Porcentaje vs Fijo
- [README_PYTHON.md](README_PYTHON.md) - Documentación completa

## 🎉 Ejemplo Real de Uso

Usuario copiando 3 traders del leaderboard:

```env
# Top 3 traders de Polymarket (ejemplo)
TARGET_TRADER_ADDRESS=0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1,0x8b3b3b624c3c0397d3da8fd861512393d51dcbac,0xa5f8c721234567890abcdef1234567890e89b42af

YOUR_POLYMARKET_ADDRESS=0x9876543210abcdef9876543210abcdef98765432
YOUR_PRIVATE_KEY=0x1234567890abcdef...

# Configuración conservadora
COPY_MODE=fixed
FIXED_STAKE_SIZE=10
MIN_ORDER_SIZE=5
MAX_ORDER_SIZE=50
MAX_SLIPPAGE=0.02

# Monitoreo
POLL_INTERVAL=5000
MAX_TRADE_AGE_MINUTES=10

# Seguridad
DRY_RUN=false
LOG_LEVEL=INFO

# Sin filtros (copiar todo)
COPY_SIDES=BUY,SELL
```

**Resultado esperado:** El bot copia trades de los 3 profesionales, invirtiendo $10 fijo por cada trade, con un máximo de $50 por orden.

---

**¿Listo para diversificar?** Configura múltiples wallets y maximiza tus oportunidades! 📈
