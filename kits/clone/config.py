import tomllib

from ..common.consts import GITHUB_ROOT_PATH

CONFIG_FILE = GITHUB_ROOT_PATH / 'config.toml'


def _get_config() -> str:
    if not CONFIG_FILE.exists():
        return ''

    with open(CONFIG_FILE, 'rb') as fp:
        config = tomllib.load(fp)

    return ' '.join(f'--{k}={v}' for k, v in config.get('config', {}).items())


CONFIG = _get_config()
