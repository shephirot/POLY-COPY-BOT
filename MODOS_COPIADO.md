# 📝 Guía de Modos de Copiado

El bot ahora soporta dos modos diferentes de copiar las operaciones del trader objetivo. Esta guía te ayudará a entender cuál usar según tu estrategia.

## 🎯 Modos Disponibles

### 1. Modo Porcentaje (`percentage`)

Copia un **porcentaje del tamaño** de las operaciones del trader.

**Cuándo usarlo:**
- ✅ Quieres escalar proporcionalmente con el trader
- ✅ El trader tiene un capital similar al tuyo
- ✅ Quieres seguir exactamente su estrategia
- ✅ Prefieres operaciones más grandes cuando el trader opera más grande

**Configuración:**
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.5  # Copia el 50% del tamaño del trader
```

**Ejemplo:**
- Trader opera: **100 tokens** @ $0.50 = $50
- Tu copias (con 0.5x): **50 tokens** @ $0.50 = **$25**

- Trader opera: **20 tokens** @ $0.30 = $6
- Tu copias (con 0.5x): **10 tokens** @ $0.30 = **$3**

**Valores comunes:**
- `0.1` = 10% del tamaño (para traders con mucho capital)
- `0.5` = 50% del tamaño (recomendado para la mayoría)
- `1.0` = 100% del tamaño (mismo tamaño que el trader)
- `2.0` = 200% del tamaño (el doble que el trader)

---

### 2. Modo Stake Fijo (`fixed`)

Copia **siempre con el mismo monto** en cada operación, sin importar el tamaño del trader.

**Cuándo usarlo:**
- ✅ Quieres riesgo consistente en cada trade
- ✅ El trader tiene mucho más (o menos) capital que tú
- ✅ Prefieres gestión de riesgo simplificada
- ✅ Quieres un tamaño de posición predecible

**Configuración:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=10  # Arriesgas $10 en cada trade
```

**Ejemplo:**
- Trader opera: **100 tokens** @ $0.50 = $50
- Tu copias (con $10 fijo): **20 tokens** @ $0.50 = **$10**

- Trader opera: **20 tokens** @ $0.30 = $6
- Tu copias (con $10 fijo): **33.33 tokens** @ $0.30 = **$10**

**Valores comunes:**
- `5` = $5 por trade (conservador)
- `10` = $10 por trade (balanceado)
- `25` = $25 por trade (moderado)
- `50` = $50 por trade (agresivo)

---

## 🔀 Comparación Directa

| Característica | Modo Porcentaje | Modo Stake Fijo |
|----------------|-----------------|-----------------|
| **Tamaño de operación** | Variable (proporcional al trader) | Constante (siempre igual) |
| **Riesgo por trade** | Variable | Constante |
| **Mejor para** | Seguir estrategia del trader | Gestión de riesgo consistente |
| **Capital similar al trader** | ✅ Ideal | ⚠️ Puede no ser proporcional |
| **Capital diferente al trader** | ⚠️ Puede ser muy grande/pequeño | ✅ Ideal |
| **Simplicidad** | 🟡 Media | 🟢 Simple |
| **Control de riesgo** | 🟡 Depende del trader | 🟢 Total control |

---

## 💡 Ejemplos de Configuración por Escenario

### Escenario 1: Trader Whale (Capital grande)
**Problema:** El trader opera con $500+ por trade, pero tú solo tienes $100.

**Solución:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=10
MAX_ORDER_SIZE=15
```

### Escenario 2: Trader Similar a Ti
**Problema:** El trader opera con tamaños similares a tu capital.

**Solución:**
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.8
MAX_ORDER_SIZE=100
```

### Escenario 3: Trader Pequeño
**Problema:** El trader opera con $5-10 por trade, pero tú quieres operar más.

**Solución:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=25
MIN_ORDER_SIZE=5
```

### Escenario 4: Máximo Control de Riesgo
**Problema:** Quieres arriesgar exactamente $15 por trade, siempre.

**Solución:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=15
MIN_ORDER_SIZE=15
MAX_ORDER_SIZE=15
```

### Escenario 5: Copiar Exactamente
**Problema:** Quieres seguir al trader al 100%, mismo tamaño.

**Solución:**
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=1.0
MAX_ORDER_SIZE=1000
```

---

## 🛡️ Límites de Seguridad

Ambos modos respetan los límites de seguridad:

```env
MIN_ORDER_SIZE=1    # No copiar trades muy pequeños
MAX_ORDER_SIZE=100  # Nunca arriesgar más de $100
```

### Cómo Funcionan los Límites

**En Modo Porcentaje:**
- Si la orden calculada es < MIN: **No se copia**
- Si la orden calculada es > MAX: **Se ajusta al MAX**

**En Modo Stake Fijo:**
- Si el precio hace que tu stake sea < MIN: **No se copia**
- Si tu stake fijo es > MAX: **Se ajusta al MAX**

**Ejemplo con límites:**
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=150
MAX_ORDER_SIZE=100
```

Resultado: Todas las órdenes se ejecutarán con **$100** (ajustado al máximo).

---

## 🎓 Recomendaciones por Experiencia

### Para Principiantes
```env
COPY_MODE=fixed
FIXED_STAKE_SIZE=5
MIN_ORDER_SIZE=2
MAX_ORDER_SIZE=10
DRY_RUN=true  # ¡Empieza en simulación!
```

### Para Traders Intermedios
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=0.5
MIN_ORDER_SIZE=5
MAX_ORDER_SIZE=50
```

### Para Traders Avanzados
```env
COPY_MODE=percentage
COPY_SIZE_MULTIPLIER=1.0
MIN_ORDER_SIZE=10
MAX_ORDER_SIZE=200
# Ajusta según tu análisis del trader
```

---

## 🔄 Cambiar Entre Modos

Puedes cambiar entre modos en cualquier momento:

1. Detén el bot (`Ctrl+C`)
2. Edita tu archivo `.env`
3. Cambia `COPY_MODE` y ajusta los parámetros correspondientes
4. Reinicia el bot

**No necesitas recompilar**, solo reiniciar.

---

## 📊 Visualización de Diferencias

### Trade 1: Precio $0.50, Trader opera 100 tokens ($50)

| Configuración | Tú copias | Tu costo |
|---------------|-----------|----------|
| percentage + 0.3x | 30 tokens | **$15** |
| percentage + 1.0x | 100 tokens | **$50** |
| fixed + $20 | 40 tokens | **$20** |
| fixed + $10 | 20 tokens | **$10** |

### Trade 2: Precio $0.25, Trader opera 200 tokens ($50)

| Configuración | Tú copias | Tu costo |
|---------------|-----------|----------|
| percentage + 0.3x | 60 tokens | **$15** |
| percentage + 1.0x | 200 tokens | **$50** |
| fixed + $20 | 80 tokens | **$20** |
| fixed + $10 | 40 tokens | **$10** |

**Observa:**
- Modo **percentage**: Tu costo varía con el trader ($15 en ambos)
- Modo **fixed**: Tu costo es siempre el mismo ($20 o $10)

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar ambos modos al mismo tiempo?**
R: No, debes elegir uno. Pero puedes cambiar entre ellos cuando quieras.

**P: ¿Qué modo es mejor?**
R: Depende de tu estrategia:
- **Percentage** si quieres seguir proporcionalmente al trader
- **Fixed** si quieres control total sobre tu riesgo

**P: ¿Qué pasa si el trader hace un trade muy grande?**
R: `MAX_ORDER_SIZE` te protege en ambos modos. Nunca copiarás más del máximo configurado.

**P: ¿Puedo tener diferentes configuraciones para diferentes traders?**
R: Sí, crea múltiples archivos `.env` (ejemplo: `.env.trader1`, `.env.trader2`) y carga el apropiado.

**P: ¿El modo afecta la velocidad de ejecución?**
R: No, ambos modos ejecutan a la misma velocidad.

---

## 🚀 Empezar Ahora

1. **Decide tu estrategia**: ¿Porcentaje o stake fijo?
2. **Edita tu `.env`**: Configura `COPY_MODE` y los parámetros correspondientes
3. **Prueba en dry-run**: Usa `DRY_RUN=true` primero
4. **Monitorea**: Observa cómo funciona durante unas horas
5. **Ajusta**: Modifica los valores según tus necesidades
6. **Activa**: Cuando estés listo, cambia a `DRY_RUN=false`

---

¿Tienes más preguntas? Revisa el [README.md](README.md) principal o crea un Issue en el repositorio.
