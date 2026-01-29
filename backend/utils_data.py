import pandas as pd
from backend.rag_engine import add_songs_to_vector_db

def procesar_historial_usuario(playlist_data):
    """
    playlist_data: Lista de diccionarios con [title, artist, genre, timestamp]
    """
    df = pd.DataFrame(playlist_data)
    
    # 1. Alimentamos el RAG: Guardamos los metadatos de las canciones para que el agente las encuentre
    canciones_texto = [f"{item['title']} de {item['artist']} - Género: {item['genre']}" for item in playlist_data]
    add_songs_to_vector_db(canciones_texto)
    
    # 2. Alimentamos el TFT: Creamos una métrica numérica (ej: 'mood_score') basada en el género
    # Esto es lo que el Transformer usará para predecir la tendencia
    genre_map = {"Rock": 0.8, "Lo-Fi": 0.2, "Pop": 0.5, "Techno": 0.9}
    df['mood_score'] = df['genre'].map(genre_map).fillna(0.5)
    
    return df