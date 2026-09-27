import httpx
import urllib3

from ._base import BaseProvider


class HttpxProvider(BaseProvider):
    """Synchronous REST provider based on httpx.

    `api_key` is sent as `Authorization: Bearer <key>` on every request,
    matching the Aptos Labs API gateway authentication scheme.
    """

    def __init__(self, base_url: str, api_key: str | None = None):
        super().__init__(base_url)
        assert base_url is not None or "", "url is required"
        self.base_parsed_url = urllib3.util.parse_url(base_url)
        self.base_url = self.base_parsed_url.url
        self.headers = dict(self.DEFAULT_HEADERS)
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.Client(headers=self.headers)

    def close(self):
        self.client.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def _get(
        self, api: str = "", params: dict | None = None, **kwargs
    ) -> httpx.Response:
        f = self.patch_url(api)
        return self.client.get(url=f, params=params, **kwargs)

    def _post(
        self, api: str = "", params: dict | None = None, **kwargs
    ) -> httpx.Response:
        f = self.patch_url(api)
        return self.client.post(url=f, json=params, **kwargs)

    def get(self, api: str = "", params_dict: dict | None = None, **kwargs):
        return self._get(api, params_dict, **kwargs).json()

    def post(self, api: str = "", params_dict: dict | None = None, **kwargs):
        return self._post(api, params_dict, **kwargs).json()
