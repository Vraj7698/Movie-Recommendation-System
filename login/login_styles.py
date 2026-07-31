import streamlit as st


def inject_login_styles():
    st.markdown(
        """
<style>

/* ===========================
   PAGE BACKGROUND
=========================== */

[data-testid="stAppViewContainer"]{

    background:
    linear-gradient(
        rgba(2,6,17,.75),
        rgba(2,6,17,.92)
    ),
    url("https://i.pinimg.com/736x/e5/98/4a/e5984a9bf3d9a6115aa0ae9873d7163f.jpg");

    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}

[data-testid="stHeader"]{
    background:transparent;
}

.block-container{
    max-width:650px;
    padding-top:40px;
    padding-bottom:50px;
}


/* ===========================
   TITLE
=========================== */

.login-title{
    text-align:center;
    font-size:70px;
    font-weight:900;
    letter-spacing:8px;
    color:#78efff;

    text-shadow:
        0 1px 0 #b5b5b5,
        0 2px 0 #999,
        0 3px 0 #777,
        0 4px 0 #555,
        0 5px 15px rgba(0,0,0,.8),
        0 0 35px rgba(229,9,20,.8);

    transform: perspective(600px) rotateX(10deg);

    margin-bottom:10px;
}

.login-subtitle{
    text-align:center;
    color:#ffd700;
    font-size:18px;
    margin-bottom:30px;
}


/* ===========================
   LOGIN CARD
=========================== */

.login-card{
    background:rgba(18,18,25,.72);
    border:1px solid rgba(255,255,255,.08);
    border-radius:22px;
    padding:28px;
    backdrop-filter:blur(18px);
    box-shadow:0 15px 45px rgba(0,0,0,.45);
}


/* ===========================
   INPUTS
=========================== */

.stTextInput input{
    background:#1A1D29;
    color:white;
    border-radius:12px;
    border:1px solid #333;
    padding:12px;
}

.stTextInput input:focus{
    border:1px solid #E50914;
}


/* ===========================
   BUTTON
=========================== */

div.stButton > button{
    width:100%;
    background:#E50914;
    color:white;
    border:none;
    border-radius:12px;
    height:48px;
    font-size:17px;
    font-weight:700;
    transition:.25s;
}

div.stButton > button:hover{
    background:#ff2b37;
}


/* ===========================
   TABS
=========================== */

.stTabs [data-baseweb="tab-list"]{
    gap:15px;
}

.stTabs [data-baseweb="tab"]{
    font-size:17px;
    color:white;
}

.stTabs [aria-selected="true"]{
    color:#E50914;
}


/* ===========================
   CHECKBOX
=========================== */

.stCheckbox label{
    color:white;
}


/* ===========================
   SUCCESS / ERROR
=========================== */

.stSuccess{
    border-radius:12px;
}

.stError{
    border-radius:12px;
}


/* ===========================
   HIDE STREAMLIT MENU
=========================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

</style>
""",
        unsafe_allow_html=True,
    )