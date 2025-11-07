# 🐍 Polymarket Copy Trading Bot - Versión Python

Bot profesional de copy trading para Polymarket en **Python puro**. Más simple y fácil de usar que la versión TypeScript.

## ✨ Por qué Python

✅ **Más Fácil de Instalar** - Solo `pip install` (sin npm, node, webpack, etc.)
✅ **Sin Compilación** - Ejecuta directamente con `python main.py`
✅ **Código Más Simple** - Python es más legible y directo
✅ **Mismas Características** - Todo lo que tiene la versión TypeScript
✅ **Popular para Trading** - Mayoría de traders usan Python

## 🚀 Instalación Ultra Rápida

### 1. Instalar Python (si no lo tienes)

**Windows:**
```bash
# Descarga desde python.org o usa:
winget install Python.Python.3.11
```

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt install python3 python3-pip
```

### 2. Instalar Dependencias

```bash
cd python
pip install -r ../requirements.txt
```

Eso es todo. No necesitas npm, node, compilar, ni nada más.

### 3. Configurar

El archivo `.env` es el mismo que la versión TypeScript:

```bash
# Si no existe, cópialo desde el directorio raíz
cp ../.env.example ../.env
# Edita con tus credenciales
nano ../.env
```

### 4. Ejecutar

```bash
python main.py
```

¡Ya está! No hay paso de compilación.

## ✅ Validar Configuración (RECOMENDADO)

Antes de ejecutar el bot, valida tu configuración:

```bash
python validate_config.py
```

Este script verifica:
- ✓ Que el archivo `.env` existe
- ✓ Que todas las direcciones son válidas
- ✓ Que la clave privada tiene el formato correcto
- ✓ Que los parámetros de trading son correctos
- ✓ Detecta si estás en modo auto-test (misma wallet)

**Salida ejemplo:**
```
✓ Archivo .env encontrado
✓ TARGET_TRADER_ADDRESS: 0x1234...abcd
✓ YOUR_POLYMARKET_ADDRESS: 0x1234...abcd
✓ YOUR_PRIVATE_KEY: 0x12ab...cd (longitud correcta)
✓ COPY_MODE: fixed
  → Stake fijo: $10 por trade
✓ VALIDACIÓN EXITOSA
```

## 🧪 Probar el Bot (Auto-Test)

¿Quieres probar el bot antes de copiar a otros traders?

**Lee la guía completa:** [GUIA_TEST.md](GUIA_TEST.md)

Resumen rápido:
1. En `.env`, usa TU dirección en ambos campos:
   ```env
   TARGET_TRADER_ADDRESS=0xTU_DIRECCION
   YOUR_POLYMARKET_ADDRESS=0xTU_DIRECCION
   DRY_RUN=true
   LOG_LEVEL=DEBUG
   ```
2. Ejecuta: `python main.py`
3. Haz un trade en Polymarket
4. El bot debería detectarlo en 5-10 segundos

**Ver guía completa con screenshots y troubleshooting:** [GUIA_TEST.md](GUIA_TEST.md)

## 📦 Dependencias

```
py-clob-client  - Cliente oficial de Polymarket
python-dotenv   - Carga variables de .env
requests        - HTTP requests
colorama        - Colores en terminal
web3            - Interacción con blockchain
```

## 🎯 Uso

### Modo Desarrollo (Recomendado para empezar)

```bash
# Con DRY_RUN=true en .env
python main.py
```

### Modo Producción (Trading Real)

```bash
# Con DRY_RUN=false en .env
python main.py
```

### Detener el Bot

```
Ctrl+C
```

## ⚙️ Configuración

Usa el mismo archivo `.env` que la versión TypeScript. Todas las variables funcionan igual:

```env
# Modo de copiado
COPY_MODE=percentage        # o "fixed"
COPY_SIZE_MULTIPLIER=0.5    # Si percentage
FIXED_STAKE_SIZE=10         # Si fixed

# Gestión de riesgo
MIN_ORDER_SIZE=1
MAX_ORDER_SIZE=100
MAX_SLIPPAGE=0.02

# Modo simulación
DRY_RUN=true
```

## 🔍 Estructura del Código Python

```
python/
├── main.py                  # Punto de entrada
├── config.py                # Carga configuración desde .env
├── logger.py                # Sistema de logging con colores
├── polymarket_client.py     # Cliente API de Polymarket
└── copy_trading_bot.py      # Lógica principal del bot
```

Todo el código es Python puro, sin frameworks complejos.

## 📊 Comparación: TypeScript vs Python

| Característica | TypeScript | Python |
|----------------|------------|--------|
| **Instalación** | `npm install` | `pip install` |
| **Compilación** | `npm run build` | ❌ No necesita |
| **Ejecutar** | `npm start` | `python main.py` |
| **Velocidad setup** | ~2 minutos | ~30 segundos |
| **Tamaño node_modules** | ~200MB | ~50MB |
| **Facilidad** | Media | Alta |
| **Características** | Todas ✅ | Todas ✅ |

## 💡 Ventajas de Python

### 1. Instalación Simplificada

**TypeScript:**
```bash
npm install          # Descarga 200MB+
npm run build        # Compila TypeScript a JavaScript
npm start           # Ejecuta
```

**Python:**
```bash
pip install -r requirements.txt   # Descarga ~50MB
python main.py                    # Ejecuta directamente
```

### 2. No Necesitas Saber Node.js

Si no tienes experiencia con `npm`, `package.json`, `tsconfig.json`, etc., Python es mucho más directo.

### 3. Modificar y Ejecutar

**TypeScript:** Editar código → `npm run build` → `npm start`
**Python:** Editar código → `python main.py`

### 4. Debugging Más Fácil

```bash
# Python tiene pdb integrado
python -m pdb main.py

# O simplemente agrega:
import pdb; pdb.set_trace()
```

## 🛠️ Scripts Útiles

### Analizar un Trader

```bash
# Crear script similar al de TypeScript
python -c "
from polymarket_client import PolymarketClient
from config import load_config

config = load_config()
client = PolymarketClient(config)
client.initialize()

trades = client.get_trader_trades('0x...', 100)
print(f'Total trades: {len(trades)}')
"
```

## 🐛 Solución de Problemas

**📘 Guía Completa:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Errores Comunes (Ya Corregidos ✅)

- ✅ **Error UnicodeEncodeError en Windows** - Arreglado (símbolos ASCII)
- ✅ **Error 401 Unauthorized** - Arreglado (cliente autenticado)
- ✅ **Error Timestamp KeyError** - Arreglado (manejo robusto)
- ✅ **Auto-test con propia wallet** - Funcionando

### Error: `ModuleNotFoundError: No module named 'py_clob_client'`

```bash
pip install py-clob-client
```

### Error: `No module named 'dotenv'`

```bash
pip install python-dotenv
```

### El bot no detecta el archivo .env

Asegúrate de que `.env` esté en el directorio raíz (un nivel arriba de `python/`):

```bash
# Desde el directorio python/
ls ../.env    # Debe existir
```

### El bot no detecta trades

1. Ejecuta el validador: `python validate_config.py`
2. Verifica que usas la dirección correcta (de tu perfil Polymarket, no de blockchain)
3. Activa DEBUG: `LOG_LEVEL=DEBUG` en `.env`
4. Lee la guía: [GUIA_TEST.md](GUIA_TEST.md)

### Más Ayuda

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Guía completa de errores
- [GUIA_TEST.md](GUIA_TEST.md) - Guía de testing paso a paso
- `bot.log` - Revisa los logs del bot

## 🎓 Ejemplos de Uso

### Ejecutar en Modo Porcentaje

```bash
# En .env:
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.5

python main.py
```

### Ejecutar en Modo Stake Fijo

```bash
# En .env:
COPY_MODE=fixed
FIXED_STAKE_SIZE=10

python main.py
```

### Ejecutar con Logs de Debug

```bash
# En .env:
LOG_LEVEL=DEBUG

python main.py
```

## 📝 Logs

Los logs se guardan en:
- **Terminal**: Salida con colores
- **bot.log**: Archivo de log completo

```bash
# Ver logs en tiempo real
tail -f bot.log

# Buscar errores
grep ERROR bot.log
```

## 🔒 Seguridad

Las mismas precauciones que la versión TypeScript:

1. Nunca compartas tu `.env`
2. Usa una wallet dedicada
3. Empieza con `DRY_RUN=true`
4. Comienza con cantidades pequeñas

## 🚀 Ejecutar 24/7

### Opción 1: Screen (Linux/Mac)

```bash
screen -S polybot
python main.py
# Ctrl+A, D para detach
# screen -r polybot para volver
```

### Opción 2: nohup

```bash
nohup python main.py > output.log 2>&1 &
```

### Opción 3: systemd (Linux)

Crear `/etc/systemd/system/polybot.service`:

```ini
[Unit]
Description=Polymarket Copy Trading Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/POLY-COPY-BOT/python
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable polybot
sudo systemctl start polybot
```

## 🆚 ¿Python o TypeScript?

### Usa Python si:
- ✅ No tienes experiencia con Node.js/npm
- ✅ Prefieres código más simple y directo
- ✅ Quieres setup más rápido
- ✅ Prefieres no compilar

### Usa TypeScript si:
- ✅ Ya tienes Node.js instalado
- ✅ Prefieres tipado fuerte
- ✅ Tu stack es JavaScript/TypeScript
- ✅ Quieres usar herramientas de npm

**Ambas versiones tienen las mismas características y funcionan igual de bien.**

## 📚 Recursos

### Documentación del Bot
- [GUIA_TEST.md](GUIA_TEST.md) - Cómo probar el bot con tu propia wallet
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas comunes
- [MODOS_COPIADO.md](../MODOS_COPIADO.md) - Guía de modos (Porcentaje vs Fijo)
- `validate_config.py` - Script para validar tu configuración

### Documentación Externa
- [py-clob-client](https://github.com/Polymarket/py-clob-client) - Cliente oficial de Python
- [Polymarket API](https://docs.polymarket.com/) - Documentación de la API
- [Polymarket Leaderboard](https://polymarket.com/leaderboard) - Encuentra traders para copiar

## 🤝 Contribuir

El código Python está en la carpeta `python/`. Los pull requests son bienvenidos.

## ❓ Preguntas Frecuentes

**P: ¿Es más lento Python que TypeScript?**
R: Para este bot, no notarás diferencia. El cuello de botella es la red, no el lenguaje.

**P: ¿Puedo ejecutar ambas versiones al mismo tiempo?**
R: No recomendado. Copiarías el mismo trade dos veces.

**P: ¿Comparten la misma configuración?**
R: Sí, ambas usan el mismo archivo `.env`.

**P: ¿Cuál es mejor?**
R: Depende de tu experiencia. Si no conoces Node.js, usa Python.

---

**¡Happy Trading con Python! 🐍📈**
