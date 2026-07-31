from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

_COMPONENT_DIR = Path(__file__).parent / "trailer_component" / "frontend" / "build"
_trailer_component = components.declare_component(
    "trailer_carousel_component",
    path=str(_COMPONENT_DIR),
)


def _safe(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _trailer_url(tmdb_id: Any) -> str:
    return f"?view=trailer&trailer_id={tmdb_id}"


def _rating_text(value: Any) -> str:
    try:
        return f"⭐ {float(value):.1f}/10" if value is not None else "⭐ N/A"
    except (TypeError, ValueError):
        return "⭐ N/A"


def _duration_text(item: dict[str, Any]) -> str:
    value = item.get("duration") or item.get("runtime") or ""
    if isinstance(value, (int, float)):
        return f"{int(value)} min"
    return str(value)


def render_trailer_home(
    st: Any,
    trailers: list[dict[str, Any]],
    state_key: str = "trailer_carousel_index",
) -> None:
    """IMDb-style carousel with no page rerun for slide changes.

    The custom component sends a TMDB id back to Python only when the user
    clicks the hero trailer. Arrow clicks, Up Next clicks and auto-slide stay
    entirely inside JavaScript, so they do not reload the Streamlit page.
    """
    valid = [item for item in trailers if item.get("tmdb_id")]
    if not valid:
        st.info("No trending trailers found.")
        return

    slides: list[dict[str, Any]] = []
    for item in valid:
        slides.append(
            {
                "tmdb_id": int(item["tmdb_id"]),
                "title": str(item.get("title") or "Unknown Movie"),
                "subtitle": str(
                    item.get("overview")
                    or item.get("original_title")
                    or "Watch the Trailer"
                ),
                "backdrop": str(
                    item.get("backdrop_url")
                    or item.get("poster_url")
                    or ""
                ),
                "poster": str(
                    item.get("poster_url")
                    or item.get("backdrop_url")
                    or ""
                ),
                "rating": _rating_text(item.get("rating")),
                "duration": _duration_text(item),
            }
        )

    selected_id = _trailer_component(
        slides=slides,
        start_index=int(st.session_state.get(state_key, 0) or 0),
        auto_slide_ms=5000,
        key="imdb_trailer_carousel",
        default=None,
    )

    if selected_id is None:
        return

    try:
        selected_id = int(selected_id)
    except (TypeError, ValueError):
        return

    # Prevent processing the same component value repeatedly after reruns.
    event_key = "_last_trailer_component_value"
    if st.session_state.get(event_key) == selected_id:
        return

    st.session_state[event_key] = selected_id
    st.session_state.selected_trailer_id = selected_id
    st.session_state.selected_tmdb_id = None
    st.session_state.selected_person_id = None
    st.session_state.view = "trailer"

    st.query_params["view"] = "trailer"
    st.query_params["trailer_id"] = str(selected_id)
    for key in ("id", "person_id", "trailer_slide"):
        if key in st.query_params:
            del st.query_params[key]

    st.rerun()


def render_related_videos(
    st: Any,
    related: list[dict[str, Any]],
    current_trailer_id: Any | None = None,
) -> None:
    """Render related trailers as an IMDb-style horizontal carousel.

    Only this section uses a small HTML component. The home trailer carousel
    and all other application code remain unchanged.
    """
    if not related:
        st.info("No related videos found.")
        return

    filtered = [
        item
        for item in related
        if item.get("tmdb_id") and item.get("tmdb_id") != current_trailer_id
    ]

    if not filtered:
        st.info("No related videos found.")
        return

    cards: list[dict[str, str]] = []
    for item in filtered[:10]:
        tmdb_id = item.get("tmdb_id")
        cards.append(
            {
                "title": str(item.get("title") or "Unknown Movie"),
                "image": str(
                    item.get("backdrop_url")
                    or item.get("poster_url")
                    or ""
                ),
                "rating": _rating_text(item.get("rating")),
                "duration": _duration_text(item),
                "url": _trailer_url(tmdb_id),
            }
        )

    import json

    cards_json = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")

    component_html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#000; font-family:Arial,Helvetica,sans-serif; overflow:hidden; }}
.related-wrap {{ position:relative; width:100%; padding:0 52px; }}
.related-track {{ display:flex; gap:18px; overflow-x:auto; scroll-behavior:smooth; scroll-snap-type:x mandatory; scrollbar-width:none; padding:4px 2px 12px; }}
.related-track::-webkit-scrollbar {{ display:none; }}
.related-card {{ flex:0 0 calc((100% - 36px)/3); min-width:280px; scroll-snap-align:start; text-decoration:none; color:#fff; border-radius:12px; overflow:hidden; background:#111827; box-shadow:0 4px 16px rgba(0,0,0,.25); }}
.thumb {{ position:relative; width:100%; aspect-ratio:16/9; overflow:hidden; background:#111; }}
.thumb img {{ width:100%; height:100%; object-fit:cover; display:block; transition:transform .25s ease; }}
.related-card:hover .thumb img {{ transform:scale(1.04); }}
.overlay {{ position:absolute; inset:0; background:linear-gradient(to top,rgba(0,0,0,.75),rgba(0,0,0,.08) 55%); }}
.play {{ position:absolute; left:16px; bottom:14px; width:46px; height:46px; display:flex; align-items:center; justify-content:center; border:3px solid #fff; border-radius:50%; background:rgba(0,0,0,.45); font-size:20px; padding-left:3px; }}
.duration {{ position:absolute; right:12px; bottom:12px; padding:5px 8px; border-radius:5px; background:rgba(0,0,0,.76); color:#fff; font-size:13px; }}
.card-body {{ padding:13px 14px 15px; }}
.card-title {{ min-height:44px; display:-webkit-box; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; font-size:17px; font-weight:750; line-height:1.28; }}
.card-meta {{ margin-top:9px; color:#facc15; font-size:14px; }}
.arrow {{ position:absolute; top:39%; z-index:5; width:42px; height:66px; transform:translateY(-50%); border:1px solid rgba(255,255,255,.65); border-radius:7px; background:rgba(0,0,0,.72); color:#fff; font-size:38px; line-height:1; cursor:pointer; }}
.arrow:hover {{ background:rgba(0,0,0,.92); }}
.prev {{ left:2px; }}
.next {{ right:2px; }}
@media (max-width:900px) {{ .related-card {{ flex-basis:calc((100% - 18px)/2); }} }}
@media (max-width:620px) {{ .related-wrap {{ padding:0 42px; }} .related-card {{ flex-basis:100%; min-width:240px; }} }}
</style>
</head>
<body>
<div class="related-wrap">
  <button class="arrow prev" id="relatedPrev" type="button" aria-label="Previous related trailers">‹</button>
  <div class="related-track" id="relatedTrack"></div>
  <button class="arrow next" id="relatedNext" type="button" aria-label="Next related trailers">›</button>
</div>
<script>
const cards = {cards_json};
const track = document.getElementById('relatedTrack');

function esc(value) {{
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}}

function parentUrl(relativeUrl) {{
  try {{
    const base = document.referrer || window.location.href;
    return new URL(relativeUrl, base).href;
  }} catch (error) {{
    return relativeUrl;
  }}
}}

cards.forEach((item) => {{
  const card = document.createElement('a');
  card.className = 'related-card';
  card.href = parentUrl(item.url);
  card.target = '_top';
  card.innerHTML = `
    <div class="thumb">
      <img src="${{esc(item.image)}}" alt="${{esc(item.title)}}">
      <div class="overlay"></div>
      <div class="play">▶</div>
      <div class="duration">${{esc(item.duration || '')}}</div>
    </div>
    <div class="card-body">
      <div class="card-title">${{esc(item.title)}}</div>
      <div class="card-meta">${{esc(item.rating)}}</div>
    </div>`;
  track.appendChild(card);
}});

function scrollAmount() {{
  const first = track.querySelector('.related-card');
  if (!first) return 320;
  return first.getBoundingClientRect().width + 18;
}}

document.getElementById('relatedPrev').addEventListener('click', () => {{
  track.scrollBy({{ left: -scrollAmount(), behavior: 'smooth' }});
}});

document.getElementById('relatedNext').addEventListener('click', () => {{
  track.scrollBy({{ left: scrollAmount(), behavior: 'smooth' }});
}});
</script>
</body>
</html>
"""

    st.markdown("#### Related Videos")
    components.html(component_html, height=330, scrolling=False)
