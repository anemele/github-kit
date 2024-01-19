import pytest

from ..common.types import Repo
from .core.core import get_release_info, query_release


@pytest.mark.skip()
def test_query_release():
    r = query_release(Repo('neovim', 'neovim'))
    assert r is not None
    assert type(r) is list
    assert len(r) > 0
    assert type(r[0]['assets']) is list


@pytest.mark.skip()
def test_get_release_info():
    r = query_release(Repo('neovim', 'neovim'))
    assert r is not None
    info = get_release_info(r)
    assert len(info) > 1
