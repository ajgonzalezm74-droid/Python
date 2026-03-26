#!/bin/bash

echo "🔧 CORRIGIENDO ERROR DE COMPILACIÓN"
echo "==================================="

# Activar entorno
cd ~/Python/kivy_de_tu_calculadora
source ../.venv/bin/activate

# 1. Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y clang-14 build-essential python3-dev libffi-dev libssl-dev

# 2. Reinstalar Cython
echo "📦 Reinstalando Cython..."
pip uninstall cython -y
pip install cython==3.0.10

# 3. Reinstalar Kivy
echo "📦 Reinstalando Kivy..."
pip uninstall kivy -y
pip install kivy[full]==2.3.0

# 4. Crear directorio para jnius si no existe
echo "📁 Creando estructura de directorios..."
mkdir -p .buildozer/android/platform/build-armeabi-v7a/build/other_builds/jnius-python3/jnius

# 5. Limpiar compilación anterior
echo "🧹 Limpiando compilación anterior..."
rm -rf .buildozer bin
rm -rf ~/.buildozer/android/platform/android-ndk-r25b

# 6. Modificar buildozer.spec para usar archivos locales
echo "⚙️ Configurando buildozer.spec..."
if [ -f "buildozer.spec" ]; then
    sed -i 's/^android.ndk = .*/android.ndk = 23b/' buildozer.spec
    sed -i 's/^android.api = .*/android.api = 30/' buildozer.spec
fi

# 7. Intentar compilar
echo "🚀 Iniciando compilación..."
buildozer android debug -v

echo "✅ Proceso completado"
