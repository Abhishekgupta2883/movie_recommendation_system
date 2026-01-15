import pickle
import streamlit as st
import pandas as pd
import requests

import os
from dotenv import load_dotenv

load_dotenv()


# Set page config
st.set_page_config(page_title="Movie Recommender", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for modern dark theme styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    body {
        background: linear-gradient(135deg, #1e1e2f, #2b2b3d);
        color: #e0e0e0;

        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #4e44ce;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #5a4fd5;
    }
    .stSelectbox>div>div>div {
        background-color: #2b2b3d;
        color: #e0e0e0;
        border-radius: 8px;
    }
    .stColumn > div {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{{}}?api_key={os.getenv('TMDB_API_KEY')}&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('combined_similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




