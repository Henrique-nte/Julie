import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from voz import falar_async

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Autenticação Spotify
scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=".cache"))

def tocar_musica(sp, query):
    results = sp.search(query, limit=5, type="track")

    if not results['tracks']['items']:
        falar_async('Música não encontrada.')
        return

    devices = sp.devices()
    if not devices['devices']:
        falar_async('Nenhum dispositivo ativo. Abra o Spotify.')
        return

    track = results['tracks']['items'][0]
    nome = track['name']
    artista = track['artists'][0]['name']
    uri = track['uri']

    falar_async(f'Tocando {nome} por {artista}')
    sp.start_playback(uris=[uri])

def pausar(sp):
    sp.pause_playback()

def continuar(sp):
    sp.start_playback()

def mudar_volume(sp, volume):
    sp.volume(volume)

def ajuda():
    print('Você pode dizer: spotify tocar, spotify pause, spotify continue, ou mude volume para 50.')

