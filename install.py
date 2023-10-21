import argparse
import subprocess
from pathlib import Path
from sys import platform
from install_utils import *


def install_helix():
    if platform == 'linux':
        run_command(f'sudo add-apt-repository ppa:maveonair/helix-editor')
        run_command(f'sudo apt update')
        run_command(f'sudo apt install helix')
    elif platform == 'darwin':
        run_command(f'brew install helix')
    else:
        raise ValueError(f'Unsupported platform {platform}')
    create_symlink('helix', '~/.config/helix')


def install_zsh() -> bool:
    success = run_command(f'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    if not success:
        return success
    # ~/.zshrc needs ZSH_CUSTOM set to zsh-custom
    zshrc_path = Path('~/.zshrc').expanduser()
    zsh_custom_path = DOTFILES_DIR / 'zsh-custom'
    if not zsh_custom_path.exists():
        raise ValueError(f'Missing zsh-custom directory {zsh_custom_path}')
    print(f'USER ACTION: Set ZSH_CUSTOM={zsh_custom_path} in {zshrc_path}')

    # Plugins for zsh
    plugins = "git fzf zsh-autosuggestions zsh-syntax-highlighting"
    print(f'USER ACTION: Set plugins=({plugins}) in {zshrc_path}')
    return success


def install_rust() -> bool:
    success = run_command(f'curl https://sh.rustup.rs -sSf | sh')
    return success


def install_zellij() -> bool:
    success = run_command(f'cargo install --locked zellij')
    create_symlink('zellij', '~/.config/zellij')
    return success


install_functions = [install_helix, install_zsh, install_rust, install_zellij]

for idx, install_fn in enumerate(install_functions):
    installing_name = install_fn.__name__.split('_')[1]

    should_install = input(f'Install {installing_name}?\n[y/N] ').lower() == 'y'
    if not should_install:
        continue

    success = install_fn()
    if success:
        print(f'\033[92mInstalled successfully\033[0m')
    else:
        print(f'\033[91mFailed to install\033[0m')

    if idx != (len(install_functions) - 1):
        input('Press Enter to continue...')
