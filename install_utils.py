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

    success = run_command(f'ln -s {target_path} {symbolic_path}', shell=True)
    print(f'Symlinking {target_path} --> {symbolic_path}: success = {success}')


def run_command(command: str, print_to_console: bool=True) -> bool:
    print(f'Running command: \"{command}\"')
    ret = subprocess.run(command, shell=True, capture_output=True, text=True)
    stdout = ret.stdout.strip()
    stderr = ret.stderr.strip()

    success = (ret.returncode == 0)
    if not success:
        print(f'{ERROR_STR} Command failed')
    if print_to_console or not success:
        print('Command output:')
        print(stdout)
    if not success:
        print('Command error:')
        print(stderr)

    return success
