#!/usr/bin/env bash
# ==============================================================================
#   Thatch - sandbox_installer.sh
#   Purpose: Isolated, memory-optimized sandbox installation for legacy setups
#            Prevents installer memory exhaustion and file pollution.
#            Stealthy open-source edition (Zeus Engine).
# ==============================================================================
set -euo pipefail

# Colors for log formatting
GREEN='\e[1;32m'
RED='\e[1;31m'
NC='\e[0m'

log_info() { echo -e "${GREEN}[*] [ZEUS-ENGINE]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Helper menu
if [ "$#" -lt 3 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Uso: $0 <runner_wine_path> <final_prefixes_dir> <game_folder_name> [installer_exe]"
    echo ""
    echo "Argumentos:"
    echo "  runner_wine_path    Ruta absoluta al ejecutable 'wine' del runner elegido"
    echo "  final_prefixes_dir  Ruta al almacén de prefijos (donde guardar el prefijo definitivo)"
    echo "  game_folder_name    Nombre del juego / carpeta de destino final"
    echo "  installer_exe       (Opcional) Ruta absoluta al instalador setup.exe"
    exit 1
fi

RUNNER_WINE="$1"
FINAL_PREFIXES_DIR="$2"
GAME_FOLDER_NAME="$3"
INSTALLER_EXE="${4:-}"

# Auto-detect installer exe in the current folder if not provided
if [ -z "$INSTALLER_EXE" ]; then
    INSTALLER_EXE=$(find . -maxdepth 1 -name 'setup*.exe' -o -name '*.exe' | head -n 1)
fi

if [ -z "$INSTALLER_EXE" ] || [ ! -f "$INSTALLER_EXE" ]; then
    log_error "No se encontró el archivo ejecutable del instalador setup.exe."
    exit 1
fi

# Define paths dynamically using the provided parameters
WINEPREFIX="$FINAL_PREFIXES_DIR/.zeus_temp_prefix"
GAME_FINAL_PATH="$FINAL_PREFIXES_DIR/${GAME_FOLDER_NAME// /_}"

# Memory addressing and decompression DLL overrides (lolz/srep repacks optimizations)
export WINEDLLOVERRIDES="atl100=n;unarc,isdone=n,b"
export PROTON_FORCE_LARGE_ADDRESS_AWARE=1

# Clean up any leftover previous temp prefix
rm -rf "$WINEPREFIX"
mkdir -p "$WINEPREFIX"

log_info "Preparando laboratorio de descompresión aislado..."
log_info "WINEPREFIX temporal: $WINEPREFIX"
log_info "Lanzando instalador: $INSTALLER_EXE"
log_info "CONSEJO: En el instalador, selecciona siempre la ruta por defecto (C:\\Games\\...)"

# Execute installer inside the temporary prefix
WINEPREFIX="$WINEPREFIX" "$RUNNER_WINE" "$INSTALLER_EXE" || log_error "El instalador reportó un código de salida no cero (no fatal)."

# Scan for the decompressed game directory in the temp prefix's drive C
GAMES_DIR="$WINEPREFIX/drive_c/Games"
INSTALL_DIR=""
if [ -d "$GAMES_DIR" ]; then
    INSTALL_DIR=$(find "$GAMES_DIR" -maxdepth 1 -type d -not -path "$GAMES_DIR" | head -n 1)
fi

if [ -n "$INSTALL_DIR" ] && [ -d "$INSTALL_DIR" ]; then
    log_info "Instalación completada. Carpeta de juego detectada: $(basename "$INSTALL_DIR")"
    log_info "Migrando datos al prefijo definitivo: $GAME_FINAL_PATH"
    
    # Establish final prefix layout
    FINAL_GAMES_DIR="$GAME_FINAL_PATH/drive_c/Games"
    mkdir -p "$FINAL_GAMES_DIR"
    
    # Relocate data atomically
    mv "$INSTALL_DIR" "$FINAL_GAMES_DIR/"
    
    log_info "¡Migración completada con éxito!"
    log_info "Juego disponible en: $FINAL_GAMES_DIR/$(basename "$INSTALL_DIR")"
    
    # Cleanup temp laboratory
    rm -rf "$WINEPREFIX"
    log_info "Sandbox temporal eliminado. Sistema Zeus limpio y ordenado."
else
    log_error "No se detectó ninguna carpeta de juego instalada. ¿Se canceló la instalación?"
    exit 1
fi
