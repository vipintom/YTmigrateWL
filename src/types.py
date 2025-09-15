# src/types.py
from typing import List, Optional, TypedDict


class FlatVideoInfo(TypedDict):
    id: str
    title: str
    url: str


class FlatPlaylistInfo(TypedDict):
    entries: List[Optional[FlatVideoInfo]]
