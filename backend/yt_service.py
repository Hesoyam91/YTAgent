from ytmusicapi import YTMusic
import os

class YTMusicProvider:
    def __init__(self, auth_file="backend/oauth.json"):
        # Verificamos que el archivo exista antes de intentar cargar
        if not os.path.exists(auth_file):
            raise FileNotFoundError(f"❌ No se encontró el archivo de sesión en: {auth_file}")
        
        try:
            # IMPORTANTE: En versiones recientes, simplemente pasamos la ruta del archivo.
            # ytmusicapi detectará si es OAuth por el contenido del JSON.
            self.yt = YTMusic(auth_file)
            print("✅ Autenticación OAuth cargada con éxito.")
        except Exception as e:
            print(f"❌ Error al inicializar YTMusic con OAuth: {e}")
            raise

    def get_user_vibe(self):
        """
        Extrae el historial reciente y los artistas favoritos 
        para crear un 'perfil de humor' musical para la IA.
        """
        try:
            # Obtenemos historial y canciones que te gustan
            history = self.yt.get_history()
            liked_songs = self.yt.get_liked_songs(limit=5)
            
            # Formateamos un string limpio para el prompt de la IA
            context = "Historial reciente: "
            context += ", ".join([f"{t['title']} ({t['artists'][0]['name']})" for t in history[:10]])
            
            return context
        except Exception as e:
            return f"Error extrayendo datos de YT Music: {e}"
        
yt_provider = YTMusicProvider()