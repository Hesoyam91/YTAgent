# backend/tools.py
from langchain.tools import tool
from .yt_service import yt_provider

@tool
def obtener_historial_reciente(limit: str) -> str:
    """Obtiene las últimas canciones escuchadas por el usuario.
    
    Args:
        limit: SOLO el número (ej: "5" o "10"), sin texto adicional
    
    Ejemplos válidos de input:
        - "10"
        - "5"
        - "1"
    
    Ejemplos INVÁLIDOS (no usar):
        - "limit = 10"
        - "10 canciones"
        - "dame 10"
    """
    try:
        # Limpia el input (por si Grok envía basura)
        clean_limit = "".join(filter(str.isdigit, str(limit)))
        limit_int = int(clean_limit) if clean_limit else 10
        
        print(f"🔍 Obteniendo historial con limit={limit_int}")
        
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music. Verifica oauth.json"
        
        historial = yt_provider.yt.get_history()
        
        if not historial:
            return "No tienes historial de reproducción en YouTube Music."
        
        canciones = []
        for item in historial[:limit_int]:
            title = item.get('title', 'Desconocido')
            artists = item.get('artists', [])
            artist = artists[0].get('name', 'Desconocido') if artists else 'Desconocido'
            canciones.append(f"🎵 {title} - {artist}")
        
        if limit_int == 1:
            return f"Tu última canción fue:\n{canciones[0]}"
        else:
            return f"Tus últimas {len(canciones)} canciones:\n" + "\n".join(canciones)
        
    except Exception as e:
        print(f"❌ Error en obtener_historial_reciente: {e}")
        import traceback
        traceback.print_exc()
        return f"Error al obtener historial: {str(e)}"


@tool
def listar_mis_playlists() -> str:
    """Lista TODAS las playlists del usuario en YouTube Music.
    
    Esta herramienta NO requiere parámetros.
    """
    try:
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        print("🔍 Obteniendo playlists...")
        playlists = yt_provider.yt.get_library_playlists(limit=100)
        
        if not playlists:
            return "No encontré playlists en tu biblioteca. ¿Has creado alguna?"
        
        print(f"✅ Encontradas {len(playlists)} playlists")
        
        lista = []
        for pl in playlists:
            nombre = pl.get('title', 'Sin nombre')
            count = pl.get('count', 0)
            playlist_id = pl.get('playlistId', 'N/A')
            lista.append(f"📁 {nombre} ({count} canciones) - ID: {playlist_id}")
        
        return f"Tienes {len(lista)} playlists:\n" + "\n".join(lista)
        
    except Exception as e:
        print(f"❌ Error en listar_mis_playlists: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}\n\nSugerencia: Verifica que oauth.json tenga permisos de lectura de biblioteca."


@tool
def buscar_playlist_por_nombre(nombre: str) -> str:
    """Busca una playlist específica por su nombre.
    
    Args:
        nombre: SOLO el nombre de la playlist (sin texto adicional)
    
    Ejemplos válidos:
        - "wenardo"
        - "Mis favoritas"
    
    Ejemplos INVÁLIDOS:
        - "busca la playlist wenardo"
        - "nombre = wenardo"
    """
    try:
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        print(f"🔍 Buscando playlist: '{nombre}'")
        playlists = yt_provider.yt.get_library_playlists(limit=100)
        
        if not playlists:
            return f"No tienes playlists. '{nombre}' no existe."
        
        nombre_lower = nombre.lower().strip()
        encontradas = []
        
        for pl in playlists:
            titulo = pl.get('title', '')
            if nombre_lower in titulo.lower():
                count = pl.get('count', 0)
                playlist_id = pl.get('playlistId', 'N/A')
                encontradas.append({
                    'nombre': titulo,
                    'canciones': count,
                    'id': playlist_id
                })
        
        if not encontradas:
            return f"❌ No encontré ninguna playlist con '{nombre}' en el nombre.\n\nTip: Usa la herramienta 'listar_mis_playlists' para ver todas tus playlists."
        
        if len(encontradas) == 1:
            pl = encontradas[0]
            return f"✅ ¡Sí! Encontré la playlist '{pl['nombre']}' con {pl['canciones']} canciones (ID: {pl['id']})"
        else:
            resultados = "\n".join([f"✅ '{pl['nombre']}' ({pl['canciones']} canciones)" for pl in encontradas])
            return f"Encontré {len(encontradas)} playlists con '{nombre}':\n{resultados}"
        
    except Exception as e:
        print(f"❌ Error en buscar_playlist_por_nombre: {e}")
        return f"Error: {str(e)}"


@tool
def ver_canciones_de_playlist(playlist_id: str) -> str:
    """Muestra las canciones de una playlist específica.
    
    Args:
        playlist_id: ID de la playlist (obtenido de buscar_playlist_por_nombre)
    """
    try:
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        playlist = yt_provider.yt.get_playlist(playlist_id, limit=100)
        
        if not playlist:
            return f"No encontré la playlist con ID: {playlist_id}"
        
        nombre = playlist.get('title', 'Playlist')
        tracks = playlist.get('tracks', [])
        
        if not tracks:
            return f"La playlist '{nombre}' está vacía."
        
        canciones = []
        for idx, track in enumerate(tracks[:50], 1):  # Limitar a 50
            title = track.get('title', 'Desconocido')
            artists = track.get('artists', [])
            artist = artists[0].get('name', 'Desconocido') if artists else 'Desconocido'
            canciones.append(f"{idx}. {title} - {artist}")
        
        total = len(tracks)
        mostrando = len(canciones)
        
        resultado = f"🎵 Playlist: {nombre}\n"
        resultado += f"Total: {total} canciones (mostrando {mostrando}):\n\n"
        resultado += "\n".join(canciones)
        
        return resultado
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def buscar_canciones(query: str) -> str:
    """Busca canciones en YouTube Music por nombre, artista o álbum.
    
    Args:
        query: Término de búsqueda
    """
    try:
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        results = yt_provider.yt.search(query, filter="songs", limit=5)
        
        if not results:
            return f"No encontré resultados para '{query}'."
        
        canciones = []
        for r in results:
            title = r.get('title', 'Desconocido')
            artists = r.get('artists', [])
            artist = artists[0].get('name', 'Desconocido') if artists else 'Desconocido'
            canciones.append(f"🎵 {title} - {artist}")
        
        return f"Resultados para '{query}':\n" + "\n".join(canciones)
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def obtener_canciones_mas_escuchadas(limit: str) -> str:
    """Analiza el historial para encontrar las canciones más repetidas.
    
    Args:
        limit: SOLO el número (ej: "10")
    """
    try:
        clean_limit = "".join(filter(str.isdigit, str(limit)))
        limit_int = int(clean_limit) if clean_limit else 10
        
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        historial = yt_provider.yt.get_history()
        
        if not historial or len(historial) < 10:
            return "No hay suficiente historial para analizar."
        
        # Contar repeticiones
        contador = {}
        for item in historial[:200]:  # Analizar últimas 200
            title = item.get('title', '')
            artists = item.get('artists', [])
            artist = artists[0].get('name', '') if artists else ''
            
            if title and artist:
                key = f"{title} - {artist}"
                contador[key] = contador.get(key, 0) + 1
        
        # Ordenar por frecuencia
        top = sorted(contador.items(), key=lambda x: x[1], reverse=True)[:limit_int]
        
        resultado = []
        for cancion, veces in top:
            resultado.append(f"🔥 {cancion} ({veces}x)")
        
        return f"Tus {len(resultado)} canciones más escuchadas:\n" + "\n".join(resultado)
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def recomendar_canciones_similares(cancion: str) -> str:
    """Recomienda canciones similares basándose en una canción.
    
    Args:
        cancion: Nombre de la canción de referencia
    """
    try:
        if not yt_provider.is_authenticated():
            return "❌ No hay conexión con YouTube Music."
        
        # Buscar la canción
        results = yt_provider.yt.search(cancion, filter="songs", limit=1)
        
        if not results:
            return f"No encontré la canción '{cancion}'."
        
        video_id = results[0].get('videoId')
        
        # Obtener radio/mix
        relacionadas = yt_provider.yt.get_watch_playlist(videoId=video_id, limit=10)
        
        if not relacionadas or 'tracks' not in relacionadas:
            return f"No pude encontrar canciones similares a '{cancion}'."
        
        recos = []
        for track in relacionadas['tracks'][:7]:
            title = track.get('title', 'Desconocido')
            artists = track.get('artists', [])
            artist = artists[0].get('name', 'Desconocido') if artists else 'Desconocido'
            recos.append(f"🎵 {title} - {artist}")
        
        return f"Canciones similares a '{cancion}':\n" + "\n".join(recos)
        
    except Exception as e:
        return f"Error: {str(e)}"