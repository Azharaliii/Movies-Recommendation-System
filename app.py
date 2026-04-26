import streamlit as st
import pickle
import pandas as pd
import requests

# 1. Page Configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# 2. Advanced CSS for HD Background and Modern Styling
def add_bg_from_url():
    st.markdown(
         f"""
         <style>  
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
             background-attachment: fixed;
             background-size: cover;
         }}

         /* Making the selectbox and text stand out with a glass effect */
         .stSelectbox, .stButton {{
             background: rgba(255, 255, 255, 0.1);
             backdrop-filter: blur(10px);
             border-radius: 10px;
             padding: 10px;
         }}

         /* Styling the movie titles */
         .movie-title {{
             font-size: 14px;
             font-weight: bold;
             color: white;
             text-align: center;
             margin-top: 5px;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))       
    return recommended_movies, recommended_posters

# 3. Load Data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 4. Header with clean style
st.markdown("<h1 style='text-align: center; color: white;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d3d3d3;'>Discover your next favorite movie based on our advanced similarity algorithm.</p>", unsafe_allow_html=True)

# 5. User Selection
selected_movie_name = st.selectbox(
    'Type or select a movie you like:',
    movies['title'].values
)

# 6. Recommendation Logic
if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # 5 movies per row

    for i in range(len(names)):
        with cols[i % 5]:   # auto move to next row
            st.image(posters[i])
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)

# 7. Sidebar info
st.sidebar.image("https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg", width=150)
st.sidebar.image("https://www.freeiconspng.com/uploads/movie-icon-27.png", width=200)