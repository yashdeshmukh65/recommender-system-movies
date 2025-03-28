import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .title-style {
        font-size:40px !important;
        color:#ff4b4b;
        font-weight:bold;
        text-align: center;
    }
    .subtitle-style {
        font-size:20px !important;
        color:#333333;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        text-align:center;
        color: grey;
        font-size: 14px;
        margin-top: 40px;
    }
    .linkedin {
        text-align:center;
        font-size:16px;
        margin-top: 5px;
    }
    .linkedin a {
        color: #0e76a8;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def fetch_movie_details(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    data = response.json()
    poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    title = data.get("title", "Unknown Title")
    overview = data.get("overview", "No overview available.")
    rating = data.get("vote_average", "N/A")
    release_date = data.get("release_date", "N/A")
    return title, overview, rating, release_date, poster


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_overviews = []
    recommended_ratings = []
    recommended_release_dates = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title, overview, rating, release_date, poster = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_overviews.append(overview)
        recommended_ratings.append(rating)
        recommended_release_dates.append(release_date)

    return recommended_movies, recommended_posters, recommended_overviews, recommended_ratings, recommended_release_dates


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("<h1 class='title-style'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-style'>🔍 Select your favorite movie and get top 5 recommendations instantly!</p>",
            unsafe_allow_html=True)

selected_movie_name = st.selectbox('🎥 Choose a Movie', movies['title'].values)

if st.button('🚀 Recommend'):
    names, posters, overviews, ratings, release_dates = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            with st.expander(f"🔍 **{names[i]}**"):
                st.markdown(f"**📅 Release Date:** {release_dates[i]}")
                st.markdown(f"**⭐ Rating:** {ratings[i]}/10")
                st.markdown(f"**📖 Overview:** {overviews[i]}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit<br>
    Project by <strong>Yash Deshmukh</strong>
</div>
<div class="linkedin">
    🔗 <a href="https://www.linkedin.com/in/yash-deshmukh-0b7151287/" target="_blank">Connect with me on LinkedIn</a>
</div>
""", unsafe_allow_html=True)
