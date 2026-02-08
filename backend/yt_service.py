# backend/yt_service.py
from ytmusicapi import YTMusic
import os

class YTMusicProvider:
    def __init__(self):
        """Inicializa YT Music con diagnóstico"""
        try:
            oauth_path = os.path.join(os.path.dirname(__file__), 'oauth.json')
            self.yt = YTMusic(oauth_path)
            print("✅ Autenticación OAuth cargada")
            self._diagnosticar()  # 👈 Añade esto
        except Exception as e:
            print(f"❌ Error inicializando YTMusic: {e}")
            self.yt = None
    
    def _diagnosticar(self):
        """Prueba qué endpoints funcionan"""
        print("\n🔍 DIAGNÓSTICO DE PERMISOS:")
        
        # Test 1: Búsqueda (no requiere auth)
        try:
            search = self.yt.search("test", limit=1)
            print(f"✅ search(): OK ({len(search)} resultados)")
        except Exception as e:
            print(f"❌ search(): {type(e).__name__}: {e}")
        
        # Test 2: Historial (requiere permisos)
        try:
            history = self.yt.get_history()
            print(f"✅ get_history(): OK ({len(history)} canciones)")
        except Exception as e:
            print(f"❌ get_history(): {type(e).__name__}: {e}")
        
        # Test 3: Playlists de biblioteca
        try:
            playlists = self.yt.get_library_playlists(limit=5)
            print(f"✅ get_library_playlists(): OK ({len(playlists)} playlists)")
        except Exception as e:
            print(f"❌ get_library_playlists(): {type(e).__name__}: {e}")
        
        # Test 4: Liked songs
        try:
            liked = self.yt.get_liked_songs(limit=1)
            print(f"✅ get_liked_songs(): OK")
        except Exception as e:
            print(f"❌ get_liked_songs(): {type(e).__name__}: {e}")
        
        # Test 5: Artistas suscritos
        try:
            artists = self.yt.get_library_artists(limit=5)
            print(f"✅ get_library_artists(): OK ({len(artists)} artistas)")
        except Exception as e:
            print(f"❌ get_library_artists(): {type(e).__name__}: {e}")
        
        print("━" * 50)
    
    def is_authenticated(self):
        return self.yt is not None

yt_provider = YTMusicProvider()