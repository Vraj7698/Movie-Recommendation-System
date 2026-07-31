# styles.py

import streamlit as st


def inject_styles():
    st.markdown(
        """
        <style>

        /* -------------------------------------------------
           WEBSITE BACKGROUND
        ------------------------------------------------- */

        html,
        body,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"] {
            background-color: #020611 !important;
        }

        [data-testid="stAppViewContainer"] {
            background-image:
                linear-gradient(
                    rgba(2, 6, 17, 0.76),
                    rgba(2, 6, 17, 0.90)
                ),
                url("https://4kwallpapers.com/images/walls/thumbs_3t/25454.jpg") !important;

            background-size: cover !important;
            background-position: center top !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }

        /* Streamlit top header transparent */
        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        /* -------------------------------------------------
           MAIN PAGE WIDTH
        ------------------------------------------------- */

        .block-container {
            width: 100% !important;
            max-width: 1450px !important;
            padding-top: 1.5rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 4rem !important;
        }

        /* -------------------------------------------------
           TEXT
        ------------------------------------------------- */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6,
        p,
        span,
        label {
            color: #ffffff;
        }

        /* -------------------------------------------------
           MOVIE DETAILS TOP SECTION
        ------------------------------------------------- */

        .movie-details-card {
            width: 100%;
            min-height: 430px;

            background:
                linear-gradient(
                    135deg,
                    rgba(10, 18, 35, 0.94),
                    rgba(5, 10, 22, 0.82)
                );

            border: 1px solid rgba(0, 229, 255, 0.28);
            border-radius: 22px;
            padding: 30px;

            box-shadow:
                0 18px 50px rgba(0, 0, 0, 0.55),
                0 0 25px rgba(0, 229, 255, 0.08);

            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
        }

        .movie-title {
            margin: 0 0 14px 0;

            font-size: clamp(34px, 4vw, 58px);
            line-height: 1.08;
            font-weight: 900;

            color: #ffffff;
            letter-spacing: -1px;

            text-shadow:
                0 4px 18px rgba(0, 0, 0, 0.85),
                0 0 20px rgba(0, 229, 255, 0.10);
        }

        .movie-meta {
            margin-top: 8px;
            margin-bottom: 12px;

            color: #cbd8ea;
            font-size: 16px;
            line-height: 1.8;
        }

        .movie-rating {
            display: inline-block;

            margin: 14px 0;
            padding: 9px 17px;

            border-radius: 999px;

            background: rgba(0, 229, 255, 0.12);
            border: 1px solid rgba(0, 229, 255, 0.55);

            color: #7df9ff;
            font-size: 18px;
            font-weight: 800;

            box-shadow: 0 0 18px rgba(0, 229, 255, 0.10);
        }

        .movie-overview {
            margin-top: 17px;

            color: #eef4ff;
            font-size: 17px;
            line-height: 1.75;
        }

        /* -------------------------------------------------
           POSTERS AND IMAGES
        ------------------------------------------------- */

        [data-testid="stImage"] img {
            border-radius: 16px !important;

            box-shadow:
                0 12px 30px rgba(0, 0, 0, 0.52),
                0 0 15px rgba(0, 229, 255, 0.08);

            transition:
                transform 0.22s ease,
                box-shadow 0.22s ease;
        }

        [data-testid="stImage"] img:hover {
            transform: translateY(-4px);

            box-shadow:
                0 18px 38px rgba(0, 0, 0, 0.62),
                0 0 22px rgba(0, 229, 255, 0.16);
        }

        /* -------------------------------------------------
           SECTION HEADINGS
        ------------------------------------------------- */

        .section-heading {
            margin-top: 38px;
            margin-bottom: 20px;
            padding-bottom: 11px;

            border-bottom: 1px solid rgba(255, 255, 255, 0.16);

            color: #ffffff;
            font-size: 27px;
            font-weight: 850;
        }

        .section-heading::after {
            content: "";
            display: block;

            width: 75px;
            height: 3px;

            margin-top: 10px;
            border-radius: 10px;

            background: linear-gradient(
                90deg,
                #00e5ff,
                transparent
            );
        }

        /* Normal Streamlit headings */
        h3 {
            margin-top: 28px !important;
            padding-bottom: 10px !important;

            border-bottom: 1px solid rgba(255, 255, 255, 0.14);

            font-size: 25px !important;
            font-weight: 800 !important;
        }

        h4 {
            font-size: 21px !important;
            font-weight: 800 !important;
        }

        /* -------------------------------------------------
           REMOVE OLD WHITE CARDS
        ------------------------------------------------- */

        .card {
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        /* -------------------------------------------------
           BUTTONS
        ------------------------------------------------- */

        div.stButton > button {
            width: 100%;
            min-height: 39px;

            border-radius: 10px;
            border: 1px solid rgba(0, 229, 255, 0.48);

            background:
                linear-gradient(
                    135deg,
                    rgba(11, 24, 43, 0.96),
                    rgba(4, 11, 24, 0.96)
                );

            color: #ffffff;
            font-weight: 700;

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease,
                box-shadow 0.2s ease;
        }

        div.stButton > button:hover {
            border-color: #00e5ff;
            color: #7df9ff;

            transform: translateY(-2px);

            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.38),
                0 0 16px rgba(0, 229, 255, 0.18);
        }

        div.stButton > button:active {
            transform: translateY(0);
        }

        /* -------------------------------------------------
           INFO / WARNING BOXES
        ------------------------------------------------- */

        [data-testid="stAlert"] {
            border-radius: 11px !important;
            border: 1px solid rgba(0, 229, 255, 0.16) !important;
            background: rgba(9, 25, 45, 0.88) !important;
        }

        /* -------------------------------------------------
           DIVIDERS
        ------------------------------------------------- */

        hr {
            border: none !important;
            border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
            margin-top: 25px !important;
            margin-bottom: 25px !important;
        }

        /* -------------------------------------------------
           MOBILE RESPONSIVE
        ------------------------------------------------- */

        @media (max-width: 900px) {

            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 1rem !important;
            }

            .movie-details-card {
                min-height: auto;
                padding: 21px;
            }

            .movie-title {
                font-size: 34px;
            }

            .movie-overview {
                font-size: 15px;
            }

            .section-heading {
                font-size: 23px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )