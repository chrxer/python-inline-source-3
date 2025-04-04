#!/usr/bin/env bash

set -e
stmp() {
    date +"%m-%d %T"
}

USER=$(awk -F: '$3 >= 1000 && $3 < 60000 {print $1; exit}' /etc/passwd)

nsu() {
    printf "\033[94m[EXC %s]\033[0m %s\n" "$(stmp)" "$*"
    sudo -u "$USER" env "PATH=$PATH" "$@"
}

asu() {
    printf "\033[94m[EXC %s]\033[0m sudo %s\n" "$(stmp)" "$*"
    sudo env "PATH=$PATH" "$@"
}

asu apt install python3

# Download and install nvm:
LATEST=$(nsu curl -s https://api.github.com/repos/nvm-sh/nvm/releases/latest | grep -o '"tag_name": *"v[^"]*' | cut -d '"' -f4)
asu curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/$LATEST/install.sh | bash

UHOME=$(su $USER -c 'echo $HOME')
# in lieu of restarting the shell
asu chmod +x $UHOME/.nvm/nvm.sh
NVMSH=$UHOME/.nvm/nvm.sh

# Download and install Node.js:
su $USER -c "source $NVMSH;nvm install 23"
su $USER -c "source $NVMSH;npm install -g @vscode/vsce"


nsu python3 -m venv .venv
nsu ./.venv/bin/python3 -m pip install --upgrade pip build
nsu ./.venv/bin/python3 -m pip install -r requirements.txt -r requirements-dev.txt
