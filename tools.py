# Paramètre de connexion.
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Initialisation connexion BDD.
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Autres
import pandas as pd
import streamlit as st

# ================================================================================>

# Fonction qui charge le fichier css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# ================================================================================>

# Fonction permettant de se connecter à la base de données.
def connect():
    load_dotenv('.env')
    engine = create_engine('mysql+pymysql://root:1234Simplon@5.tcp.eu.ngrok.io:16336/imdb')
    conn = engine.connect()
    return conn

# ================================================================================>

# Fonction permettant de créer les tables dans une base de données.
def create_table_predictions():

    # Connexion.
    conn = connect()
    cursor = conn.connection.cursor()

    # Création de la table "predictions" s'il n'existe pas.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions
        (id_prediction INTEGER PRIMARY KEY AUTO_INCREMENT,
        id_movie INTEGER,
        prediction_result TEXT,
        FOREIGN KEY (id_movie) REFERENCES movie (id_movie)
        )
    ''')

    print("Table 'predictions' créée avec succès.")

    # Fermer la connexion.
    conn.close()

# ================================================================================>

# Récupération de la colonne title_movie.
def get_title_movies():

    # Récupération de la liste des films pour l'input.
    conn = connect()
    table1_sql = "SELECT movie_title FROM movie"
    movie_title = pd.read_sql_query(table1_sql, conn)

    # netflix_df = pd.read_csv("movie_metadata.csv")
    # netflix_df['movie_title'] = netflix_df['movie_title'].str.rstrip('\xa0')
    return movie_title

# ================================================================================>

# Envoie data nettoyée.
def send_clean_data():
    netflix_data = pd.read_csv("netflix_data.csv")
    engine = connect()
    netflix_data.to_sql(name='netflix_data', con=engine, if_exists='append', index=False)
    engine.close()
    print("netflix_data envoyé avec succès !")

# ======================================================================================>

# Fonction permettent d'insérer les données.
def insert_data_to_database(data):

    # Récupération de la colonne title et id de la table netflix_data.
    conn = connect()
    table1_sql = "SELECT id_movie, movie_title FROM movie"
    movie_title_id = pd.read_sql_query(table1_sql, conn)

    # Récupération id du film.
    movie_id = movie_title_id[movie_title_id['movie_title'] == "Avatar"]['id_movie'][0]

    # Insertion des prédictions et de lla clé étrangère du film.
    table1_sql = "INSERT INTO predictions (id_movie, prediction_result) VALUES (%s, %s)"
    conn.execute(table1_sql, (movie_id, str(data["predictions"])))
    conn.close()

# ======================================================================================>

# # Fonction permettent de mettre un background.
# def background_front(url:str):
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url({url});
#              background-attachment: fixed;
#              background-size: cover;
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#     )

# ======================================================================================>
