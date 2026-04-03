# Humari - Discord бот з зручним налаштуванням модулів

> [!WARNING]
> Бот створюється однією бездарною людиною, тому будьте готові до величезної кількості говнокоду та багів. Я буду старатися покращувати бота, але нічого дуже хорошого обіцяти не можу.

> [!NOTE]
> Цей проєкт задувувався як бот для одного сервера. Тобто, він не зможе правильно функціонувати на декількох серверах.

В файлі `config/modules.jsonc` ви можете налаштовувати івенти та деякі команди бота:
```jsonc
{
  "server_modules": {
    "events": {
      "on_voice_state_update": {
        "load_module": true,
        "create_channel_id": 1482679460221423678,
        "send_msg": true
      },
      "on_member_join": {
        "load_module": true,
        "send_welcome_msg_to": 1466851747090792552
      }
    }
  },
  "client_modules": {
    "events": {
      "on_ready": {
        "load_module": true
      }
    },
    "commands": {
      "help": {
        "load_module": true,
        "show_disabled_commands": true
      }
    }
  }
}
```

## Як його запустити?!
1. Спочатку, клонуйте код собі:
```
git clone https://github.com/cjoyer/humari.git
```
2. Далі, створіть `.venv` в директорії бота, встановіть залежності та додайте змінну середовища:
```
python -m venv .venv
pip install -r requirements.txt
export DISCORD_BOT_TOKEN="your_token"
```
3. Запустіть бота:
```
[~]$ python -m source.main
```
Або, можете використати цей скріпт:
```sh
#!/bin/bash

function log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") [bash] $*"
}

log "Starting via \"start.sh\"..."

required_packages=("disnake" "commentjson")
venv_path=".venv"
export DISCORD_BOT_TOKEN="your_token"

function install_packages() {
    for pkg in "${required_packages[@]}"; do
        if ! pip show "$pkg" &>/dev/null; then
            log "Package \"$pkg\" is not installed, installing..."
            pip install "$pkg"
            log "Package \"$pkg\" was installed"
        else
            log "Package \"$pkg\" is already installed"
        fi
    done
}

if [ -d "$venv_path" ]; then
    log "\"$venv_path\" exists"
    source "$venv_path/bin/activate"
    log "venv was activated"
    install_packages
else
    log "\"$venv_path\" does not exist, creating..."
    python -m venv "$venv_path"
    log "\"$venv_path\" was created"
    source "$venv_path/bin/activate"
    log "venv was activated"
    log "Upgrading pip..."
    pip install --upgrade pip
    log "pip was upgraded"
    install_packages
fi

python -m source.main
```
