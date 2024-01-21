import argparse
import sys
from pathlib import Path

from ..common.parser import check, parse_url_batch
from .config import CONFIG, CONFIG_FILE
from .core import git_clone
from .utils import get_url_list_from_file

parser = argparse.ArgumentParser(prog='ghc', description=__doc__)
parser.add_argument('url', type=str, nargs='*', help='github repo url')
parser.add_argument(
    '-f',
    '--file',
    type=Path,
    help='read github repo url from a file, one line per url',
)
parser.add_argument(
    '-d',
    '--dest',
    type=Path,
    help='replace `user/repo` with `user/dest`',
)
parser.add_argument(
    '--check',
    action='store_true',
    help='do not clone, check validation',
)
parser.add_argument(
    '--config',
    help=f'git configs (wrapped with a pair of QUOTE). or save in a file: `{ CONFIG_FILE}`',
    default='',
)

args = parser.parse_args()

args_file: Path | None = args.file
args_url: list[str] = args.url
args_dest: Path | None = args.dest
args_check: bool = args.check
args_config: str = args.config

url_list = args_url
if args_file is not None and args_file.is_file():
    url_list.extend(get_url_list_from_file(args_file))

if len(url_list) == 0:
    parser.print_usage()
    exit()

if args_check:
    check(url_list)
    exit()

ur_list = parse_url_batch(url_list)
config = f'{CONFIG} {args_config}'

for user, repo in ur_list:
    git_clone(user, repo, args_dest, config=config)
