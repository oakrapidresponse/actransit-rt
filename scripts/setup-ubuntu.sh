#!/usr/bin/env bash

# exit when a command fails instead of blindly blundering forward
set -e
# treat unset variables as an error and exit immediately
set -u
# don't hide exit codes when pipeline output to another command
set -o pipefail

echo "Installing system dependencies"
sudo apt-get update
sudo apt-get -y install --no-install-recommends \
    bash \
    build-essential \
    curl \
    expat \
    fontconfig \
    gcc \
    git \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libmpfr-dev \
    libncurses-dev \
    libpq-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    locales \
    make \
    openssl \
    sudo \
    tk-dev \
    unzip \
    vim \
    wget \
    wget \
    xz-utils \
    zip \
    zlib1g \
    zlib1g-dev

echo "Installing project dependencies"
sudo apt-get update
sudo apt-get -y install --no-install-recommends \
    shellcheck

echo "Installing pyenv"
curl https://pyenv.run | bash

# shellcheck disable=SC2016
{
    echo ''
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
    echo 'eval "$(pyenv init --path)"'
    echo 'eval "$(pyenv init -)"'
    echo 'eval "$(pyenv virtualenv-init -)"'
 } >> ~/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

echo "Installing project python version"
"$PYENV_ROOT"/bin/pyenv install
"$PYENV_ROOT"/bin/pyenv global "$(cat .python-version)"

echo "Installing pipx"
python3 -m pip install --user pipx
python3 -m pipx ensurepath

echo "Installing poetry"
curl -sSL https://install.python-poetry.org | python3 -

export PATH="$HOME/.local/bin:$PATH"

echo "Installing python dependencies using Poetry into local venv"
"$HOME"/.local/bin/poetry env use "$(cat .python-version)"
"$HOME"/.local/bin/poetry install

echo "Enabling pre-commit hooks"
"$HOME"/.local/bin/poetry run tox -e install-hooks

echo "Install done."
