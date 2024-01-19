import json
import subprocess as sbp
from dataclasses import dataclass
from itertools import chain
from typing import Any, Iterable

from pick import pick

from ...common.parser import parse_url
from ...common.types import Repo
from ..config import choose_repo
from ..consts import DOWNLOAD_DIR
from ..log import logger
from ..parser import parse_download_link
from .download import download_release


def run(url: str | None):
    if url is not None:
        repo = parse_url(url)
        if repo is None:
            logger.warning(f'invalid url: {url}')
            return
        urls = get_download_url(repo)
    else:
        repos = choose_repo()
        if repos is None:
            return
        urls = tuple(chain(*map(get_download_url, repos)))
    s, _ = download_release(urls)
    if s > 0:
        sbp.run(f'explorer {DOWNLOAD_DIR}')


def get_download_url(repo: Repo) -> Iterable[str]:
    info = get_download_info(repo)
    if info is None:
        return ()

    release, assets = info
    logger.info(f'choose {len(assets)} of {repo}')
    return (f'{release}/{asset}' for asset in assets)


def get_download_info(repo: Repo):
    choice = get_tag_choice(repo)
    if choice is None:
        return

    url, assets = choice
    if assets is None or len(assets) == 0:
        logger.info(f'no choice: {repo}')
        return

    release = parse_download_link(url)
    if release is None:
        logger.info(f'no release found: {repo}')
        return

    return release, assets


def get_tag_choice(repo: Repo) -> tuple[str, tuple[str, ...]] | None:
    resp = query_release(repo)
    if resp is None or len(resp) == 0:
        logger.error(f'no release found: {repo}')
        return

    info = get_release_info(resp)
    logger.debug(f'{len(info)=}')
    if len(info) == 0:
        logger.error(f'no tag found: {repo}')
        return

    index: int
    _, index = pick([i.name for i in info], str(repo))  # type: ignore
    tag = info[index]
    if len(tag.assets) == 0:
        logger.error(f'no assets found: {repo}')
        return

    choices = pick([i.name for i in tag.assets], tag.url, multiselect=True)

    return tag.url, tuple(x[0] for x in choices)  # type: ignore


def query_release(repo: Repo) -> list[dict[str, Any]] | None:
    ret = sbp.run(f'gh api repos/{repo}/releases', capture_output=True)
    if ret.returncode != 0:
        logger.error(f'{repo}: {ret.stderr}')
        return

    return json.loads(ret.stdout)


@dataclass
class Asset:
    name: str
    size: int
    url: str

    def __str__(self) -> str:
        return f'{self.name}:{self.size:,}  {self.url}'


@dataclass
class Release:
    name: str
    url: str
    assets: list[Asset]


def get_release_info(data):
    return [
        Release(
            it['name'],
            it['html_url'],
            [
                Asset(asset['name'], asset['size'], asset['browser_download_url'])
                for asset in it['assets']
            ],
        )
        for it in data
    ]
