from pathlib import Path
import subprocess


DOTFILES_DIR = Path(__file__).parent
ERROR_STR = '\033[91mERROR!\033[0m'


def create_symlink(target, symbolic_path):
    target_path = DOTFILES_DIR / target
    if not target_path.exists():
        raise ValueError(f'Invalid target path {target_path}')

    symbolic_path = Path(symbolic_path).expanduser()
    if symbolic_path.exists():
        print(f'Skipped symlinking {target_path} --> {symbolic_path} as it already exists')

    success = run_command(f'ln -s {target_path} {symbolic_path}')
    print(f'Symlinking {target_path} --> {symbolic_path}: {"SUCCESS" if success else "FAILURE"}')


def run_command(command: str, print_to_console: bool=True) -> bool:
    print(f'Running command: \"{command}\"')
    ret = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)

    output = ''
    for line in ret.stdout:
        if print_to_console:
            print(line, flush=True, end='')
        output += line
    for line in ret.stdin:
        if print_to_console:
            print(line, flush=True, end='')
        output += line
    for line in ret.stderr:
        if print_to_console:
            print(line, flush=True, end='')
        output += line

    ret.stdin.closer()

    ret.wait()

    if ret.returncode != 0:
        print(f'{ERROR_STR} Command failed: {ret.args}, return code = {ret.returncode}\n')

    return (ret.returncode == 0)

