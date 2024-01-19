import subprocess
from pathlib import Path

from ..common.consts import GITHUB_ROOT_PATH, SSH_URL
from .log import logger


def git_clone(
    user: str,
    repo: str,
    dst: Path | None,
    *,
    config,
):
    url = f'{SSH_URL}{user}/{repo}.git'
    dst = GITHUB_ROOT_PATH / f'{user}/{dst or repo}'
    cmd = f'git clone {url} {dst} {config}'
    logger.info(cmd)
    cp = subprocess.run(cmd)
    if cp.returncode == 0:
        logger.info(f'done: {dst}, url={url}')
    else:
        logger.error(f'failed: {user}/{repo}')
        try:
            dst.parent.rmdir()
        except:
            pass
