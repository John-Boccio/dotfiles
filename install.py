#!/usr/bin/env python3

import subprocess
from pathlib import Path
import argparse


DOTFILES_DIR = Path(__file__).parent


parser = argparse.ArgumentParser('Dotfiles Installer')
parser.add_argument('--no-symlink', action='store_true', help='Skip symlinking step')
parser.add_argument('--no-rust', action='store_true', help='Skip installing Rust')
parser.add_argument('--no-zsh', action='store_true', help='Skip installing oh-my-zsh')
args = parser.parse_args()


def install_symlinks():
    SYMLINKS = {
        'helix' : '~/.config/helix'
    }
    # Create all dotfile symlinks
    print('Creating symlinks to setup dotfiles')
    for target, symbolic_path in SYMLINKS.items():
        target_path = DOTFILES_DIR / target
        if not target_path.exists():
            raise ValueError(f'Invalid target path {target_path}')

        symbolic_path = Path(symbolic_path).expanduser()
        if symbolic_path.exists():
            print(f'Skipped symlinking {target_path} --> {symbolic_path} as it already exists')
            continue

        ret = subprocess.call(f'ln -s {target_path} {symbolic_path}', shell=True)
        print(f'Symlinking {target_path} --> {symbolic_path}: Return code = {ret}')


def install_zsh():
    # ~/.zshrc needs ZSH_CUSTOM set to zsh-custom
    zshrc_path = Path('~/.zshrc').expanduser()
    zsh_custom_path = DOTFILES_DIR / 'zsh-custom'
    if not zsh_custom_path.exists():
        raise ValueError(f'Missing zsh-custom directory {zsh_custom_path}')
    print(f'USER ACTION: Set ZSH_CUSTOM={zsh_custom_path} in {zshrc_path}')

    # Plugins for zsh
    plugins = "git fzf zsh-autosuggestions zsh-syntax-highlighting"
    print(f'USER ACTION: Set plugins=({plugins}) in {zshrc_path}')


def install_rust():
    print(f'Installing Rust')
    ret = subprocess.call(f'curl https://sh.rustup.rs -sSf | sh', shell=True)
    print(f'Installed Rust: Return code = {ret}')


ARG_ACTIONS = {
    'symlink' : install_symlinks,
    'zsh' : install_zsh,
    'rust' : install_rust,
}

args_to_skip = set([arg for arg in ARG_ACTIONS.keys() if args.__dict__[f'no_{arg}']])
print(args_to_skip)

for arg, action in ARG_ACTIONS.items():
    if arg in args_to_skip:
        print(f'{arg} set, skipping')
        continue

    print()
    action()
