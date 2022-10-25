import asyncio
from typing import Union, List, Optional, Dict

import httpx
import urllib3

from ._base import BaseProvider


# [WIP]
class HttpxAsyncProvider(BaseProvider):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        assert base_url is not None or '', "url is required"
        self.base_parsed_url = urllib3.util.parse_url(base_url)
        self.base_url = self.base_parsed_url.url
        self.client = httpx.AsyncClient()
        self.loop = asyncio.get_event_loop()

    async def close(self):
        await self.client.aclose()

    def __del__(self):
        self.loop.run_until_complete(self.close())
        self.loop.close()

    async def _get(self, api: str = '', params: Optional[Dict] = None):
        f = self.patch_url(api)
        response = await self.client.get(url=f, params=params)
        return response.json()

    async def _post(self, api: str = '', params: Optional[Dict] = None):
        f = self.patch_url(api)
        response = await self.client.post(url=f, json=params)
        return response.json()

    def get(self, api: str = '', params_dict: Optional[Dict] = None):
        return self.loop.run_until_complete(self._get(api, params_dict))

    def post(self, api: str = '', params_dict: Optional[Dict] = None):
        return self.loop.run_until_complete(self._post(api, params_dict))
