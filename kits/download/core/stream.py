from fake_useragent import FakeUserAgent
from requests import Session

_session = Session()
_session.headers.update({'user-agent': FakeUserAgent().edge})

get = _session.get
