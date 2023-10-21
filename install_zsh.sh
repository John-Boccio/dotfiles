#/usr/bin/env bash

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

ZSHRC_PATH="$HOME/.zshrc"
OH_MY_ZSH_PATH="$HOME/.oh-my-zsh"
ZSHRC_CUSTOM_PATH="$OH_MY_ZSH_PATH/custom"
ZSH_CUSTOM="$(pwd)/zsh-custom"

if [ -d "$ZSH_CUSTOM" ]; then
	# Create the symbolic link to the ZSH_CUSTOM location
	rm -rf $ZSHRC_CUSTOM_PATH
	ln -sT "$ZSH_CUSTOM" "$ZSHRC_CUSTOM_PATH"
	echo "Symlink created from $ZSH_CUSTOM to $ZSHRC_CUSTOM_PATH"
else
	echo "$ZSH_CUSTOM was not found"
	exit 1
fi

# https://github.com/unixorn/fzf-zsh-plugin#installing
git clone --depth 1 https://github.com/unixorn/fzf-zsh-plugin.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/fzf-zsh-plugin

# https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

echo "Modify .zshrc plugins to contain 

plugins=(
	git
	fzf
	zsh-autosuggestions
	zsh-syntax-highlighting
)

"

