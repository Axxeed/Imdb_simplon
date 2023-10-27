import pandas as pd
# from sklearn.linear_model import SGDRegressor
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.preprocessing import StandardScaler
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
# import difflib
import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer





def get_top_recommendations(input_title:str):
    df= pd.read_csv("movie_metadata.csv")
    df.drop_duplicates(inplace=True)
    cols = ['movie_title', 'plot_keywords']
    df = df[cols]
    df.dropna(inplace=True)

    input_movie = df[df['movie_title'] == input_title]

    features = input_movie[['plot_keywords']]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['plot_keywords'])

    features = pd.DataFrame(tfidf_matrix.toarray())

    cosine_sim = cosine_similarity(features, features)

    idx = df.index[df['movie_title'] == input_title].tolist()[0]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_indices = [i[0] for i in sim_scores[1:6]]

    return df['movie_title'].iloc[sim_indices]
