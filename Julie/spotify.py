import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from voz import falar

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Autenticação Spotify
scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=".cache"))

def tocar_musica(sp, query):
    results = sp.search(query, limit=5, type="track")

    if not results['tracks']['items']:
        falar('Música não encontrada.')
        return

    devices = sp.devices()
    if not devices['devices']:
        falar('Nenhum dispositivo ativo. Abra o Spotify.')
        return

    track = results['tracks']['items'][0]
    nome = track['name']
    artista = track['artists'][0]['name']
    uri = track['uri']

    falar(f'Tocando {nome} por {artista}')
    sp.start_playback(uris=[uri])

def pausar(sp):
    sp.pause_playback()

def continuar(sp):
    sp.start_playback()

def mudar_volume(sp, volume):
    sp.volume(volume)
