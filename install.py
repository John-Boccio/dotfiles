#!/usr/bin/env python3

import subprocess
from pathlib import Path


DOTFILES_DIR = Path(__file__).parent
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

print()

# ~/.zshrc needs ZSH_CUSTOM set to zsh-custom
zshrc_path = Path('~/.zshrc').expanduser()
zsh_custom_path = DOTFILES_DIR / 'zsh-custom'
if not zsh_custom_path.exists():
    raise ValueError(f'Missing zsh-custom directory {zsh_custom_path}')
print(f'USER ACTION: Set ZSH_CUSTOM={zsh_custom_path} in {zshrc_path}')

print()

# Plugins for zsh
plugins = "git fzf zsh-autosuggestions zsh-syntax-highlighting"
print(f'USER ACTION: Set plugins=({plugins}) in {zshrc_path}')
