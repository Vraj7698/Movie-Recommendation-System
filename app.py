import requests
import streamlit as st

st.set_page_config(
    page_title="CINEVERSE",
    page_icon="🎬",
    layout="wide"
)

from movie_api import fetch_trailer
import html
import streamlit.components.v1 as components
import json
# from trailer_ui import render_trailer_component
from trailer_ui_v2 import (
    render_trailer_home,
    render_related_videos,
)
from search_component import render_imdb_search
from header import render_header
from styles import inject_styles
from login.auth import (
    login,
    signup,
    get_user,
    add_favorite,
    get_favorites,
    remove_favorite
)
from login.database import create_tables
from login.login_styles import inject_login_styles
from streamlit_js_eval import streamlit_js_eval




# st.write("TEST QUERY:", st.query_params)

create_tables()

# -----------------------------
# Responsive Layout
# -----------------------------
from streamlit_js_eval import streamlit_js_eval

if "screen_width" not in st.session_state:
    st.session_state.screen_width = 1400

screen_width = streamlit_js_eval(
    js_expressions="window.innerWidth",
    key="SCREEN_WIDTH",
)

if screen_width:
    st.session_state.screen_width = screen_width

if st.session_state.screen_width >= 1200:
    GRID_COLS = 5
elif st.session_state.screen_width >= 768:
    GRID_COLS = 3
else:
    GRID_COLS = 2


# -----------------------------
# Session Initialization
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "email" not in st.session_state:
    st.session_state.email = ""


# -----------------------------
# Restore Login From URL
# -----------------------------

if "logged_in" in st.query_params:

    if st.query_params["logged_in"] == "true":

        st.session_state.logged_in = True

        st.session_state.username = st.query_params.get("username", "")
        st.session_state.email = st.query_params.get("email", "")

        if isinstance(st.session_state.username, list):
            st.session_state.username = st.session_state.username[0]

        if isinstance(st.session_state.email, list):
            st.session_state.email = st.session_state.email[0]
# -----------------------------
# Restore View
# -----------------------------

if "view" not in st.session_state:

    st.session_state.view = st.query_params.get(
        "view",
        "home"
    )

# -----------------------------
# LOGIN PAGE
# -----------------------------



if not st.session_state.logged_in:

    inject_login_styles()

    st.markdown(
        """
        <div class="login-title">
            CINEVERSE
        </div>

        <div class="login-subtitle">
            Discover Movies • Trailers • Cast • Streaming
        </div>
        """,
        unsafe_allow_html=True
    )


    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Signup"]
    )


    with tab1:

        st.subheader("Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        remember_me = st.checkbox(
            "Remember Me"
        )


        if st.button(
            "Login",
            use_container_width=True
        ):

            success, result = login(
                login_email,
                login_password
            )


            if success:

                st.session_state.logged_in = True

                st.session_state.username = result["username"]

                st.session_state.email = result["email"]

                # Save Login State In URL

                st.query_params.clear()

                st.query_params.update(
                    {
                        "logged_in": "true",
                        "username": result["username"],
                        "email": result["email"],
                        "view": "home"
                    }
                )

                

                st.session_state.view = "home"




                if remember_me:

                    st.session_state.remember_me = True


                st.success(
                    "Login Successful ✅"
                )

                st.rerun()


            else:

                st.error(result)



    with tab2:

        st.subheader(
            "Create Account"
        )


        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Create Account",
            use_container_width=True
        ):

            success, message = signup(
                username,
                email,
                password
            )


            if success:

                st.success(message)

            else:

                st.error(message)


    st.stop()
# -----------------------------------------------------------------------------------
# CONFIG
# the FastAPI backend endpoint (deployed or local)
# API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
# API_BASE = "http://127.0.0.1:8000"
# API_BASE = "http://127.0.0.1:8001"


# base URL for movie posters
API_BASE = "https://movie-recommender-app-spyz.onrender.com"

# st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

inject_styles()

# -----------------------------
# Login Session
# -----------------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "username" not in st.session_state:
#     st.session_state.username = ""

# st.markdown("""
#     <style>

#     .block-container {
#         max-width: 1600px;
#         padding-top: 1.2rem;
#         padding-left: 2rem;
#         padding-right: 2rem;
#         padding-bottom: 3rem;
#     }

#     [data-testid="stAppViewContainer"] {
#         background-image: url("https://4kwallpapers.com/images/walls/thumbs_3t/25454.jpg");
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }

#     [data-testid="stHeader"] {
#         background: transparent;
#     }

#     hr {
#         border-color: rgba(255, 255, 255, 0.12);
#     }

#     @media (max-width: 700px) {
#         .block-container {
#             padding-left: 0.8rem;
#             padding-right: 0.8rem;
#         }
#     }

#     </style>
#     """, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------------------------------------\

# STYLES (minimal modern)

# Adds minimal modern styles for:
#                                Cards
#                                Movie title truncation
#                                 Muted text
# Gives a clean, app-like look
st.markdown(
    """


<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.small-muted {
    color: #6b7280;
    font-size: 0.92rem;
}

.movie-title {
    font-size: 0.9rem;
    line-height: 1.15rem;
    height: 2.3rem;
    overflow: hidden;
}

.card {
    # border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 14px;
    background: transparent;
}

.stream-title {
    font-size: 1rem;
    font-weight: 700;
    min-height: 48px;
    margin-top: 8px;
    margin-bottom: 10px;
}

div.stButton > button {
    border-radius: 24px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------------------------------------------------------------------

# STATE + ROUTING (single-file pages)

# "home" → search + home feed
# "details" → movie details
if "view" not in st.session_state:
    st.session_state.view = st.query_params.get(
        "view",
        "home"
    )

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

if "selected_person_id" not in st.session_state:
    st.session_state.selected_person_id = None

if "selected_trailer_id" not in st.session_state:
    st.session_state.selected_trailer_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details", "person", "trailer", "profile", "mylist"):
    st.session_state.view = qp_view

if qp_id and qp_view != "profile":
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except (TypeError, ValueError):
        pass

qp_person_id = st.query_params.get("person_id")

if qp_view == "person" and qp_person_id:
    try:
        st.session_state.selected_person_id = int(qp_person_id)
        st.session_state.selected_tmdb_id = None
        st.session_state.view = "person"
    except (TypeError, ValueError):
        pass

qp_trailer_id = st.query_params.get("trailer_id")

if qp_view == "trailer" and qp_trailer_id:
    try:
        st.session_state.selected_trailer_id = int(qp_trailer_id)
        st.session_state.view = "trailer"
    except (TypeError, ValueError):
        pass


# Navigation helpers:

def goto_home():
    st.session_state.view = "home"

    st.query_params["view"] = "home"

    st.session_state.selected_tmdb_id = None
    st.session_state.selected_person_id = None
    st.session_state.selected_trailer_id = None

    st.query_params["view"] = "home"

    for key in ["id", "person_id", "trailer_id"]:
        if key in st.query_params:
            del st.query_params[key]

    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()

def goto_trailer(tmdb_id: int):
    st.session_state.selected_trailer_id = int(tmdb_id)
    st.session_state.view = "trailer"

    st.query_params["view"] = "trailer"
    st.query_params["trailer_id"] = str(int(tmdb_id))

    if "id" in st.query_params:
        del st.query_params["id"]

    if "person_id" in st.query_params:
        del st.query_params["person_id"]

    st.rerun()

def goto_profile():
    st.session_state.view = "profile"

    st.query_params["view"] = "profile"

    for key in ["id", "person_id", "trailer_id"]:
        if key in st.query_params:
            del st.query_params[key]

    st.rerun()


def goto_mylist():
    st.session_state.view = "mylist"

    st.query_params["view"] = "mylist"

    for key in ["id", "person_id", "trailer_id"]:
        if key in st.query_params:
            del st.query_params[key]

    st.rerun()
# --------------------------------------------------------------------------------------------------------------------------------------------

# API HELPERS

# alls backend with requests.get
# Returns JSON data or error
# Cached for 30 seconds for autocomplete speed

@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"

@st.cache_data(ttl=300)
def fetch_provider_movies(provider_id: int):
    data, err = api_get_json(
        f"/provider/{provider_id}/movies"
    )

    if err:
        st.error(err)
        return []

    return data or []


@st.cache_data(ttl=300)
def fetch_trending_people():
    data, err = api_get_json("/people/trending")

    if err:
        st.error(err)
        return []

    return data or []
@st.cache_data(ttl=300)
def fetch_trending_trailers():
    data, err = api_get_json("/trailers/trending")

    if err:
        st.error(err)
        return []

    return data or []


# 5.POSTER GRID
# 6. PARSING TMDB RESULTS

def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(
                        poster,
                        width=250
                    )
                else:
                    st.write("🖼️ No poster")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# ----------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]

def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards
# -----------------------------------------------------------------------------------------------------------------------------------------

# HEADER

#  App title + instructions

# st.title("🍿 Movie Recommender")
# st.markdown(
#     "<div class='small-muted'>Type keyword → dropdown suggestions + matching results → open → details + recommendations</div>",
#     unsafe_allow_html=True,
# )
# st.divider()
# render_header()

# ==========================================================
# HEADER
# ==========================================================

render_header()

# Username
st.markdown(
    f"<div style='text-align:right;font-size:16px;'>👋 {st.session_state.username}</div>",
    unsafe_allow_html=True
)

st.divider()

# ==========================================================
# TOP MENU
# ==========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    if st.button(
        "🏠 Home",
        key="menu_home",
        use_container_width=True
    ):
        goto_home()

with m2:
    if st.button(
        "❤️ My List",
        key="menu_mylist",
        use_container_width=True
    ):
        goto_mylist()

with m3:
    if st.button(
        "👤 Profile",
        key="menu_profile",
        use_container_width=True
    ):
        goto_profile()

with m4:
    if st.button(
        "🚪 Logout",
        key="menu_logout",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.email = ""
        st.query_params.clear()
        st.session_state.view = "home"
        st.rerun()

st.divider()
# ------------------------------------------------------------------------------------------------------------------------------------------------

# VIEW: HOME

# Search Mode:
#             Text input for keyword
#             Calls /tmdb/search endpoint
#             Parses results via parse_tmdb_search_to_cards

# st.write("Current View =", st.session_state.view)

if st.session_state.view == "home":
    # Trailer carousel index URL से लो
    try:
        trailer_slide = int(
            st.query_params.get("trailer_slide", 0)
        )
    except (TypeError, ValueError):
        trailer_slide = 0

    st.session_state.trailer_carousel_index = trailer_slide
    
    search_event = render_imdb_search(
        API_BASE,
        placeholder="Search movies, actors, TV shows...",
        key="movie_search",
    )

    # Process each custom-component event only once.
    if search_event:
        event_id = search_event.get("event_id")
        if event_id and st.session_state.get("_last_search_event") != event_id:
            st.session_state._last_search_event = event_id

            if search_event.get("action") == "open":
                selected_id = search_event.get("tmdb_id")
                if selected_id:
                    goto_details(int(selected_id))

            elif search_event.get("action") == "search":
                query = str(search_event.get("query") or "").strip()
                if query:
                    data, search_err = api_get_json(
                        "/tmdb/search",
                        params={"query": query},
                    )
                    if search_err or data is None:
                        st.error(f"Search failed: {search_err}")
                    else:
                        suggestions, cards = parse_tmdb_search_to_cards(
                            data, query, limit=24
                        )
                        st.markdown("### Results")
                        poster_grid(
                            cards,
                            cols=6,
                            key_prefix="custom_search_results",
                        )
                    st.stop()

    st.divider()

    # HOME FEED MODE
    # st.markdown(f"### 🏠 Home — {home_category.replace('_',' ').title()}")
    # st.markdown("### 🏠 Home")
    st.markdown("### 🏠 Home — Trending")

    home_cards, err = api_get_json(
        # "/home", params={"category": home_category, "limit": 24}
        "/home", params={"category": "trending", "limit": 15}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()


    # poster_grid(home_cards, cols=5, key_prefix="home_feed")
    poster_grid(home_cards, cols=GRID_COLS, key_prefix="home_feed")


        # ---------------------------------------------------------
    # Trending Trailers
    # ---------------------------------------------------------

    st.divider()
    st.subheader("🎬 Trending Trailers")

    trailers = fetch_trending_trailers()

    if trailers:
        render_trailer_home(
            st,
            trailers
        )
    else:
        st.info("No trending trailers found.")
 

   
    # ---------------------------------------------------------
    # Explore What's Streaming
    # ---------------------------------------------------------

    st.divider()
    st.subheader("🎬 Explore What's Streaming")

    PROVIDERS = {
        "Prime Video": 119,
        "Netflix": 8,
        "JioHotstar": 122,
        "SonyLIV": 237,
        "ZEE5": 232,
        "Apple TV+": 350,
    }

    provider_name = st.radio(
        "Choose streaming service",
        list(PROVIDERS.keys()),
        horizontal=True
    )

    provider_id = PROVIDERS[provider_name]

    provider_movies = fetch_provider_movies(provider_id)

    if not provider_movies:
        st.info(f"No movies available for {provider_name}.")

    else:
        # movie_columns = st.columns(5)
        movie_columns = st.columns(GRID_COLS)

        for index, movie in enumerate(provider_movies[:10]):
            # with movie_columns[index % 5]:
            with movie_columns[index % len(movie_columns)]:
                poster_url = movie.get("poster_url")
                title = movie.get("title", "Unknown Movie")
                rating = movie.get("rating")
                movie_tmdb_id = movie.get("tmdb_id")

                if poster_url:
                    st.image(
                        poster_url,
                        width=250
                    )
                else:
                    st.info("No poster")

                if rating is not None:
                    st.markdown(f"⭐ **{rating:.1f}**")
                else:
                    st.markdown("⭐ **N/A**")

                st.markdown(
                    f"<div class='stream-title'>{title}</div>",
                    unsafe_allow_html=True
                )

                if movie_tmdb_id:
                    if st.button(
                        "🎟️ Watch Now",
                        key=f"watch_{provider_id}_{movie_tmdb_id}_{index}",
                        use_container_width=True
                    ):
                        goto_details(movie_tmdb_id)

                    if st.button(
                        "▶ Trailer",
                        key=f"trailer_{provider_id}_{movie_tmdb_id}_{index}",
                        use_container_width=True
                    ):
                        trailer_url = fetch_trailer(movie_tmdb_id)

                        if trailer_url:
                            st.link_button(
                                "Open Trailer",
                                trailer_url,
                                use_container_width=True
                            )
                        else:
                            st.warning("Trailer unavailable.")

     # ---------------------------------------------------------
    # Trending People
    # ---------------------------------------------------------

    st.markdown(
    """
    <style>
    .person-photo-box {
        width: 100%;
        height: 327px;
        overflow: hidden;
        background: #19324a;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        box-sizing: border-box;
    }

    .person-photo-box img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .person-photo-box.no-photo {
        background: #19324a;
    }
    </style>
    """,
        unsafe_allow_html=True
    )

    
    st.divider()
    st.subheader("🔥 Trending People")

    people = fetch_trending_people()

    if people:
        cols = st.columns(6)

        for index, person in enumerate(people[:6]):
            with cols[index]:
                profile_url = person.get("profile_url")
                person_name = person.get("name", "Unknown")
                department = person.get("department", "Unknown")
                person_id = person.get("person_id")
                popularity = person.get("popularity") or 0

                if profile_url:
                    person_image_html = f"""
                    <div class="person-photo-box">
                        <img src="{profile_url}" alt="{person_name}">
                    </div>
                    """
                else:
                    person_image_html = """
                    <div class="person-photo-box no-photo">
                        No Photo
                    </div>
                    """

                st.markdown(
                    person_image_html,
                    unsafe_allow_html=True
                )

                if person_id and st.button(
                    "Open Profile",
                    key=f"photo_click_{person_id}",
                    use_container_width=True
                ):
                    st.session_state.selected_person_id = person_id
                    st.session_state.selected_tmdb_id = None
                    st.session_state.view = "person"

                    st.query_params["view"] = "person"
                    st.query_params["person_id"] = str(person_id)

                    if "id" in st.query_params:
                        del st.query_params["id"]

                    st.rerun()

                st.markdown(f"### {index + 1}")
                st.caption(f"▲ {popularity:.1f}")
                st.markdown(f"**{person_name}**")
                st.caption(department)

    else:
        st.info("No trending people found.")

    # ---------------------------------------------------------
    # Trending People
    # ---------------------------------------------------------
# Steps:
#        1)Fetch movie details
#                 /movie/id/{tmdb_id}
#         2)Display poster + info
#                 Poster left, details right

#                 Shows title, release date, genres, overview
#         3)Backdrop image
#                 Optional, full-width if exists
#         4)Recommendations
#                Fetch /movie/search bundle
#                      TF-IDF similarmovie_columns = st.columns(6) movies
#                      Genre-based recommendations
#                 Display as poster grids
#         5)Fallback
#                If bundle fails → only genre recommendations

elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home", use_container_width=False):
            goto_home()
        st.stop()

    # Details-page-only styling. Unique class names avoid conflicts with poster grids.
    st.markdown(
        """
        <style>
        .details-page-title {
            margin: 0;
            font-size: clamp(2.25rem, 4.7vw, 4.8rem);
            line-height: 1.02;
            font-weight: 900;
            letter-spacing: -0.055em;
            color: #ffffff;
            text-shadow: 0 5px 26px rgba(0,0,0,.78);
        }
        .details-kicker {
            color: #78efff;
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .18em;
            text-transform: uppercase;
            margin-bottom: .65rem;
        }
        .details-meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin: 1.05rem 0 1.2rem;
        }
        .details-pill {
            display: inline-flex;
            align-items: center;
            gap: .38rem;
            min-height: 34px;
            padding: .42rem .78rem;
            border: 1px solid rgba(122,239,255,.30);
            border-radius: 999px;
            background: rgba(4,16,30,.72);
            color: #eafcff;
            font-size: .88rem;
            font-weight: 650;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
        }
        .details-rating {
            border-color: rgba(255,210,70,.46);
            color: #ffe47d;
            background: rgba(52,39,5,.62);
        }
        .details-overview-card {
            margin-top: .5rem;
            padding: 1.2rem 1.3rem;
            border: 1px solid rgba(122,239,255,.19);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(8,22,39,.86), rgba(4,10,21,.78));
            box-shadow: 0 16px 42px rgba(0,0,0,.30);
            backdrop-filter: blur(12px);
        }
        .details-overview-label {
            margin-bottom: .55rem;
            color: #78efff;
            font-size: .78rem;
            font-weight: 850;
            letter-spacing: .14em;
            text-transform: uppercase;
        }
        .details-overview-text {
            color: #e8f0fa;
            font-size: 1.03rem;
            line-height: 1.78;
        }
        .details-poster-shell {
            padding: .55rem;
            border: 1px solid rgba(122,239,255,.25);
            border-radius: 22px;
            background: linear-gradient(145deg, rgba(13,31,51,.88), rgba(3,8,18,.90));
            box-shadow: 0 24px 65px rgba(0,0,0,.55), 0 0 30px rgba(0,229,255,.07);
        }
        .details-section-title {
            margin: 2.2rem 0 1.05rem;
            padding-bottom: .7rem;
            border-bottom: 1px solid rgba(255,255,255,.13);
            color: #fff;
            font-size: 1.55rem;
            font-weight: 850;
        }
        .details-section-title::after {
            content: "";
            display: block;
            width: 72px;
            height: 3px;
            margin-top: .72rem;
            border-radius: 999px;
            background: linear-gradient(90deg,#00e5ff,transparent);
        }
        .cast-card {
            min-height: 104px;
            margin: .35rem 0 .8rem;
            padding: .75rem;
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 14px;
            background: rgba(5,14,27,.70);
        }
        .cast-name {
            margin-top: .2rem;
            color: #fff;
            font-weight: 800;
            line-height: 1.25;
        }
        .cast-role {
            margin-top: .2rem;
            color: #9fb0c6;
            font-size: .82rem;
            line-height: 1.35;
        }
        .provider-card {
            min-height: 126px;
            padding: .9rem .7rem;
            text-align: center;
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 15px;
            background: rgba(5,14,27,.72);
        }
        .provider-name {
            margin-top: .5rem;
            color: #fff;
            font-weight: 750;
            font-size: .9rem;
        }
        .provider-type {
            color: #8fa4bd;
            font-size: .76rem;
            text-transform: capitalize;
        }
        [data-testid="stAppViewContainer"] {
            background-image:
                linear-gradient(rgba(2,6,17,.77), rgba(2,6,17,.93)),
                url("https://4kwallpapers.com/images/walls/thumbs_3t/25454.jpg") !important;
            background-size: cover !important;
            background-position: center top !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .block-container {
            max-width: 1500px !important;
            padding-top: 1.25rem !important;
            padding-left: 2.2rem !important;
            padding-right: 2.2rem !important;
        }
        @media (max-width: 800px) {
            .block-container { padding-left: .85rem !important; padding-right: .85rem !important; }
            .details-page-title { font-size: 2.4rem; }
            .details-overview-text { font-size: .95rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([5, 1.25])
    with top_left:
        st.markdown("<div class='details-kicker'>Cineverse • Movie details</div>", unsafe_allow_html=True)
    with top_right:
        if st.button("← Back to Home", key="details_back_home", use_container_width=True):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    title = str(data.get("title") or "Untitled")
    release = str(data.get("release_date") or "N/A")
    release_year = release[:4] if release and release != "N/A" else "N/A"
    overview = str(data.get("overview") or "No overview available.")
    genres = ", ".join(
        str(g.get("name")) for g in (data.get("genres") or []) if g.get("name")
    ) or "Genre unavailable"

    rating = data.get("vote_average")
    rating_text = f"{float(rating):.1f}/10" if rating is not None else "N/A"

    runtime = data.get("runtime")
    if runtime:
        runtime = int(runtime)
        hours, minutes = divmod(runtime, 60)
        runtime_text = f"{hours} hr {minutes} min" if hours else f"{minutes} min"
    else:
        runtime_text = "N/A"

    safe_title = html.escape(title)
    safe_genres = html.escape(genres)
    safe_overview = html.escape(overview)
    safe_release = html.escape(release)

    poster_col, info_col = st.columns([1, 2.45], gap="large")

    with poster_col:
        st.markdown("<div class='details-poster-shell'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], width=250)
        else:
            st.info("Poster unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

        favorites = get_favorites(st.session_state.email)

        favorite_ids = [movie[0] for movie in favorites]

        if tmdb_id in favorite_ids:

            if st.button("💔 Remove from My List", use_container_width=True):

                remove_favorite(
                    st.session_state.email,
                    tmdb_id
                )

                st.success("Removed from My List")
                st.rerun()

        else:

            if st.button("❤️ Add to My List", use_container_width=True):

                add_favorite(
                    st.session_state.email,
                    tmdb_id,
                    title,
                    data.get("poster_url")
                )

                st.success("Added to My List")
                st.rerun()

        trailer_url = fetch_trailer(tmdb_id)
        if trailer_url:
            st.link_button("▶ Watch Trailer", trailer_url, use_container_width=True)
        else:
            st.button("Trailer unavailable", disabled=True, use_container_width=True)

    with info_col:
        st.markdown(
            f"""
            <h1 class="details-page-title">{safe_title}</h1>
            <div class="details-meta-row">
                <span class="details-pill details-rating">⭐ {rating_text}</span>
                <span class="details-pill">📅 {safe_release}</span>
                <span class="details-pill">⏱ {runtime_text}</span>
                <span class="details-pill">🎭 {safe_genres}</span>
            </div>
            <div class="details-overview-card">
                <div class="details-overview-label">Overview</div>
                <div class="details-overview-text">{safe_overview}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if data.get("backdrop_url"):
            st.image(data["backdrop_url"], width=900)

    # CAST
    st.markdown("<div class='details-section-title'>👥 Cast</div>", unsafe_allow_html=True)
    cast_data, cast_err = api_get_json(f"/movie/id/{tmdb_id}/cast")

    if cast_err:
        st.warning(f"Cast could not be loaded: {cast_err}")
    elif cast_data:
        cast_columns = st.columns(6)
        for index, actor in enumerate(cast_data[:12]):
            with cast_columns[index % 6]:
                profile_url = actor.get("profile_url")
                actor_name = str(actor.get("name") or "Unknown")
                character_name = str(actor.get("character") or "Unknown character")
                actor_id = actor.get("id")

                if profile_url:
                    st.image(profile_url, width=250)
                else:
                    st.markdown(
                        "<div class='person-photo-box no-photo'>No Photo</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div class="cast-card">
                        <div class="cast-name">{html.escape(actor_name)}</div>
                        <div class="cast-role">as {html.escape(character_name)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if actor_id and st.button(
                    "View Profile",
                    key=f"details_person_{actor_id}_{index}",
                    use_container_width=True,
                ):
                    st.session_state.selected_person_id = int(actor_id)
                    st.session_state.selected_tmdb_id = None
                    st.session_state.view = "person"
                    st.query_params["view"] = "person"
                    st.query_params["person_id"] = str(actor_id)
                    if "id" in st.query_params:
                        del st.query_params["id"]
                    st.rerun()
    else:
        st.info("Cast information is not available.")

    # BACKDROPS
    images, images_err = api_get_json(f"/movie/id/{tmdb_id}/images")
    if images:
        st.markdown("<div class='details-section-title'>🖼 Backdrops</div>", unsafe_allow_html=True)
        backdrop_cols = st.columns(5)
        for index, image_item in enumerate(images[:5]):
            file_url = image_item.get("file_url")
            if file_url:
                with backdrop_cols[index]:
                    st.image(file_url, width=250)
    elif images_err:
        st.warning(f"Backdrops could not be loaded: {images_err}")

    # WATCH PROVIDERS
    providers, providers_err = api_get_json(f"/movie/id/{tmdb_id}/watch-providers")
    st.markdown("<div class='details-section-title'>📺 Where to Watch</div>", unsafe_allow_html=True)

    if providers_err:
        st.warning(f"Watch providers could not be loaded: {providers_err}")
    elif providers:
        provider_columns = st.columns(min(len(providers), 6))
        for index, provider in enumerate(providers):
            with provider_columns[index % len(provider_columns)]:
                logo_url = provider.get("logo_url")
                provider_name = str(provider.get("provider_name") or "Unknown provider")
                provider_type = str(provider.get("provider_type") or "Available")

                if logo_url:
                    st.image(logo_url, width=250)
                st.markdown(
                    f"""
                    <div class="provider-card">
                        <div class="provider-name">{html.escape(provider_name)}</div>
                        <div class="provider-type">{html.escape(provider_type)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Watch providers are not available for this movie.")

    # RECOMMENDATIONS
    st.markdown("<div class='details-section-title'>✨ Recommendations</div>", unsafe_allow_html=True)

    if title.strip():
        bundle, bundle_err = api_get_json(
            "/movie/search",
            params={"query": title.strip(), "tfidf_top_n": 10, "genre_limit": 10},
        )

        if not bundle_err and bundle:
            st.markdown("#### 🔎 Similar Movies")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=5,
                key_prefix="details_tfidf",
            )

            st.markdown("#### 🎭 More Like This")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=5,
                key_prefix="details_genre",
            )
        else:
            genre_only, genre_err = api_get_json(
                "/recommend/genre",
                params={"tmdb_id": tmdb_id, "limit": 15},
            )
            if not genre_err and genre_only:
                poster_grid(
                    genre_only,
                    cols=5,
                    key_prefix="details_genre_fallback",
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")

#==============================================================================
elif st.session_state.view == "person":
    person_id = st.session_state.selected_person_id

    if person_id is None:
        st.error("Person ID not found.")

        # if st.button("← Back to Movie Details"):
        if st.button("← Back to Home"):
             goto_home()
            # st.session_state.view = "details"
            # st.rerun()

    else:
        try:
            person_response = requests.get(
                f"{API_BASE}/person/{person_id}",
                timeout=10
            )

            movies_response = requests.get(
                f"{API_BASE}/person/{person_id}/movies",
                timeout=10
            )

            if person_response.status_code != 200:
                st.error("Person details load नहीं हुईं.")

            else:
                person = person_response.json()

                # if st.button("← Back to Movie Details"):
                #     st.session_state.view = "details"
                #     st.session_state.selected_person_id = None
                #     st.rerun()
                if st.button("← Back to Home"):
                     goto_home()



                st.title(person.get("name", "Person Details"))

                profile_col, info_col = st.columns([1, 2])

                with profile_col:
                    profile_url = person.get("profile_url")

                    if profile_url:
                        st.image(
                            profile_url,
                            width=250
                        )
                    else:
                        st.info("Profile image available नहीं है.")

                with info_col:
                    department = person.get("known_for_department")
                    birthday = person.get("birthday")
                    place_of_birth = person.get("place_of_birth")

                    if department:
                        st.write(f"**Known for:** {department}")

                    if birthday:
                        st.write(f"**Birthday:** {birthday}")

                    if place_of_birth:
                        st.write(
                            f"**Place of Birth:** {place_of_birth}"
                        )

                    st.subheader("Biography")

                    biography = person.get("biography")

                    if biography:
                        st.write(biography)
                    else:
                        st.info("Biography available नहीं है.")

                st.divider()
                st.subheader("Movies")

                if movies_response.status_code != 200:
                    st.error("Person movies load नहीं हुईं.")

                else:
                    movies = movies_response.json()

                    if not movies:
                        st.info("इस actor की movies नहीं मिलीं.")

                    else:
                        # movie_columns = st.columns(5)
                        movie_columns = st.columns(GRID_COLS)

                        for index, movie in enumerate(movies[:10]):
                            # with movie_columns[index % 5]:
                            with movie_columns[index % len(movie_columns)]:
                                poster_url = movie.get("poster_url")
                                movie_title = movie.get(
                                    "title",
                                    "Unknown Movie"
                                )

                                if poster_url:
                                    st.image(
                                        poster_url,
                                        width=250
                                    )
                                else:
                                    st.info("No poster")

                                st.caption(movie_title)

                                release_date = movie.get("release_date")

                                if release_date:
                                    st.caption(release_date)

                                movie_id = movie.get("tmdb_id")

                                if st.button(
                                    "View Movie",
                                    key=f"person_movie_{movie_id}"
                                ):
                                    st.session_state.selected_tmdb_id = (
                                        movie_id
                                    )
                                    st.session_state.view = "details"
                                    st.session_state.selected_person_id = None
                                    st.rerun()

        except requests.exceptions.RequestException as error:
            st.error(f"Backend connection error: {error}")


#=============================================================================

elif st.session_state.view == "profile":

    left, center, right = st.columns([1, 10, 1])

    with center:
        if st.button(
            "← Back to Home",
            key="profile_back_home",
            use_container_width=True
        ):
            goto_home()


    st.title("👤 My Profile")

    user = get_user(st.session_state.email)
    favorites = get_favorites(st.session_state.email)

    avatar_col, info_col = st.columns([1, 4])

    with avatar_col:

        profile_image = (
            "https://ui-avatars.com/api/?name="
            + st.session_state.username
            + "&background=0D8ABC&color=fff&size=256"
        )

        st.image(
        "https://ui-avatars.com/api/?name=vraj&background=0D8ABC&color=fff&size=256",
        width=150
    )


    with info_col:

        st.markdown(
            f"""
            <h2 style="margin-bottom:5px;">
            {st.session_state.username}
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            f"📧 {st.session_state.email}"
        )

    if user:

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"""
👤 Username

**{user[0]}**
"""
            )

            st.info(
                f"""
📧 Email

**{user[1]}**
"""
            )

        with col2:
            st.success(
                f"""
📅 Account Created

**{user[2]}**
"""
            )

            st.success(
                f"""
❤️ Favorite Movies

**{len(favorites)}**
"""
            )

        # ==========================
        # Profile Statistics
        # ==========================
        st.divider()

        stat1, stat2, stat3, stat4 = st.columns(4)

        with stat1:
            st.metric(
                "❤️ Favorites",
                len(favorites)
            )

        with stat2:
            st.metric(
                "🎬 Movies Viewed",
                len(favorites)   # Temporary
            )

        with stat3:
            st.metric(
                "⭐ Member Since",
                user[2][:10]
            )

        with stat4:
            st.metric(
                "👤 Username",
                user[0]
            )

        # ==========================
        # Recent Favorite Movies
        # ==========================
        st.divider()

        st.subheader("🎬 Recent Favorite Movies")

        if favorites:

            # cols = st.columns(5)
            cols = st.columns(GRID_COLS)

            for index, movie in enumerate(favorites[:5]):

                movie_id = movie[0]
                movie_title = movie[1]
                poster = movie[2]

                # with cols[index % 5]:
                with cols[index % len(cols)]:

                    if poster:
                        st.image(
                            poster,
                            width=250
                        )

                    st.caption(movie_title)

                    if st.button(
                        "🎬 Open",
                        key=f"profile_movie_{movie_id}"
                    ):
                        goto_details(movie_id)

        else:
            st.info("No favorite movies yet.")

        # ==========================
        # Quick Actions
        # ==========================
        st.divider()

        st.subheader("⚙️ Quick Actions")

        action1, action2, action3 = st.columns(3)

        with action1:
            if st.button(
                "❤️ My List",
                key="profile_quick_mylist",
                use_container_width=True
            ):
                goto_mylist()
        with action2:
            if st.button(
                "🏠 Home",
                key="profile_quick_home",
                use_container_width=True
            ):
                goto_home()

        with action3:
            if st.button(
                "🚪 Logout",
                key="profile_quick_logout",
                use_container_width=True
            ):

                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.email = ""

                st.query_params.clear()


                st.rerun()

    else:
        st.warning("User data not found.")

#=============================================================================

elif st.session_state.view == "mylist":

    if st.button(
        "← Back to Home",
        key="mylist_back_home",
        use_container_width=True
    ):
        goto_home()


    st.title("❤️ My List")

    if st.button("🏠 Back to Home"):
        goto_home()

    favorites = get_favorites(st.session_state.email)

    if not favorites:
        st.info("Your My List is empty.")
        st.stop()

    # cols = st.columns(5)
    cols = st.columns(GRID_COLS)

    for index, movie in enumerate(favorites):

        movie_id = movie[0]
        title = movie[1]
        poster = movie[2]

        # with cols[index % 5]:
        with cols[index % len(cols)]:

            if poster:
                st.image(poster, width=250)

            st.markdown(f"**{title}**")

            if st.button("🎬 Open", key=f"open_{movie_id}"):
                goto_details(movie_id)

            if st.button("🗑 Remove", key=f"remove_{movie_id}"):

                remove_favorite(
                    st.session_state.email,
                    movie_id
                )

                st.success("Removed Successfully")

                st.rerun()

#=============================================================================
elif st.session_state.view == "trailer":

    trailer_id = st.session_state.selected_trailer_id

    if not trailer_id:
        st.warning("Trailer not selected.")

        if st.button("← Back to Home"):
            goto_home()

        st.stop()

    trailers = fetch_trending_trailers()

    selected_trailer = next(
        (
            trailer
            for trailer in trailers
            if trailer.get("tmdb_id") == trailer_id
        ),
        None
    )

    if not selected_trailer:
        st.error("Trailer details not found.")

        if st.button("← Back to Home"):
            goto_home()

        st.stop()

    if st.button("✕ Close"):
        goto_home()

    video_col, info_col = st.columns(
        [3.2, 1.4],
        gap="large"
    )

    # LEFT SIDE VIDEO
    with video_col:
        trailer_url = selected_trailer.get("trailer_url")

        if trailer_url:
            st.video(trailer_url)
        else:
            st.info("Trailer unavailable.")

        # ---------------------------------------------------------
        # Trailer Reactions
        # ---------------------------------------------------------

        reaction_key = f"trailer_reactions_{trailer_id}"

        if reaction_key not in st.session_state:
            st.session_state[reaction_key] = {
                "like": 148,
                "dislike": 0,
                "love": 40,
                "clap": 14,
                "idea": 10,
                "happy": 14,
                "wow": 17,
            }

        reactions = st.session_state[reaction_key]

        reaction_cols = st.columns(7)

        with reaction_cols[0]:
            if st.button(
                f"👍 {reactions['like']}",
                key=f"like_{trailer_id}",
                use_container_width=True
            ):
                reactions["like"] += 1
                st.rerun()

        with reaction_cols[1]:
            if st.button(
                f"👎 {reactions['dislike']}",
                key=f"dislike_{trailer_id}",
                use_container_width=True
            ):
                reactions["dislike"] += 1
                st.rerun()

        with reaction_cols[2]:
            if st.button(
                f"❤️ {reactions['love']}",
                key=f"love_{trailer_id}",
                use_container_width=True
            ):
                reactions["love"] += 1
                st.rerun()

        with reaction_cols[3]:
            if st.button(
                f"👏 {reactions['clap']}",
                key=f"clap_{trailer_id}",
                use_container_width=True
            ):
                reactions["clap"] += 1
                st.rerun()

        with reaction_cols[4]:
            if st.button(
                f"💡 {reactions['idea']}",
                key=f"idea_{trailer_id}",
                use_container_width=True
            ):
                reactions["idea"] += 1
                st.rerun()

        with reaction_cols[5]:
            if st.button(
                f"😄 {reactions['happy']}",
                key=f"happy_{trailer_id}",
                use_container_width=True
            ):
                reactions["happy"] += 1
                st.rerun()

        with reaction_cols[6]:
            if st.button(
                f"🤩 {reactions['wow']}",
                key=f"wow_{trailer_id}",
                use_container_width=True
            ):
                reactions["wow"] += 1
                st.rerun()
        
        
    # RIGHT SIDE DETAILS
    with info_col:
        poster_col, title_col = st.columns([1, 2])

        with poster_col:
            poster_url = selected_trailer.get("poster_url")

            if poster_url:
                st.image(
                    poster_url,
                    width=250
                )

        with title_col:
            st.markdown(
                f"### {selected_trailer.get('title', 'Unknown Movie')}"
            )

            rating = selected_trailer.get("rating")

            if rating is not None:
                st.caption(f"⭐ {rating:.1f}/10")

            movie_id = selected_trailer.get("tmdb_id")

            if movie_id and st.button(
                "View Movie Details",
                key=f"trailer_movie_{movie_id}",
                use_container_width=True
            ):
                goto_details(movie_id)

        st.divider()
        st.markdown("## Trailer")

        overview = selected_trailer.get("overview")

        if overview:
            st.write(overview)
        else:
            st.info("Overview unavailable.")


    # # info_col के बाहर, function के अंदर
    # trailer_id = selected_trailer.get("tmdb_id")

    render_related_videos(
        st,
        trailers,
        trailer_id
    )