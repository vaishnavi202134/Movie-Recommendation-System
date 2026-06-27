import streamlit as st
import pickle
import pandas as pd
import time
import requests


st.set_page_config(
    page_title="Movie Reco",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background: radial-gradient(circle at top, #1b1b2f, #0f0f0f 70%);
}


@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
    0% { box-shadow: 0 0 15px rgba(255, 75, 75, 0.4); }
    50% { box-shadow: 0 0 30px rgba(255, 75, 75, 0.8); }
    100% { box-shadow: 0 0 15px rgba(255, 75, 75, 0.4); }
}

.title {
    text-align: center;
    font-size: 3rem;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 1.2s ease-out;
    margin-bottom: 30px;
}

.movie-card {
    background: linear-gradient(145deg, #2a2a40, #1c1c2b);
    height: 90px;                     
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 12px;
    border-radius: 16px;
    margin-bottom: 10px;
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
    animation: slideUp 0.6s ease forwards, glow 3s infinite;
    overflow: hidden;
}

.movie-card {
    word-break: break-word;
}

.stButton > button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    border-radius: 14px;
    padding: 12px 24px;
    font-size: 18px;
    border: none;
}
</style>
""", unsafe_allow_html=True)



API_KEY = "4cc2036661282ae0420d3c5a68a853cf"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def rec(movie):
    mi = ml[ml['title'] == movie].index[0]
    dis = similarity[mi]
    ml_list = sorted(list(enumerate(dis)), reverse=True, key=lambda x: x[1])[1:6]

    rec_movies = []
    rec_posters = []

    for i in ml_list:
        movie_id = ml.iloc[i[0]].movie_id
        rec_movies.append(ml.iloc[i[0]].title)
        rec_posters.append(fetch_poster(movie_id))

    return rec_movies, rec_posters

ml_dict = pickle.load(open('movie_dict.pkl', 'rb'))
ml = pd.DataFrame(ml_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.markdown("<div class='title'>Movie Recommendation Engine</div>", unsafe_allow_html=True)
option = st.selectbox(
    "Pick a movie you love",
    ml['title'].values
)

if st.button("Get Recommendations"):
    with st.spinner("AI is thinking..."):
        time.sleep(1.5)

    rec_names, rec_posters = rec(option)

    st.markdown("### You may also like:")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"<div class='movie-card'>🎥 {rec_names[idx]}</div>",
                unsafe_allow_html=True
            )
            if rec_posters[idx]:
                st.image(rec_posters[idx], use_container_width=True)
