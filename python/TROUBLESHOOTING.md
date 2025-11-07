# 🔧 Solución de Problemas - Bot Python

Guía para resolver los errores más comunes al ejecutar el bot.

## ❌ Error: UnicodeEncodeError (Windows)

### Problema
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2717'
```

### Causa
Windows cmd.exe no puede mostrar caracteres Unicode como ✗, ✓, 💱

### Solución
✅ **YA ESTÁ ARREGLADO** en la última versión del código.

El bot ahora detecta automáticamente Windows y usa caracteres ASCII:
- `✓` → `[OK]`
- `✗` → `[X]`
- `⚠` → `[!]`
- `💱` → `[TRADE]`
- `📊` → `[STATS]`

Si aún ves el error, actualiza el código:
```bash
git pull
```

---

## 🔒 Error 401: Unauthorized

### Problema
```
401 Client Error: Unauthorized for url: https://clob.polymarket.com/data/trades
```

### Causas Posibles

#### 1. Restricción Geográfica
Polymarket bloquea ciertos países.

**Solución:**
```bash
# Usa una VPN conectada a USA
# Servicios recomendados: NordVPN, ExpressVPN, ProtonVPN
```

#### 2. API Key Incorrecta
Tu clave privada puede ser incorrecta.

**Solución:**
```bash
# Verifica en .env:
YOUR_PRIVATE_KEY=0x...  # Debe empezar con 0x
YOUR_POLYMARKET_ADDRESS=0x...  # Tu dirección real
```

#### 3. Cambios en la API
La API de Polymarket puede haber cambiado.

**Solución:**
```bash
# Actualizar el cliente
pip install --upgrade py-clob-client
```

### Test Rápido

Verifica si puedes acceder a la API:

```python
import requests

url = "https://clob.polymarket.com/data/trades"
params = {"maker_address": "0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1", "limit": 1}
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, params=params, headers=headers)
print(f"Status: {response.status_code}")
print(response.text[:200])
```

Si esto falla con 401, el problema es acceso/geolocalización.

---

## 🌍 Error 403: Forbidden

### Problema
```
403 Client Error: Forbidden
```

### Causa
Restricción geográfica estricta.

### Solución
1. **Usa VPN** conectada a USA
2. **Verifica** que la VPN esté activa
3. **Prueba** diferentes servidores VPN
4. **Considera** usar un VPS en USA

---

## ⏱️ Error: Timeout

### Problema
```
Timeout al conectar con Polymarket
```

### Soluciones

#### 1. Verifica tu Conexión
```bash
ping google.com
```

#### 2. Aumenta el Timeout
En `polymarket_client.py`, línea 50:
```python
response = requests.get(url, params=params, headers=self.headers, timeout=30)  # Era 10
```

#### 3. Usa VPN
La conexión puede estar bloqueada.

---

## 🔌 Error: ConnectionError

### Problema
```
Error de conexión - verifica tu internet o usa VPN
```

### Soluciones

1. **Verifica Internet:**
   ```bash
   ping 8.8.8.8
   ```

2. **Verifica Firewall:**
   - Permite Python en el firewall
   - Permite conexiones a clob.polymarket.com

3. **Usa VPN:**
   - Conecta a servidor en país permitido

---

## 📦 Error: ModuleNotFoundError

### Problema
```
ModuleNotFoundError: No module named 'py_clob_client'
```

### Solución
```bash
pip install -r ../requirements.txt
```

O instalar manualmente:
```bash
pip install py-clob-client python-dotenv requests colorama web3
```

---

## 🔑 Error: Faltan Variables de Entorno

### Problema
```
Faltan variables de entorno requeridas: TARGET_TRADER_ADDRESS
```

### Solución

1. **Verifica que `.env` existe:**
   ```bash
   ls ../.env
   ```

2. **Si no existe, créalo:**
   ```bash
   cp ../.env.example ../.env
   ```

3. **Edita con tus datos:**
   ```bash
   notepad ../.env   # Windows
   nano ../.env      # Linux/Mac
   ```

4. **Variables mínimas requeridas:**
   ```env
   TARGET_TRADER_ADDRESS=0x...
   YOUR_POLYMARKET_ADDRESS=0x...
   YOUR_PRIVATE_KEY=0x...
   ```

---

## 🚫 No Detecta Trades

### Problema
El bot arranca pero no detecta ningún trade.

### Causas y Soluciones

#### 1. Trader No Ha Operado Recientemente
```env
# Aumenta el tiempo de antigüedad en .env:
MAX_TRADE_AGE_MINUTES=60  # En lugar de 5
```

#### 2. Dirección del Trader Incorrecta
Verifica la dirección en Polymarket:
- Ve a https://polymarket.com/leaderboard
- Copia la dirección exacta del trader

#### 3. Filtros Muy Restrictivos
```env
# Revisa estos filtros en .env:
COPY_SIDES=BUY,SELL  # Ambos lados
# BLACKLIST_MARKETS=  # Comentado
# WHITELIST_MARKETS=  # Comentado
```

---

## 🐛 Debug Mode

Para ver más información de errores:

```env
# En .env:
LOG_LEVEL=DEBUG
```

Luego ejecuta:
```bash
python main.py
```

Verás logs detallados como:
```
DEBUG: Obteniendo trades de 0x44c1dfe4...
DEBUG: Se obtuvieron 15 trades
DEBUG: Modo porcentaje: 100 × 0.5 = 50.0 tokens
```

---

## 📝 Archivo de Log

El bot guarda un log completo en `bot.log`:

```bash
# Ver últimas líneas:
tail -n 50 bot.log

# Buscar errores:
grep ERROR bot.log

# Ver en tiempo real:
tail -f bot.log
```

---

## 🔄 Reinstalación Completa

Si nada funciona, reinstala desde cero:

### Windows
```bash
cd python
rmdir /s /q __pycache__
pip uninstall -y py-clob-client python-dotenv requests colorama web3
pip install -r ../requirements.txt
python main.py
```

### Linux/Mac
```bash
cd python
rm -rf __pycache__
pip3 uninstall -y py-clob-client python-dotenv requests colorama web3
pip3 install -r ../requirements.txt
python3 main.py
```

---

## 💬 Aún Necesitas Ayuda?

1. **Revisa el log completo:**
   ```bash
   cat bot.log
   ```

2. **Verifica la configuración:**
   ```bash
   cat ../.env
   ```

3. **Prueba con DRY_RUN:**
   ```env
   DRY_RUN=true
   ```

4. **Abre un Issue:**
   - Incluye el error completo
   - Incluye tu OS (Windows/Mac/Linux)
   - Incluye versión de Python: `python --version`

---

## ✅ Checklist de Verificación

Antes de abrir un issue, verifica:

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Dependencias instaladas (`pip list | grep py-clob-client`)
- [ ] Archivo `.env` existe y está configurado
- [ ] Variables requeridas están en `.env`
- [ ] VPN activa (si estás en país restringido)
- [ ] Internet funciona (`ping google.com`)
- [ ] Has intentado con `DRY_RUN=true`
- [ ] Has revisado `bot.log`

---

## 📚 Recursos Adicionales

- [README Python](README_PYTHON.md) - Documentación completa
- [Guía de Modos](../MODOS_COPIADO.md) - Porcentaje vs Fijo
- [Polymarket Docs](https://docs.polymarket.com/) - Documentación oficial
- [py-clob-client](https://github.com/Polymarket/py-clob-client) - Cliente oficial

---

**¿Solucionaste tu problema?** ¡Genial! Ahora puedes ejecutar:

```bash
python main.py
```

Y empezar a copiar trades. Recuerda usar `DRY_RUN=true` al principio para probar sin riesgo.
