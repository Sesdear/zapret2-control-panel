#!/bin/sh
set -eu

APP_DIR="/opt/zapret2-control-panel"
BIN_PATH="/usr/local/bin/zapret2-cp"

echo "== Zapret2 Control Panel uninstaller =="

if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
else
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    elif command -v doas >/dev/null 2>&1; then
        SUDO="doas"
    else
        echo "Ошибка: требуются права суперпользователя"
        exit 1
    fi
fi

echo
echo "Будут удалены:"
echo "  - $APP_DIR"
echo "  - $BIN_PATH"
echo
printf "Продолжить? [y/N]: "
read ans
case "$ans" in
    y|Y|yes|YES) ;;
    *) echo "Отменено"; exit 0 ;;
esac

if [ -f "$BIN_PATH" ]; then
    echo "Удаление команды zapret2-cp..."
    $SUDO rm -f "$BIN_PATH"
else
    echo "Команда zapret2-cp не найдена — пропускаем"
fi

if [ -d "$APP_DIR" ]; then
    echo "Удаление каталога приложения..."
    $SUDO rm -rf "$APP_DIR"
else
    echo "Каталог приложения не найден — пропускаем"
fi

echo
echo "Удаление завершено."
