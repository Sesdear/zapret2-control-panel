#!/bin/sh
set -eu

APP_DIR="/opt/zapret2-control-panel"
REPO_URL="https://github.com/Sesdear/zapret2-control-panel.git"
BIN_PATH="/usr/local/bin/zapret2-cp"
PYTHON_REQUIRED="3.11"

echo "== Zapret2 Control Panel installer =="

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



install_dependencies() {
    . /etc/os-release || { echo "Не удалось определить ОС"; exit 1; }

    echo "Установка зависимостей для $ID..."

    case "$ID" in
        arch|artix|cachyos|endeavouros|manjaro|garuda)
            $SUDO pacman -Syu --noconfirm
            $SUDO pacman -S --noconfirm --needed git python python-pip
            ;;
        debian|ubuntu|mint)
            $SUDO apt update
            $SUDO apt install -y git python3.11 python3.11-venv python3-pip
            ;;
        fedora|almalinux|rocky|rhel|centos|oracle|redos)
            $SUDO dnf install -y git python3.11 python3-pip
            ;;
        void)
            $SUDO xbps-install -Sy git python3.11 python3-pip
            ;;
        opensuse*)
            $SUDO zypper refresh
            $SUDO zypper install -y git python311 python311-pip
            ;;
        alpine)
            $SUDO apk add --no-cache git python3 py3-pip
            ;;
        *)
            echo "Неподдерживаемая ОС: $ID"
            exit 1
            ;;
    esac
}

command -v git >/dev/null 2>&1 || install_dependencies

 PYTHON_BIN="$(command -v python3.11 || command -v python || true)"

if [ -z "$PYTHON_BIN" ]; then
    echo "Python 3.11 не найден — устанавливаем зависимости"
    install_dependencies
    PYTHON_BIN="$(command -v python3.11 || true)"
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "Ошибка: Python 3.11 недоступен"
    exit 1
fi

echo "Используется Python: $($PYTHON_BIN --version)"

if [ ! -d "$APP_DIR" ]; then
    echo "Клонирование репозитория..."
    $SUDO git clone "$REPO_URL" "$APP_DIR"
else
    echo "Обновление репозитория..."
    cd "$APP_DIR"
    if ! $SUDO git pull --rebase; then
        echo "Ошибка обновления — пересоздаём каталог"
        cd /
        $SUDO rm -rf "$APP_DIR"
        $SUDO git clone "$REPO_URL" "$APP_DIR"
    fi
fi

cd "$APP_DIR"

if [ ! -d ".venv" ]; then
    echo "Создание виртуального окружения (Python 3.11)..."
    $SUDO "$PYTHON_BIN" -m venv .venv
fi

echo "Установка Python-зависимостей..."
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt

echo "Создание команды zapret2-cp..."

$SUDO tee "$BIN_PATH" >/dev/null << EOF
#!/bin/sh
exec /opt/zapret2-control-panel/.venv/bin/python \
     /opt/zapret2-control-panel/app.py "\$@"
EOF

$SUDO chmod +x "$BIN_PATH"

echo
echo "Установка завершена успешно."
echo "Проверка Python:"
"$APP_DIR/.venv/bin/python" --version
echo
echo "Запуск:"
echo "  sudo zapret2-cp"
