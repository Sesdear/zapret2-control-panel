#!/bin/sh
set -e

APP_DIR="/opt/zapret2-control-panel"
REPO_URL="https://github.com/Sesdear/zapret2-control-panel.git"
BIN_PATH="/usr/local/bin/zapret2-cp"

echo "Проверка прав суперпользователя..."
if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
else
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    elif command -v doas >/dev/null 2>&1; then
        SUDO="doas"
    else
        echo "Требуются права суперпользователя."
        exit 1
    fi
fi

if [ -r /proc/mounts ] && [ "$(awk '$2=="/"{print $4}' /proc/mounts)" = "ro" ]; then
    echo "Файловая система только для чтения."
    exit 1
fi

install_dependencies() {
    [ -f /etc/os-release ] || { echo "Не удалось определить ОС"; exit 1; }
    . /etc/os-release

    echo "Установка зависимостей..."
    case "$ID" in
        arch|artix|cachyos|endeavouros|manjaro|garuda)
            $SUDO pacman -Syu --noconfirm
            $SUDO pacman -S --noconfirm --needed git python python-pip
            ;;
        debian|ubuntu|mint)
            $SUDO apt update -y
            $SUDO apt install -y git python3 python3-venv python3-pip
            ;;
        fedora|almalinux|rocky|rhel|centos|oracle|redos)
            if command -v dnf >/dev/null 2>&1; then
                $SUDO dnf install -y git python3 python3-pip
            else
                $SUDO yum install -y git python3 python3-pip
            fi
            ;;
        void)
            $SUDO xbps-install -S
            $SUDO xbps-install -y git python3 python3-pip
            ;;
        opensuse*)
            $SUDO zypper refresh
            $SUDO zypper install -y git python3 python3-pip
            ;;
        alpine)
            $SUDO apk update
            $SUDO apk add git python3 py3-pip
            ;;
        *)
            echo "Неподдерживаемая ОС: $ID"
            exit 1
            ;;
    esac
}

command -v git >/dev/null 2>&1 || install_dependencies
command -v python3 >/dev/null 2>&1 || install_dependencies

echo "Клонируем или обновляем репозиторий..."
if [ ! -d "$APP_DIR" ]; then
    $SUDO git clone "$REPO_URL" "$APP_DIR"
else
    cd "$APP_DIR"
    if ! $SUDO git pull; then
        cd /
        $SUDO rm -rf "$APP_DIR"
        $SUDO git clone "$REPO_URL" "$APP_DIR"
    fi
fi

cd "$APP_DIR"

echo "Создание виртуального окружения..."
if [ ! -d ".venv" ]; then
    $SUDO python3 -m venv .venv
fi

echo "Установка зависимостей Python..."
$SUDO ./.venv/bin/python -m pip install --upgrade pip
$SUDO ./.venv/bin/python -m pip install -r requirements.txt

echo "Создание команды zapret2-cp..."
$SUDO tee "$BIN_PATH" >/dev/null << 'EOF'
#!/bin/sh

if [ "$(id -u)" -ne 0 ]; then
    echo "Эта команда должна быть запущена с sudo"
    exit 1
fi

APP_DIR="/opt/zapret2-control-panel"
PYTHON="$APP_DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "Виртуальное окружение не найдено"
    exit 1
fi

exec "$PYTHON" "$APP_DIR/app.py" "$@"
EOF

$SUDO chmod +x "$BIN_PATH"

echo "Установка завершена."
echo "Запуск приложения: sudo zapret2-cp"
