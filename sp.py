import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyttsx3
import os 

listener = sr.Recognizer()

sr.Microphone.list_microphone_names()

def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:
            print('Listening...')

# Configurações de autenticação
os.environ['SPOTIPY_CLIENT_ID'] = '631c53df63f841d2962c9c06d746a5c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = '4ddee1ce1dd646ce841e979d030590e6'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/retorno'

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

engine = pyttsx3.init()
engine.say('Hello')
engine.runAndWait()

while True:
    command = ouvir()

    if 'spotify play' in command.lower():
        query = command.lower().replace('spotify play','').strip()

        results = sp.search(query,1,0,"track")

        nome_artista = results['tracks']['items'][0]['artists'][0]['name']
        nome_musica = results['tracks']['items'][0]['name']
        track_uri = results['tracks']['items'][0]['uri']

        engine.say(f'Playing {nome_musica} by {nome_artista}')
        engine.runAndWait()

        sp.start_playback(uris=[track_uri])

    elif 'spotify pause' in command.lower():
        sp.pause_playback()
    elif 'spotify continue' in command.lower():
        sp.start_playback()
    elif 'spotify change volume to' in command.lower():
        volume = int(command.lower().replace('spotify change volume to','').strip())
        sp.volume(volume)