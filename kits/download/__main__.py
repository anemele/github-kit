import argparse

from .core.core import run

parser = argparse.ArgumentParser(prog='ghd', description=__doc__)
parser.add_argument(
    'url',
    type=str,
    nargs='?',
    help='read from manifest by default.',
)
args = parser.parse_args()

url: str | None = args.url

try:
    run(url)
except KeyboardInterrupt:
    pass
