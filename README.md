# 🎬 CineVerse - Movie Recommendation System

<p align="center">

<img src="YOUR_LOGO_OR_BANNER_IMAGE_LINK" width="800"/>

</p>

<h3 align="center">
Discover Movies • Watch Trailers • Explore Cast • Get Smart Recommendations
</h3>

<p align="center">

A Netflix-style movie discovery platform built using Machine Learning, FastAPI, Streamlit, and TMDB API.

</p>

---

# 🌐 Live Demo

🚀 Website:

https://cineverse-movies.streamlit.app/

---

# 🎥 Project Demo Video

Add your project demonstration video here:

[▶ Watch CineVerse Demo](YOUR_VIDEO_LINK)

---

# 📌 About The Project

**CineVerse** is a movie recommendation and exploration platform that helps users discover movies, view details, explore cast information, watch trailers, and find similar movies using Machine Learning.

The project combines:

* Machine Learning based recommendation system
* TMDB movie data
* FastAPI backend services
* Streamlit interactive frontend
* User authentication system

The goal of this project is to create a modern movie platform similar to Netflix/IMDb where users can explore entertainment content easily.

---

# ✨ Features

## 🎬 Movie Discovery

* Trending movies
* Popular movies
* Top rated movies
* Upcoming movies
* Genre-based exploration

## 🤖 Movie Recommendation System

Implemented content-based recommendation using:

* TF-IDF Vectorization
* Cosine Similarity
* Movie metadata analysis

Users can get similar movie recommendations based on their selected movie.

## 🎭 Movie Details

Users can explore:

* Movie posters
* Ratings
* Overview
* Release date
* Genres
* Runtime
* Cast information
* Actor details

## 🎞 Trailer Integration

* Watch movie trailers
* Integrated with movie video data

## 📺 Streaming Platform Information

Shows available streaming providers:

* Netflix
* Amazon Prime Video
* JioHotstar
* SonyLIV
* ZEE5
* Apple TV+

## 👤 User Authentication

Implemented:

* User registration
* Login system
* Profile management
* Session handling

---

# 🖼 Screenshots

## 🏠 Home Page

<img src="YOUR_HOME_SCREENSHOT_LINK" width="900">

## 🎬 Movie Details Page

<img src="YOUR_MOVIE_DETAILS_SCREENSHOT_LINK" width="900">

## 🔎 Recommendation Section

<img src="YOUR_RECOMMENDATION_SCREENSHOT_LINK" width="900">

---

# 🏗 System Architecture

```
                 User

                  |
                  |

          Streamlit Frontend

                  |

                  |

             FastAPI Backend

                  |

        ---------------------

        |                   |

     TMDB API        ML Recommendation

                            |

                     Movie Dataset

                            |

                  Similarity Model

                  (similarity.pkl)

```

---

# 🛠 Tech Stack

## Frontend

* Streamlit
* HTML
* CSS
* JavaScript

## Backend

* FastAPI
* Python

## Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* TF-IDF Vectorizer
* Cosine Similarity

## Database

* SQL Database
* User Authentication Storage

## APIs

* TMDB API

## Deployment

* Streamlit Cloud
* GitHub

---

# 📂 Project Structure

```
Movie-Recommendation-System/

│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── movie_api/
│
│   ├── tmdb.py
│   ├── routes.py
│
│
├── models/
│
│   ├── similarity.pkl
│   └── movies_list.pkl
│
│
├── assets/
│
│   ├── images/
│   └── videos/
│
│
└── .env

```

---

# ⚙️ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Movie-Recommendation-System.git
```

## Go To Project Folder

```bash
cd Movie-Recommendation-System
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Add Environment Variables

Create `.env` file:

```
TMDB_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

---

## Run Application

Start Streamlit:

```bash
streamlit run app.py
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

---

# 🔌 API Endpoints

## Movie Details

```
GET /movie/{movie_id}
```

## Movie Cast

```
GET /movie/{movie_id}/cast
```

## Movie Images

```
GET /movie/{movie_id}/images
```

## Watch Providers

```
GET /movie/{movie_id}/watch-providers
```

---

# 🧠 Machine Learning Workflow

```
Movie Dataset

      |

Data Cleaning

      |

Feature Extraction

      |

TF-IDF Vectorization

      |

Cosine Similarity

      |

Movie Recommendation

```

---

# 🚀 Future Improvements

* Next.js frontend migration
* PostgreSQL database integration
* JWT authentication
* Personalized recommendations
* AI movie assistant chatbot
* Advanced search system
* Mobile responsive UI
* SEO optimization
* Custom domain integration

---

# 👨‍💻 Developer

**Vraj Patel**

Computer Engineering Student

Skills:

* Python
* Machine Learning
* FastAPI
* Streamlit
* SQL
* Data Science

---

# ⭐ If You Like This Project

Give this repository a ⭐ on GitHub.

Your support motivates further development!

---

# 📜 License

This project is developed for educational and portfolio purposes.
