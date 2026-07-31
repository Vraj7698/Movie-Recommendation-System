import streamlit as st


def render_header():
    st.markdown(
        """
        <style>
        .hero-header {
            position: relative;
            overflow: hidden;
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            border-radius: 18px;
            # border: 1px solid rgba(245, 197, 24, 0.45);

            background:
                linear-gradient(
                    rgba(5, 8, 15, 0.35),
                    rgba(5, 8, 15, 0.65)
                ),
                url("");

            background-size: cover;
            background-position: center;
            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.55),
                inset 0 0 25px rgba(0, 0, 0, 0.2);
        }
            background-size: 400% 400%;
            box-shadow:
                0 20px 55px rgba(0, 0, 0, 0.55),
                inset 0 0 35px rgba(255, 255, 255, 0.04);
            animation: heroBackground 9s ease infinite;
        }

        .hero-header::before {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(245, 197, 24, 0.2);
            filter: blur(65px);
            animation: heroGlow 5s ease-in-out infinite alternate;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            padding: 30px 20px;
            text-align: center;
        }

        .hero-title {
            margin: 0;
            color: #7DF9FF;
            font-size: clamp(40px);
            font-weight: 900;
            letter-spacing: 5px;
            text-transform: uppercase;


            text-shadow:
                0 2px 0 #CBD5E1,
                0 4px 0 #94A3B8,
                0 7px 0 #64748B,
                0 10px 18px rgba(0,0,0,.9),
                0 0 25px rgba(255,255,255,.8);

            animation: titleFloat 3s ease-in-out infinite;
        }
        .hero-subtitle {
            margin-top: 12px;
            color: #ffffff;
            font-size: clamp(12px, 1.5vw, 16px);
            font-weight: 600;
            letter-spacing: 1px;
            text-shadow: 0 3px 10px rgba(0, 0, 0, 1);
        }

        @keyframes heroBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes heroGlow {
            from { transform: translateX(-170px); }
            to { transform: translateX(170px); }
        }

        @keyframes titleFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }

        @media (max-width: 700px) {
            .hero-header {
                min-height: 175px;
            }

            .hero-title {
                letter-spacing: 3px;
            }
        }
        </style>

        <div class="hero-header">
            <div class="hero-content">
                <h1 class="hero-title">CINEVERSE</h1>
                <div class="hero-subtitle">
                    Discover Movies • Trailers • Cast • Streaming
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )