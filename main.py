import os      # file paths & environment variables
import pickle  #load saved ML data (df, tfidf, etc.)
import requests
from typing import Optional, List, Dict, Any, Tuple 

import numpy as np  # data handling
import pandas as pd # data handling
import httpx  # async API calls (to TMDB)
from fastapi import FastAPI, HTTPException, Query  # backend framework
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # response models (clean JSON structure)
from dotenv import load_dotenv



#.env, cors and path config
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

if not TMDB_API_KEY:
    # Don't crash import-time in production if you prefer; but for you better fail early:
    raise RuntimeError("TMDB_API_KEY missing. Put it in .env as TMDB_API_KEY=xxxx")

# -------------------------------------------------------------------------------------------------------
# -> FASTAPI APP

# Creates your backend server.

app = FastAPI(title="Movie Recommender API", version="3.0")
# Allows frontend (like Streamlit) to call this API.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------------------------------------

# PICKLE GLOBALS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "df.pkl")  # movie dataset
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl") # mapping (title → index)
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl") # ML similarity matrix
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl") # vectorizer

#  Loaded later when server starts.

df: Optional[pd.DataFrame] = None
indices_obj: Any = None
tfidf_matrix: Any = None
tfidf_obj: Any = None

TITLE_TO_IDX: Optional[Dict[str, int]] = None
#---------------------------------------------------------------------------------------------------

# MODELS
# Why important?
# They define how API responses look.

# small movie card (poster, title)

class TMDBMovieCard(BaseModel):
    tmdb_id: int
    title: str
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None

# full details

class TMDBMovieDetails(BaseModel):
    tmdb_id: int
    title: str
    overview: Optional[str] = None
    release_date: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    genres: List[dict] = []
#----------------------------------------------------------
    vote_average: Optional[float] = None
    runtime: Optional[int] = None
#----------------------------------------------------------
class CastMember(BaseModel):
    id: int
    name: str
    character: str | None = None
    profile_url: str | None = None

#----------------------------------------------------------


class TMDBPersonDetails(BaseModel):
    id: int
    name: str
    biography: Optional[str] = None
    birthday: Optional[str] = None
    place_of_birth: Optional[str] = None
    profile_url: Optional[str] = None
    known_for_department: Optional[str] = None

class MovieImage(BaseModel):
    file_url: str

def tmdb_person_details(person_id: int) -> TMDBPersonDetails:
    url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Person details not found"
        )

    data = response.json()

    return TMDBPersonDetails(
        id=data.get("id"),
        name=data.get("name", "Unknown"),
        biography=data.get("biography"),
        birthday=data.get("birthday"),
        place_of_birth=data.get("place_of_birth"),
        profile_url=make_img_url(data.get("profile_path")),
        known_for_department=data.get("known_for_department")
    )
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class PersonMovie(BaseModel):
    tmdb_id: int
    title: str
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
#----------------------------------------------------------


# ML recommendation

class TFIDFRecItem(BaseModel):
    title: str
    score: float
    tmdb: Optional[TMDBMovieCard] = None

# combined response

class SearchBundleResponse(BaseModel):
    query: str
    movie_details: TMDBMovieDetails
    tfidf_recommendations: List[TFIDFRecItem]
    genre_recommendations: List[TMDBMovieCard]

# This keeps API clean, structured, predictable

# ------------------------------------------------------------------------------------------------------------------

# UTILS

# (A) Normalize title
# title
def _norm_title(t: str) -> str:
    return str(t).strip().lower()

#img

# (B) Image URL builder
# Converts TMDB image path → full URL

def make_img_url(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"

# (c) TMDB API CALL (VERY IMPORTANT)

async def tmdb_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safe TMDB GET:
    - Network errors -> 502
    - TMDB API errors -> 502 with detail
    """
    q = dict(params)
    q["api_key"] = TMDB_API_KEY

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(f"{TMDB_BASE}{path}", params=q)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"TMDB request error: {type(e).__name__} | {repr(e)}",
        )

    if r.status_code != 200:
        raise HTTPException(
            status_code=502, detail=f"TMDB error {r.status_code}: {r.text}"
        )

    return r.json()

# (d) Convert TMDB → Movie Cards
# Converts raw API data → clean objects

#canvert a card 

async def tmdb_cards_from_results(
    results: List[dict], limit: int = 20
) -> List[TMDBMovieCard]:
    out: List[TMDBMovieCard] = []
    for m in (results or [])[:limit]:
        out.append(
            TMDBMovieCard(
                tmdb_id=int(m["id"]),
                title=m.get("title") or m.get("name") or "",
                poster_url=make_img_url(m.get("poster_path")),
                release_date=m.get("release_date"),
                vote_average=m.get("vote_average"),
            )
        )
    return out

# (e) Movie Details
# Gets full info:

# title
# overview
# poster
# genres

#movie detelis
async def tmdb_movie_details(movie_id: int) -> TMDBMovieDetails:
    data = await tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})
    return TMDBMovieDetails(
        tmdb_id=int(data["id"]),
        title=data.get("title") or "",
        overview=data.get("overview"),
        release_date=data.get("release_date"),
        poster_url=make_img_url(data.get("poster_path")),
        backdrop_url=make_img_url(data.get("backdrop_path")),
        genres=data.get("genres", []) or [],
#-------------------------------------------------------
        vote_average=data.get("vote_average"),
        runtime=data.get("runtime"),
    )
#-------------------------------------------------------

def tmdb_movie_images(tmdb_id: int) -> list[MovieImage]:
    url = (
        f"https://api.themoviedb.org/3/movie/{tmdb_id}/images"
        f"?api_key={TMDB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Movie images not found"
        )

    data = response.json()
    backdrops = data.get("backdrops", [])

    images = []

    for backdrop in backdrops[:5]:
        file_path = backdrop.get("file_path")

        if file_path:
            images.append(
                MovieImage(
                    file_url=make_img_url(file_path)
                )
            )

    return images
#-------------------------------------------------------

def tmdb_movie_cast(tmdb_id: int):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unable to fetch movie cast"
        )

    data = response.json()
    cast_list = []

    for actor in data.get("cast", [])[:12]:
        profile_path = actor.get("profile_path")

        profile_url = (
            f"https://image.tmdb.org/t/p/w500{profile_path}"
            if profile_path
            else None
        )

        cast_list.append(
            CastMember(
                id=actor.get("id"),
                name=actor.get("name", "Unknown"),
                character=actor.get("character"),
                profile_url=profile_url
            )
        )

    return cast_list

#-------------------------------------------------------
# def tmdb_movie_images
# (f) Search Movies
# Returns list of movies from TMDB

async def tmdb_search_movies(query: str, page: int = 1) -> Dict[str, Any]:
    """
    Raw TMDB response for keyword search (MULTIPLE results).
    Streamlit will use this for suggestions and grid.
    """
    return await tmdb_get(
        "/search/movie",
        {
            "query": query,
            "include_adult": "false",
            "language": "en-US",
            "page": page,
        },
    )

#search movie
async def tmdb_search_first(query: str) -> Optional[dict]:
    data = await tmdb_search_movies(query=query, page=1)
    results = data.get("results", [])
    return results[0] if results else None

# -----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------

def tmdb_person_movies(person_id: int) -> list[PersonMovie]:
    url = (
        f"https://api.themoviedb.org/3/person/{person_id}/movie_credits"
        f"?api_key={TMDB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Person movies not found"
        )

    data = response.json()
    cast_movies = data.get("cast", [])

    # Popular movies पहले दिखेंगी
    sorted_movies = sorted(
        cast_movies,
        key=lambda movie: movie.get("popularity", 0),
        reverse=True
    )

    movies: list[PersonMovie] = []
    seen_movie_ids = set()

    for movie in sorted_movies:
        movie_id = movie.get("id")

        # Duplicate या invalid movie को skip करें
        if not movie_id or movie_id in seen_movie_ids:
            continue

        seen_movie_ids.add(movie_id)

        title = movie.get("title") or movie.get("original_title")

        if not title:
            continue

        movies.append(
            PersonMovie(
                tmdb_id=movie_id,
                title=title,
                poster_url=make_img_url(movie.get("poster_path")),
                release_date=movie.get("release_date")
            )
        )

    return movies

# -----------------------------------------------------------------------------------------------------------------------


# TF-IDF Helpers

# (a) Build title → index map

# Converts:

# title → row index in matrix
def build_title_to_idx_map(indices: Any) -> Dict[str, int]:
    """
    indices.pkl can be:
    - dict(title -> index)
    - pandas Series (index=title, value=index)
    We normalize into TITLE_TO_IDX.
    """
    title_to_idx: Dict[str, int] = {}

    if isinstance(indices, dict):
        for k, v in indices.items():
            title_to_idx[_norm_title(k)] = int(v)
        return title_to_idx

    # pandas Series or similar mapping
    try:
        for k, v in indices.items():
            title_to_idx[_norm_title(k)] = int(v)
        return title_to_idx
    except Exception:
        # last resort: if it's a list-like etc.
        raise RuntimeError(
            "indices.pkl must be dict or pandas Series-like (with .items())"
        )

# (b) Get index by title

# Finds movie in dataset

def get_local_idx_by_title(title: str) -> int:
    global TITLE_TO_IDX
    if TITLE_TO_IDX is None:
        raise HTTPException(status_code=500, detail="TF-IDF index map not initialized")
    key = _norm_title(title)
    if key in TITLE_TO_IDX:
        return int(TITLE_TO_IDX[key])
    raise HTTPException(
        status_code=404, detail=f"Title not found in local dataset: '{title}'"
    )

# (c) Recommendation Logic (MAIN ML)

# Steps:
#       Find movie index
#       Get its TF-IDF vector
#       Compute similarity:

def tfidf_recommend_titles(
    query_title: str, top_n: int = 10
) -> List[Tuple[str, float]]:
    """
    Returns list of (title, score) from local df using cosine similarity on TF-IDF matrix.
    Safe against missing columns/rows.
    """
    global df, tfidf_matrix
    if df is None or tfidf_matrix is None:
        raise HTTPException(status_code=500, detail="TF-IDF resources not loaded")

    idx = get_local_idx_by_title(query_title)

    # query vector
    qv = tfidf_matrix[idx]
    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    # sort descending
    order = np.argsort(-scores)

    out: List[Tuple[str, float]] = []
    for i in order:
        if int(i) == int(idx):
            continue
        try:
            title_i = str(df.iloc[int(i)]["title"])
        except Exception:
            continue
        out.append((title_i, float(scores[int(i)])))
        if len(out) >= top_n:
            break
    return out

# (d) Attach TMDB Poster

# Adds poster/info to ML results

async def attach_tmdb_card_by_title(title: str) -> Optional[TMDBMovieCard]:
    """
    Uses TMDB search by title to fetch poster for a local title.
    If not found, returns None (never crashes the endpoint).
    """
    try:
        m = await tmdb_search_first(title)
        if not m:
            return None
        return TMDBMovieCard(
            tmdb_id=int(m["id"]),
            title=m.get("title") or title,
            poster_url=make_img_url(m.get("poster_path")),
            release_date=m.get("release_date"),
            vote_average=m.get("vote_average"),
        )
    except Exception:
        return None
    
# ---------------------------------------------------------------------------------------------------------------------------------

# STARTUP: LOAD PICKLES

#   STARTUP EVENT
@app.on_event("startup")
def load_pickles():
    global df, indices_obj, tfidf_matrix, tfidf_obj, TITLE_TO_IDX

    # Load df.pkl
    with open("models/df.pkl", "rb") as f:
        df = pickle.load(f)

    # Load indices.pkl
    with open("models/indices.pkl", "rb") as f:
        indices_obj = pickle.load(f)

    # Load TF-IDF matrix
    with open("models/tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)

    # Load TF-IDF vectorizer
    with open("models/tfidf.pkl", "rb") as f:
        tfidf_obj = pickle.load(f)

    # Build normalized map
    TITLE_TO_IDX = build_title_to_idx_map(indices_obj)

    # sanity check
    if df is None or "title" not in df.columns:
        raise RuntimeError(
            "df.pkl must contain a DataFrame with a 'title' column"
        )


# ------------------------------------------------------------------------------------------------------------------------------------

# ROUTES

# 1. Health Check

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- HOME FEED (TMDB) ----------
@app.get("/home", response_model=List[TMDBMovieCard])
async def home(
    category: str = Query("popular"),
    limit: int = Query(24, ge=1, le=50),
):
    """
    Home feed for Streamlit (posters).
    category:
      - trending (trending/movie/day)
      - popular, top_rated, upcoming, now_playing  (movie/{category})
    """
    try:
        if category == "trending":
            data = await tmdb_get("/trending/movie/day", {"language": "en-US"})
            return await tmdb_cards_from_results(data.get("results", []), limit=limit)

        if category not in {"popular", "top_rated", "upcoming", "now_playing"}:
            raise HTTPException(status_code=400, detail="Invalid category")

        data = await tmdb_get(f"/movie/{category}", {"language": "en-US", "page": 1})
        return await tmdb_cards_from_results(data.get("results", []), limit=limit)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Home route failed: {e}")


# ---------- TMDB KEYWORD SEARCH (MULTIPLE RESULTS) ----------
@app.get("/tmdb/search")
async def tmdb_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1, le=10),
):
    """
    Returns RAW TMDB shape with 'results' list.
    Streamlit will use it for:
      - dropdown suggestions
      - grid results
    """
    return await tmdb_search_movies(query=query, page=page)


# ---------- MOVIE DETAILS (SAFE ROUTE) ----------
@app.get(
    "/movie/id/{tmdb_id}",
    response_model=TMDBMovieDetails
)
async def movie_details_route(tmdb_id: int):
    return await tmdb_movie_details(tmdb_id)


@app.get(
    "/movie/id/{tmdb_id}/cast",
    response_model=list[CastMember]
)
def movie_cast_route(tmdb_id: int):
    return tmdb_movie_cast(tmdb_id)

@app.get("/person/{person_id}", response_model=TMDBPersonDetails)
def get_person_details(person_id: int):
    return tmdb_person_details(person_id)


@app.get("/person/{person_id}/movies", response_model=list[PersonMovie])
def get_person_movies(person_id: int):
    return tmdb_person_movies(person_id)

@app.get(
    "/movie/id/{tmdb_id}/images",
    response_model=list[MovieImage]
)
 
def get_movie_images(tmdb_id: int):
    return tmdb_movie_images(tmdb_id)

@app.get("/movie/id/{tmdb_id}/watch-providers")
def get_movie_watch_providers(tmdb_id: int):
    return tmdb_movie_watch_providers(tmdb_id)

def tmdb_movie_watch_providers(tmdb_id: int) -> list[dict]:
    url = (
        f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers"
        f"?api_key={TMDB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="TMDB watch providers API failed"
        )

    data = response.json()
    results = data.get("results", {})

    region_data = results.get("IN")

    if not region_data:
        region_data = results.get("US")

    if not region_data and results:
        region_data = next(iter(results.values()))

    if not region_data:
        return []

    providers = []
    seen_provider_ids = set()

    for provider_type in ["flatrate", "rent", "buy"]:
        provider_list = region_data.get(provider_type, [])

        for provider in provider_list:
            provider_id = provider.get("provider_id")

            if not provider_id or provider_id in seen_provider_ids:
                continue

            seen_provider_ids.add(provider_id)

            providers.append(
                {
                    "provider_id": provider_id,
                    "provider_name": provider.get(
                        "provider_name",
                        "Unknown Provider"
                    ),
                    "logo_url": make_img_url(
                        provider.get("logo_path")
                    ),
                    "provider_type": provider_type
                }
            )

    return providers


# नया function — बिल्कुल बाहर
def tmdb_provider_movies(provider_id: int) -> list[dict]:
    url = (
        "https://api.themoviedb.org/3/discover/movie"
        f"?api_key={TMDB_API_KEY}"
        f"&with_watch_providers={provider_id}"
        "&watch_region=IN"
        "&sort_by=popularity.desc"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    movies = []

    for movie in data.get("results", [])[:20]:
        movies.append(
            {
                "tmdb_id": movie.get("id"),
                "title": movie.get("title"),
                "poster_url": make_img_url(
                    movie.get("poster_path")
                ),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
            }
        )

    return movies


def tmdb_trending_people() -> list[dict]:
    url = (
        "https://api.themoviedb.org/3/trending/person/week"
        f"?api_key={TMDB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    people = []

    for person in data.get("results", [])[:12]:
        profile_path = person.get("profile_path")

        people.append(
            {
                "person_id": person.get("id"),
                "name": person.get("name", "Unknown"),
                "profile_url": (
                    make_img_url(profile_path)
                    if profile_path else None
                ),
                "department": person.get(
                    "known_for_department",
                    "Unknown"
                ),
                "popularity": person.get("popularity"),
            }
        )

    return people

    #-------------------------------------------------------------------

def tmdb_trending_trailers() -> list[dict]:
    url = (
        "https://api.themoviedb.org/3/trending/movie/week"
        f"?api_key={TMDB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    trailers = []

    for movie in data.get("results", [])[:4]:
        movie_id = movie.get("id")

        video_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
            f"?api_key={TMDB_API_KEY}"
        )

        video_response = requests.get(video_url, timeout=10)

        if video_response.status_code != 200:
            continue

        video_data = video_response.json()

        trailer_key = None

        for video in video_data.get("results", []):
            if (
                video.get("site") == "YouTube"
                and video.get("type") in ["Trailer", "Teaser"]
            ):
                trailer_key = video.get("key")
                break

        if not trailer_key:
            continue

        trailers.append(
            {
                "tmdb_id": movie_id,
                "title": movie.get("title", "Unknown Movie"),
                "overview": movie.get("overview"),
                "backdrop_url": make_img_url(
                    movie.get("backdrop_path")
                ),
                "poster_url": make_img_url(
                    movie.get("poster_path")
                ),
                "trailer_url": (
                    f"https://www.youtube.com/watch?v={trailer_key}"
                ),
                "rating": movie.get("vote_average"),
            }
        )

    return trailers

    #-------------------------------------------------------------------

@app.get("/trailers/trending")
def get_trending_trailers():
    return tmdb_trending_trailers()

@app.get("/provider/{provider_id}/movies")
def get_provider_movies(provider_id: int):
    return tmdb_provider_movies(provider_id)

@app.get("/people/trending")
def get_trending_people():
    return tmdb_trending_people()

    
# ---------- GENRE RECOMMENDATIONS ----------
@app.get("/recommend/genre", response_model=List[TMDBMovieCard])
async def recommend_genre(
    tmdb_id: int = Query(...),
    limit: int = Query(18, ge=1, le=50),
):
    """
    Given a TMDB movie ID:
    - fetch details
    - pick first genre
    - discover movies in that genre (popular)
    """
    details = await tmdb_movie_details(tmdb_id)
    if not details.genres:
        return []

    genre_id = details.genres[0]["id"]
    discover = await tmdb_get(
        "/discover/movie",
        {
            "with_genres": genre_id,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1,
        },
    )
    cards = await tmdb_cards_from_results(discover.get("results", []), limit=limit)
    return [c for c in cards if c.tmdb_id != tmdb_id]


# ---------- TF-IDF ONLY (debug/useful) ----------
@app.get("/recommend/tfidf")
async def recommend_tfidf(
    title: str = Query(..., min_length=1),
    top_n: int = Query(10, ge=1, le=50),
):
    recs = tfidf_recommend_titles(title, top_n=top_n)
    return [{"title": t, "score": s} for t, s in recs]


# ---------- BUNDLE: Details + TF-IDF recs + Genre recs ----------
@app.get("/movie/search", response_model=SearchBundleResponse)
async def search_bundle(
    query: str = Query(..., min_length=1),
    tfidf_top_n: int = Query(12, ge=1, le=30),
    genre_limit: int = Query(12, ge=1, le=30),
):
    """
    This endpoint is for when you have a selected movie and want:
      - movie details       
      - TF-IDF recommendations (local) + posters
      - Genre recommendations (TMDB) + posters

    NOTE:
    - It selects the BEST match from TMDB for the given query.
    - If you want MULTIPLE matches, use /tmdb/search
    """
    best = await tmdb_search_first(query)
    if not best:
        raise HTTPException(
            status_code=404, detail=f"No TMDB movie found for query: {query}"
        )

    tmdb_id = int(best["id"])
    details = await tmdb_movie_details(tmdb_id)

    # 1) TF-IDF recommendations (never crash endpoint)
    tfidf_items: List[TFIDFRecItem] = []

    recs: List[Tuple[str, float]] = []
    try:
        # try local dataset by TMDB title
        recs = tfidf_recommend_titles(details.title, top_n=tfidf_top_n)
    except Exception:
        # fallback to user query
        try:
            recs = tfidf_recommend_titles(query, top_n=tfidf_top_n)
        except Exception:
            recs = []

    for title, score in recs:
        card = await attach_tmdb_card_by_title(title)
        tfidf_items.append(TFIDFRecItem(title=title, score=score, tmdb=card))

    # 2) Genre recommendations (TMDB discover by first genre)
    genre_recs: List[TMDBMovieCard] = []
    if details.genres:
        genre_id = details.genres[0]["id"]
        discover = await tmdb_get(
            "/discover/movie",
            {
                "with_genres": genre_id,
                "language": "en-US",
                "sort_by": "popularity.desc",
                "page": 1,
            },
        )
        cards = await tmdb_cards_from_results(
            discover.get("results", []), limit=genre_limit
        )
        genre_recs = [c for c in cards if c.tmdb_id != details.tmdb_id]

    return SearchBundleResponse(
        query=query,
        movie_details=details,
        tfidf_recommendations=tfidf_items,
        genre_recommendations=genre_recs,
    )



# This is your complete system

# It returns:

# 🎬 Movie Details
# 🧠 TF-IDF Recommendations
# 🎭 Genre Recommendations

