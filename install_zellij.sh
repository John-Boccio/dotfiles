#/usr/bin/env bash

ZELLIJ_PATH="$HOME/.config/zellij"
ZELLIJ_CUSTOM="$(pwd)/zellij"

# Install rust
curl https://sh.rustup.rs -sSf | sh
rustup update

# https://zellij.dev/documentation/installation#third-party-repositories
cargo install --locked zellij

if [ -d "$ZELLIJ_CUSTOM" ]; then
	# Create the symbolic link to the ZELLIJ_CUSTOM location
	ln -sT "$ZELLIJ_CUSTOM" "$ZELLIJ_PATH"
	echo "Symlink created from $ZELLIJ_CUSTOM to $ZELLIJ_PATH"
else
	echo "$ZELLIJ_CUSTOM was not found"
	exit 1
fi


