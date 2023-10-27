import pandas as pd
import streamlit as st
from model import *
from tools import *
from PIL import Image
import io

def main():

    #Import du CSS
    local_css("style.css")
    # Récupération des titres des films

    #---------------------  Sidebar  ----------------------#

    # Chargement de l'image à partir d'un fichier local
    image_path = "picture.PNG"
    image = Image.open(image_path)

    # Redimensionnement de l'image
    width, height = image.size
    new_width = int(width * 0.5)  # Réduire la largeur de l'image de moitié
    new_height = int(height * 0.5)  # Réduire la hauteur de l'image de moitié
    resized_image = image.resize((new_width, new_height))

    # Conversion de l'image redimensionnée en format PNG
    image_io = io.BytesIO()
    resized_image.save(image_io, format='PNG')

    # Affichage de l'image redimensionnée dans Streamlit
    st.sidebar.image(image_io, caption='Image de description', use_column_width=True)


    title_movies = get_title_movies()

    # Le formulaire.
    with st.form("my_form"):

        # Dictionnaire contenant l'input de choix du film.
        movie = st.selectbox('Sélectionnez votre Film...', (title_movies))

        # Bouton d'envoi du formulaire.
        submitted = st.form_submit_button("Envoyer")

        # Si l'utilisateur clique sur envoyer :
        if submitted:

            # Execution du model et affichage du résultat.
            top_recommendations = get_top_recommendations(input_title=movie)

            st.subheader("Vous aimerez aussi peut-être:")

            # Affichez les 5 premières recommandations
            for i, film in enumerate(top_recommendations[:5], 1):
                st.write(f"**{i}.** {film}")





            # st.write(top_recommendations)
            # # Ajout de la prédiction et du film choisis.
            # data={}
            # data["movie"] = movie

            # # Nettoyage des prédictions.
            # predictions = [i.replace(" ", "").replace("\xa0", "") for i in top_recommendations["movie_title"]]
            # data["predictions"] = predictions

            # # Insertion des données.
            # insert_data_to_database(data=data)

main()
