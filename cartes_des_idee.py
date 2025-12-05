import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from settings import REQUIRED_COLS, THEME_COLORS_LIST, COULEURS_FR

# --- Configuration de la Page ---
st.set_page_config(
    page_title="Carte des Propositions vivre le Bourget-du-lac",
    page_icon="📍",
    layout="wide",
)

st.title("📍 Carte Interactive des propositions au Bourget")
st.markdown(
    "Chaque marqueur a une couleur basée sur le **thème** et affiche la **suggestion** dans son pop-up."
)

# --- Téléchargement du Fichier CSV ---
# uploaded_file = st.file_uploader(
#     "Téléchargez votre fichier CSV",
#     type="csv",
#     help="Le fichier doit contenir : 'theme', 'lat', 'lon', 'suggestions', 'localisation'."
# )

uploaded_file = "proposition_geoloc.csv"


def check_columns(df: pd.DataFrame, required_cols: list):
    required_cols = ["theme", "lat", "lon", "suggestions", "localisation"]
    if not all(col in df.columns for col in required_cols):
        st.error(
            "⚠️ Erreur: Le fichier CSV doit contenir les colonnes exactes : "
            "'theme', 'lat', 'lon', 'suggestions', 'localisation'."
        )
        st.stop()


def clean_gps_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df.dropna(subset=["lat", "lon"], inplace=True)
    return df


def get_unique_themes_and_theme_to_color(
    df: pd.DataFrame, theme_colors_list: list
) -> tuple[list, list]:
    # 2. Définition de la Légende et des Couleurs
    unique_themes = df["theme"].unique()

    # Mapping Thème -> Couleur
    theme_to_color = {
        theme: theme_colors_list[i % len(theme_colors_list)]
        for i, theme in enumerate(unique_themes)
    }

    return unique_themes, theme_to_color


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        check_columns(df, REQUIRED_COLS)

        df = clean_gps_coordinates(df)

        # st.dataframe(df.head())

        unique_themes, theme_to_color = get_unique_themes_and_theme_to_color(
            df, THEME_COLORS_LIST
        )

        st.sidebar.header("Options et Légende")

        # Afficher la légende dans la barre latérale
        st.sidebar.subheader("Légende des Thèmes")
        legend_data = pd.DataFrame(
            {
                "Thème": unique_themes,
                "Couleur": [COULEURS_FR[theme_to_color[t]] for t in unique_themes],
            }
        )
        st.sidebar.dataframe(legend_data, hide_index=True)

        # Filtre par thème
        selected_themes = st.sidebar.multiselect(
            "Filtrer par Thème", options=unique_themes, default=unique_themes
        )

        df_filtered = df[df["theme"].isin(selected_themes)]

        if df_filtered.empty:
            st.warning("Aucune donnée à afficher après le filtrage.")
            st.stop()

        # 3. Création de la Carte Folium

        # Calculer la position moyenne pour centrer la carte
        center_lat = df_filtered["lat"].mean()
        center_lon = df_filtered["lon"].mean()

        # Initialiser la carte
        m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

        # 4. Ajout des Marqueurs (Pins) avec Pop-ups Personnalisés

        for index, row in df_filtered.iterrows():
            theme = row["theme"]
            color = theme_to_color[theme]

            # Contenu HTML du Pop-up
            popup_html = f"""
            <h4>📍 Proposition : {row["theme"]}</h4>
            <hr style="margin:5px 0;">
            <b>Localisation:</b> {row["localisation"]}<br>
            <b>Suggestion:</b> <em>{row["suggestions"]}</em><br>
            """

            # Création de l'objet Pop-up
            popup = folium.Popup(popup_html, max_width=300)

            # Ajout du marqueur à la carte
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=popup,  # Utilisation du pop-up personnalisé
                tooltip=row["suggestions"],  # Texte affiché au survol
                icon=folium.Icon(
                    color=color, icon="lightbulb", prefix="fa"
                ),  # Icône et couleur personnalisées
            ).add_to(m)

        # 5. Affichage de la Carte dans Streamlit
        st.subheader(f"Carte de {len(df_filtered)} Propositions Filtrées")

        # La fonction st_folium affiche la carte Folium dans Streamlit
        st_folium(m, width=1400, height=1200)

    except Exception as e:
        st.error(
            f"Une erreur est survenue lors du traitement du fichier ou de la carte : {e}"
        )
        st.exception(e)  # Afficher l'erreur complète pour le débogage

else:
    st.info("Veuillez téléverser un fichier CSV pour afficher la carte interactive.")
