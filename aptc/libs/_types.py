from typing import Union, Optional

from ..sdk_impl import AccountAddress

Address = Union[str, AccountAddress]
TXHash = Union[str, AccountAddress]
IntNumber = Union[int, str]
OptionalIntNumber = Optional[IntNumber]

