#!/bin/bash
# Script de instalación para la versión Python

echo "🐍 Instalando bot de copy trading de Polymarket (Python)"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior:"
    echo "  - Windows: https://www.python.org/downloads/"
    echo "  - Mac: brew install python3"
    echo "  - Linux: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "Por favor instala pip3"
    exit 1
fi

echo "✓ pip encontrado: $(pip3 --version)"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -r ../requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Instalación completada!"
    echo ""
    echo "Siguiente paso:"
    echo "1. Copia y configura .env:"
    echo "   cp ../.env.example ../.env"
    echo "   nano ../.env"
    echo ""
    echo "2. Ejecuta el bot:"
    echo "   python3 main.py"
else
    echo ""
    echo "❌ Error en la instalación"
    exit 1
fi
