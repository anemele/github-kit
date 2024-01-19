from typing import Iterable

from ..consts import DOWNLOAD_DIR
from .log import logger
from .mirrors import MIRROR_SITE
from .stream import get


def get_mirror_url(url: str):
    for mirror in MIRROR_SITE:
        yield mirror(url)


def download_release(urls: Iterable[str]) -> tuple[int, int]:
    succ = 0
    count = 0

    for url in urls:
        count += 1
        for mirror in get_mirror_url(url):
            logger.info(f'GET {mirror}')
            resp = get(mirror)
            if resp.status_code != 200:
                continue
            path = DOWNLOAD_DIR / mirror.rsplit('/', 1)[-1]
            if path.exists():
                logger.warning(f'exists {path}')
            path.write_bytes(resp.content)
            succ += 1
            logger.info(f'SAVE {path}')

            break
        else:
            logger.warning(f'NO ACCESSIBLE RESOURCE: {url}')

    logger.info(f'FINISH {succ}/{count}')
    return succ, count
