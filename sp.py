import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Configurações de autenticação
os.environ['SPOTIPY_CLIENT_ID'] = '631c53df63f841d2962c9c06d746a5c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = '4ddee1ce1dd646ce841e979d030590e6'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/retorno'

# Permissões necessárias para controlar a reprodução
scope = "user-read-playback-state user-modify-playback-state"

# Autenticação correta para controle de reprodução
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Música a ser tocada
query = 'Runaway'
results = sp.search(query, 1, 0, "track")

# Verifica se encontrou a música
if results["tracks"]["items"]:
    track_uri = results["tracks"]["items"][0]["uri"]
    sp.start_playback(uris=[track_uri])
    print("🎵 Música tocando:", results["tracks"]["items"][0]["name"])
else:
    print("❌ Nenhuma música encontrada.")

