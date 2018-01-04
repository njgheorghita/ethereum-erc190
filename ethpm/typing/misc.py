from typing import (  # noqa: F401
    Any,
    Dict,
    NewType,
)

ContractName = NewType('ContractName', str)

URI = NewType('URI', str)


class CacheAttribute():
    cache = None  # type: Any


class MetafuncType():
    fixturenames = None  # type: Dict[Any, Any]
    config = None  # type: CacheAttribute
    parametrize = None  # type: Any
