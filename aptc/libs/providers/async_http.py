import asyncio

import httpx
import urllib3

from ._base import BaseProvider


# [WIP]
class HttpxAsyncProvider(BaseProvider):
    """Asynchronous REST provider based on httpx.AsyncClient."""

    def __init__(self, base_url: str, api_key: str | None = None):
        super().__init__(base_url)
        assert base_url is not None or "", "url is required"
        self.base_parsed_url = urllib3.util.parse_url(base_url)
        self.base_url = self.base_parsed_url.url
        self.headers = dict(self.DEFAULT_HEADERS)
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.AsyncClient(headers=self.headers)
        self.loop = asyncio.new_event_loop()

    async def close(self):
        await self.client.aclose()

    def __del__(self):
        try:
            if self.loop.is_closed():
                return
            self.loop.run_until_complete(self.close())
            self.loop.close()
        except Exception:
            pass

    async def _get(self, api: str = "", params: dict | None = None):
        f = self.patch_url(api)
        response = await self.client.get(url=f, params=params)
        return response.json()

    async def _post(self, api: str = "", params: dict | None = None):
        f = self.patch_url(api)
        response = await self.client.post(url=f, json=params)
        return response.json()

    def get(self, api: str = "", params_dict: dict | None = None):
        return self.loop.run_until_complete(self._get(api, params_dict))

    def post(self, api: str = "", params_dict: dict | None = None):
        return self.loop.run_until_complete(self._post(api, params_dict))
