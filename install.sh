#!/bin/sh
set -e

APP_DIR="/opt/zapret2-control-panel"
REPO_URL="https://github.com/Sesdear/zapret2-control-panel.git"
BIN_PATH="/usr/local/bin/zapret2-cp"

install_dependencies() {
    kernel="$(uname -s)"

    if [ "$kernel" != "Linux" ]; then
        echo "Поддерживается только Linux."
        exit 1
    fi

    [ -f /etc/os-release ] && . /etc/os-release || {
        echo "Не удалось определить ОС"
        exit 1
    }

    find_package_manager() {
        case "$1" in
            arch|artix|cachyos|endeavouros|manjaro|garuda)
                echo "$SUDO pacman -Syu --noconfirm && $SUDO pacman -S --noconfirm --needed git python python-pip"
                ;;
            debian|ubuntu|mint)
                echo "$SUDO apt update -y && $SUDO apt install -y git python3 python3-venv python3-pip"
                ;;
            fedora|almalinux|rocky|rhel|centos|oracle|redos)
                echo "if command -v dnf >/dev/null 2>&1; then $SUDO dnf install -y git python3 python3-pip; else $SUDO yum install -y git python3 python3-pip; fi"
                ;;
            void)
                echo "$SUDO xbps-install -S && $SUDO xbps-install -y git python3 python3-pip"
                ;;
            gentoo)
                echo "$SUDO emerge --sync --quiet && $SUDO emerge dev-vcs/git dev-lang/python"
                ;;
            opensuse)
                echo "$SUDO zypper refresh && $SUDO zypper install -y git python3 python3-pip"
                ;;
            alpine)
                echo "$SUDO apk update && $SUDO apk add git python3 py3-pip"
                ;;
            *)
                echo ""
                ;;
        esac
    }

    install_cmd="$(find_package_manager "$ID")"
    if [ -z "$install_cmd" ] && [ -n "$ID_LIKE" ]; then
        for like in $ID_LIKE; do
            install_cmd="$(find_package_manager "$like")"
            [ -n "$install_cmd" ] && break
        done
    fi

    if [ -n "$install_cmd" ]; then
        eval "$install_cmd"
    else
        echo "Неизвестная ОС: ${ID:-Неизвестно}"
        exit 1
    fi
}

if [ "$(awk '$2 == "/" {print $4}' /proc/mounts)" = "ro" ]; then
    echo "Файловая система только для чтения."
    exit 1
fi

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

if ! command -v git >/dev/null 2>&1 || ! command -v python3 >/dev/null 2>&1; then
    install_dependencies
fi

if [ ! -d "$APP_DIR" ]; then
    $SUDO git clone "$REPO_URL" "$APP_DIR"
else
    cd "$APP_DIR"
    if ! $SUDO git pull; then
        echo "Ошибка обновления, пересоздаю репозиторий..."
        cd /
        $SUDO rm -rf "$APP_DIR"
        $SUDO git clone "$REPO_URL" "$APP_DIR"
    fi
fi

cd "$APP_DIR"

if [ ! -d ".venv" ]; then
    $SUDO python3 -m venv .venv
fi

$SUDO ./.venv/bin/python -m pip install --upgrade pip
$SUDO ./.venv/bin/python -m pip install -r requirements.txt
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
echo "Запуск: sudo zapret2-cp"
