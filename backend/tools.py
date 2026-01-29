from langchain.tools import tool
from .yt_service import YTMusicProvider

yt = YTMusicProvider()

@tool
def obtener_historial_usuario(limit: int = 10):
    """Obtiene las últimas canciones escuchadas por el usuario. El argumento debe ser un número entero."""
    # Forzamos la conversión por si el LLM envía basura
    """
    Uso: Proporciona UN NÚMERO ENTERO para el límite. 
    Ejemplo: 10
    No envíes nombres de variables, solo el número.
    """
    try:
        if isinstance(limit, str):
            # Limpia casos como "limit = 10" o "10"
            clean_limit = "".join(filter(str.isdigit, limit))
            limit = int(clean_limit) if clean_limit else 10
        
        return yt.get_user_vibe() 
    except Exception as e:
        print(f"Error en tool limit: {e}")
        return yt.get_user_vibe()

@tool
def buscar_musica(query: str):
    """Busca canciones, artistas o álbumes en YouTube Music. Útil para dar recomendaciones específicas."""
    results = yt.yt.search(query, filter="songs")
    return [f"{r['title']} - {r['artists'][0]['name']} (ID: {r['videoId']})" for r in results[:3]]