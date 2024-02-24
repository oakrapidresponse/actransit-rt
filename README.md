# AC Transit Realtime Archiver

## Usage

Before using the project, either install it by following instructions in [Installation](#installation) section, or configure a development environment by following instructions in [Development](#development) section.

### Commands

- Output project version

    ```python
    actransit-rt version
    ```

- Retrieve latest vehicle positions

    ```python
    actransit-rt archive retrieve-vehicle-positions --input-dir=gs://tvrr-transit-snapshots/actransit/gtfs-rt --limit=10
    ```

## Installation

If not developing, then no need to clone this repo. You can use [pipx](https://github.com/pypa/pipx) to install the project directly. If you don't have `pipx` then first [install it](https://pypa.github.io/pipx/installation/).

1. Install the project:

    ```sh
    pipx install git+https://github.com/bryanculbertson/actransit-rt
    ```

1. Test your installation!

    ```sh
    actransit-rt --help
    ```

## Development

If developing, then clone this repo, setup a development environment, and run the project from there.

### Setup System Environment

This project uses [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://github.com/python-poetry/poetry) to manage python virtual environment and dependencies. If you have a working `python` system with those tools installed then you can skip system environment setup and go straight to [Setup Project Environment](#setup-project-environment).

If you know what you are doing, then you can skip using `pyenv` as long as you have the version of python installed that is specified in `.python-version`.

#### VSCode Devcontainer/Github Codespace

1. Create a Codespace or open in VS Code locally

    Follow Github instructions to [Create a Codespace](https://docs.github.com/en/codespaces/developing-in-codespaces/creating-a-codespace) for this project, or VS Code instructions to [open repo in container](https://code.visualstudio.com/docs/remote/containers-tutorial)

1. Choose the local `.venv` python if given a choice.

#### Ubuntu/Debian

1. Install python build dependencies:

    ```sh
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
    ```

1. Install project dependencies:

    ```sh
    sudo apt-get update
    sudo apt-get -y install --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        shellcheck
    ```

1. Install [pyenv](https://github.com/pyenv/pyenv) (if you haven't already):

    ```sh
    curl https://pyenv.run | bash
    ```

    Add `pyenv` paths for `bash`:

    ```sh
    {
        echo ''
        echo 'export PYENV_ROOT="$HOME/.pyenv"'
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
        echo 'eval "$(pyenv init --path)"'
        echo 'eval "$(pyenv init -)"'
        echo 'eval "$(pyenv virtualenv-init -)"'
    } >> ~/.bashrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.bashrc
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:

    ```sh
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version specified in `.python-version`:

    ```sh
    pyenv install
    ```

    Check correct `python`  version was installed by verifying it matches `.python-version`:

    ```sh
    python --version
    cat .python-version
    ```

1. Install [poetry](https://github.com/python-poetry/poetry) (if you haven't already):

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Add `poetry` paths for `bash`:

    ```sh
    echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.bashrc
    ```

1. Install `gcloud-cli` (if you haven't already)

    https://cloud.google.com/sdk/docs/install-sdk#deb

    ```sh
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

    sudo apt-get update && sudo apt-get install google-cloud-cli
    ```

#### Mac

1. Install homebrew (if you haven't already):

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

1. Install python build dependencies:

    ```sh
    brew install openssl readline sqlite3 xz zlib
    ```

1. Install project dependencies:

    ```sh
    brew install shellcheck
    ```

1. Install [pyenv](https://github.com/pyenv/pyenv) (if you haven't already):

    ```sh
    brew install pyenv
    ```

    Add `pyenv` path for `zsh` (or `~/.bashrc` if using `bash`):

    ```sh
    echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.zprofile
    source ~/.zshrc
    ```

    Check `pyenv` was installed correctly by verifying `python` points to `~/.pyenv/shims/python`:

    ```sh
    which python
    ```

    If you have an issue, see pyenv's [instructions](https://github.com/pyenv/pyenv#basic-github-checkout).

1. Install project python version specified in `.python-version`:

    ```sh
    pyenv install
    ```

    Check correct `python`  version was installed by verifying it matches `.python-version`:

    ```sh
    python --version
    cat .python-version
    ```

1. Install [poetry](https://github.com/python-poetry/poetry) (if you haven't already):

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Add `poetry` path for `zsh` (or `~/.bashrc` if using `bash`):

    ```sh
    echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.zshrc
    ```

    Refresh current shell with updated paths:

    ```sh
    source ~/.zshrc
    ```

1. Install `gcloud-cli` (if you haven't already)

    Download and extract the `tar.gz` package for your Platform from here:
    https://cloud.google.com/sdk/docs/install-sdk#mac

    ```sh
    ./google-cloud-sdk/install.sh
    ```

### Setup Project Environment

After setting up system environment with `pyenv` and `poetry`, then you can install the project and its depedancies.

1. Install project python version specified in `.python-version`:

    ```sh
    pyenv install
    ```

    Check correct `python`  version was installed by verifying it matches `.python-version`:

    ```sh
    python --version
    cat .python-version
    ```

1. Install project and dependancies into local poetry managed `.venv`:

    ```sh
    poetry env use "$(cat .python-version)"
    poetry install
    ```

    Add poetry plugins used by this project

    ```sh
    poetry self add poetry-plugin-export poetry-plugin-dotenv
    ```

1. Test your installation!

    ```sh
    poetry run actransit-rt --help
    ```

    *or*

    ```sh
    poetry shell
    actransit-rt --help
    ```

### Setup Google Cloud

1. Init `gcloud`

    *If you are working with TVRR then choose project `tvrr-409423` and compute zone `us-west1-b`:*

    ```sh
      gcloud init
      gcloud auth application-default login
    ```

### Testing

After setting up system and project environments you can run tests, formatting, linting, etc. with [tox](https://github.com/tox-dev/tox).

`tox` is installed and managed within the local venv so either activate the `venv` with `poetry shell`, or prefix each command with `poetry run`.

1. Run tests and linting

    ```python
    poetry run tox
    ```

1. Run tests

    ```python
    poetry run tox -qe test
    ```

1. Run linting

    ```python
    poetry run tox -qe lint
    ```

1. Enable pre-commit hooks:

    ```sh
    poetry run tox -e install-hooks
    ```
