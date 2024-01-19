from pathlib import Path
from typing import Iterable

from .log import logger


def get_url_list_from_file(file: Path) -> Iterable[str]:
    try:
        return (line.strip() for line in file.read_text().strip().splitlines())
    except Exception as e:
        logger.warning(e)

    return ()
