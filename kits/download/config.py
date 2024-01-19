from pick import pick

from ..common.parser import parse_url
from ..common.types import Repo
from .consts import DOWLOAD_MANIFEST
from .log import logger


def _get_manifest():
    if not DOWLOAD_MANIFEST.is_file():
        return

    return DOWLOAD_MANIFEST.read_text().strip().splitlines()


def choose_repo() -> tuple[Repo, ...]:
    manifest = _get_manifest()
    if manifest is None:
        logger.error('no repo given')
        return ()

    choices = pick(manifest, 'choose repos to download release', multiselect=True)
    if len(choices) == 0:
        logger.info('no choice')
        return ()

    choice = tuple(filter(None, (parse_url(x[0]) for x in choices)))  # type: ignore
    logger.info(f'{choice=}')
    return choice


def add_manifest(item: str):
    with open(DOWLOAD_MANIFEST, 'a') as fp:
        fp.write(f'{item}\n')
