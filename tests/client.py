from starlette.testclient import TestClient as PureClient


class TestClient(PureClient):
    def __init__(self, prefix: str = "", *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.prefix = prefix

    def request(self, *args, **kwargs):
        return super(TestClient, self).request(*args, **kwargs)