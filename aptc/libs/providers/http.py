from typing import Optional, Dict

import httpx
import urllib3

from ._base import BaseProvider


class HttpxProvider(BaseProvider):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        assert base_url is not None or '', "url is required"
        self.base_parsed_url = urllib3.util.parse_url(base_url)
        self.base_url = self.base_parsed_url.url
        self.client = httpx.Client()

    def close(self):
        self.client.close()

    def __del__(self):
        self.close()

    def _get(self, api: str = '', params: Optional[Dict] = None, **kwargs):
        f = self.patch_url(api)
        return self.client.get(url=f, params=params, headers=self.DEFAULT_HEADERS, **kwargs)

    def _post(self, api: str = '', params: Optional[Dict] = None, **kwargs):
        f = self.patch_url(api)
        return self.client.post(url=f, json=params, headers=self.DEFAULT_HEADERS, **kwargs)

    def get(self, api: str = '', params_dict: Optional[Dict] = None, **kwargs):
        return self._get(api, params_dict, **kwargs).json()

    def post(self, api: str = '', params_dict: Optional[Dict] = None, **kwargs):
        return self._post(api, params_dict, **kwargs).json()
