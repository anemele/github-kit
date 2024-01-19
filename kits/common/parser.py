import re
from typing import Iterable

from .consts import HTTP_URL
from .log import logger
from .types import Repo

PATTERN = re.compile(r'^(?:https://[\w\.\-]+/)|(?:git@[\w\.\-]+:)')
PATTERN2 = re.compile(r'([\w-]+)/([\w\.-]+)')


def parse_url(url: str) -> Repo | None:
    s = PATTERN.search(url)
    if s is not None:
        url = url[s.end() :]

    url = url.removeprefix('/')
    s2 = PATTERN2.match(url)
    if s2 is None:
        return

    owner, repo = s2.groups()
    if s2.end() == s2.endpos or url[s2.end()] != '/':
        repo = repo.removesuffix('.git')

    return Repo(owner, repo)


def parse_url_batch(url_list: Iterable[str]) -> Iterable[Repo]:
    for url in url_list:
        sth = parse_url(url)
        if sth is None:
            logger.warning(f'invalid url: {url}')
            continue
        yield sth


def check(urls: list[str]) -> None:
    for r in parse_url_batch(urls):
        print(f'{HTTP_URL}{r}.git')
