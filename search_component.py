from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit.components.v1 as components


_COMPONENT_DIR = (
    Path(__file__).parent
    / "search_component"
    / "frontend"
    / "build"
)

_imdb_search_component = components.declare_component(
    "imdb_movie_search_component",
    path=str(_COMPONENT_DIR),
)


def render_imdb_search(
    api_base: str,
    *,
    placeholder: str = "Search IMDb",
    key: str = "imdb_movie_search",
) -> dict[str, Any] | None:
    """Render the IMDb-style search component."""

    categories = [
        {"label": "All", "value": "all"},
        {"label": "Movies", "value": "movie"},
        {"label": "TV Shows", "value": "tv"},
        {"label": "People", "value": "person"},
    ]

    value = _imdb_search_component(
        api_base=api_base.rstrip("/"),
        placeholder=placeholder,
        categories=categories,
        default_category="all",
        key=key,
        default=None,
    )

    return value if isinstance(value, dict) else None