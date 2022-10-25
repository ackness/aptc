import itertools
from abc import abstractmethod
from typing import List, Union


class BaseProvider:
    DEFAULT_HEADERS = {"Content-Type": "application/json"}

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = None

    def patch_url(self, extra: Union[List[str], str]):
        f = ''
        if isinstance(extra, str):
            f = extra
        elif isinstance(extra, List):
            f = '/'.join(extra)
        return f'{self.base_url}{f}' if self.base_url.endswith('/') else f'{self.base_url}/{f}'

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def _get(self, *args, **kwargs):
        pass

    @abstractmethod
    def _post(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs):
        pass
