#!/usr/bin/env python3

__author__ = "xi"
__all__ = [
    "APIInfo",
    "api",
    "get",
    "post",
    "list_api_info",
]

from dataclasses import dataclass, field
from typing import Any, Callable, List, Literal, Mapping, Optional, Tuple

API_INFO = "__api_info__"


@dataclass
class APIInfo:
    method: str = field()
    path: str = field()
    stream_delimiter: str = field()
    stream_prefix: str = field()
    extra_info: Mapping[str, Any] = field(default_factory=dict)


def api(
        method: Literal["GET", "POST"] = "POST",
        path: Optional[str] = None,
        stream_delimiter: str = "\n\n",
        stream_prefix: str = None,
        **kwargs
) -> Callable:
    def _api(fn: Callable):
        _path = path
        if _path is None:
            if not hasattr(fn, "__name__"):
                raise RuntimeError("At least one of \"path\" or \"fn.__name__\" should be given.")
            name = getattr(fn, "__name__")
            _path = "/" + name

        setattr(fn, API_INFO, APIInfo(
            method=method,
            path=_path,
            stream_delimiter=stream_delimiter,
            stream_prefix=stream_prefix,
            extra_info=kwargs
        ))
        return fn

    return _api


def get(
        path: Optional[str] = None,
        stream_delimiter: str = "\n\n",
        stream_prefix: str = None,
        **kwargs
) -> Callable:
    return api(
        method="GET",
        path=path,
        stream_delimiter=stream_delimiter,
        stream_prefix=stream_prefix,
        **kwargs
    )


def post(
        path: Optional[str] = None,
        stream_delimiter: str = "\n\n",
        stream_prefix: str = None,
        **kwargs
) -> Callable:
    return api(
        method="POST",
        path=path,
        stream_delimiter=stream_delimiter,
        stream_prefix=stream_prefix,
        **kwargs
    )


def list_api_info(obj) -> List[Tuple[Callable, APIInfo]]:
    api_list = []
    for name in dir(obj):
        fn = getattr(obj, name)
        if not callable(fn):
            continue
        if not hasattr(fn, API_INFO):
            continue
        api_info = getattr(fn, API_INFO)
        api_list.append((fn, api_info))
    return api_list
