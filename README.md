# 🎬 CineVerse - Movie Recommendation System

<p align="center">
  <img src="/image/logo.png" width="200"/>
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python">

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi">

<img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit">

<img src="https://img.shields.io/badge/Machine%20Learning-TF--IDF-orange?style=for-the-badge">

<img src="https://img.shields.io/badge/TMDB-API-01B4E4?style=for-the-badge">

<img src="https://img.shields.io/github/stars/Vraj7698/Movie-Recommendation-System?style=for-the-badge">

</p>

<h3 align="center">
Discover Movies • Watch Trailers • Explore Cast • Get Smart Recommendations
</h3>

<p align="center">
A Netflix-style movie discovery platform built using Machine Learning, FastAPI, Streamlit, and TMDB API.
</p>

---

# 🌐 Live Demo

🚀 Website: https://cineverse-movies.streamlit.app/

---

# 🎥 Project Demo Video

Add My project demonstration video here:

[▶ Watch Demo Video](https://drive.google.com/drive/u/0/folders/1N0MYjkEI3Vei7wSeGRJQ4Kc61ifaF9Sx)
---

# 📌 About The Project

**CineVerse** is a movie recommendation and exploration platform that helps users discover movies, view details, explore cast information, watch trailers, and find similar movies using Machine Learning.

The project combines:

- Machine Learning based recommendation system
- TMDB movie data
- FastAPI backend services
- Streamlit interactive frontend
- User authentication system

The goal of this project is to create a modern movie platform similar to Netflix/IMDb where users can explore entertainment content easily.

---

# ✨ Features

## 🎬 Movie Discovery

- Trending movies
- Popular movies
- Top rated movies
- Upcoming movies
- Genre-based exploration

## 🤖 Movie Recommendation System

Implemented content-based recommendation using:

- TF-IDF Vectorization
- Cosine Similarity
- Movie metadata analysis

Users can get similar movie recommendations based on their selected movie.

## 🎭 Movie Details

Users can explore:

- Movie posters
- Ratings
- Overview
- Release date
- Genres
- Runtime
- Cast information
- Actor details

## 🎞 Trailer Integration

- Watch movie trailers
- Integrated with movie video data

## 📺 Streaming Platform Information

Shows available streaming providers:

- Netflix
- Amazon Prime Video
- JioHotstar
- SonyLIV
- ZEE5
- Apple TV+

## 👤 User Authentication

Implemented:

- User registration
- Login system
- Profile management
- Session handling

---

# 🖼 Screenshots

## 🏠 Home & Movie Discovery

<p align="center">
  <img src="/image/Home.png" width="45%">
  <img src="/image/trending.png" width="45%">
</p>

## 🎬 Movie Details & Recommendations

<p align="center">
  <img src="/image/movie_details.png" width="45%">
  <img src="/image/recommendation.png" width="45%">
</p>

## 👤 Authentication & Profile

<p align="center">
  <img src="/image/login.png" width="45%">
  <img src="/image/profile.png" width="45%">
</p>

---

# 🏗 System Architecture

<p align="center">
  <img src="/image/system_architecture.png" width="550">
</p>

---

# 🛠 Tech Stack

## Frontend

- Streamlit
- HTML
- CSS
- JavaScript

## Backend

- FastAPI
- Python

## Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- TF-IDF Vectorizer
- Cosine Similarity

## Database

- SQL Database
- User Authentication Storage

## APIs

- TMDB API

## Deployment

- Streamlit Cloud
- Render
- GitHub

---

# 📂 Project Structure

```text
Movie-Recommendation-System/

│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── movie_api/
│   ├── tmdb.py
│   └── routes.py
│
├── models/
│   ├── df.pkl
│   ├── indices.pkl
│   ├── tfidf.pkl
│   └── tfidf_matrix.pkl
│
├── image/
│   ├── logo.png
│   ├── Home.png
│   ├── movie_details.png
│   ├── login.png
│   ├── profile.png
│   ├── Demo_Video.mp4
│   └── ml_workflow.png
│
├── users.db
├── .gitignore
└── .env
```

---

# ⚙️ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/Vraj7698/Movie-Recommendation-System.git
```

## Go To Project Folder

```bash
cd Movie-Recommendation-System
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate Environment (Windows)

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

Create `.env`

```env
TMDB_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

---

## Run Application

Start Streamlit

```bash
streamlit run app.py
```

Start FastAPI

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

<p align="center">
  <img src="/image/ml_workflow.png" width="550">
</p>

---

# 🚀 Future Improvements

- Next.js frontend migration
- PostgreSQL database integration
- JWT authentication
- Personalized recommendations
- AI movie assistant chatbot
- Advanced search system
- Mobile responsive UI
- SEO optimization
- Custom domain integration

---

# 👨‍💻 Developer

**Vraj Patel**

Computer Engineering Student

### Skills

- Python
- Machine Learning
- FastAPI
- Streamlit
- SQL
- Data Science

---

# ⭐ If You Like This Project

Give this repository a ⭐ on GitHub.

Your support motivates further development!

---

# 📜 License

This project is developed for educational and portfolio purposes.