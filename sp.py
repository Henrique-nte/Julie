import os
import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyttsx3
from datetime import datetime

# Autenticação Spotify
os.environ['SPOTIPY_CLIENT_ID'] = '631c53df63f841d2962c9c06d746a5c6'
os.environ['SPOTIPY_CLIENT_SECRET'] = '4ddee1ce1dd646ce841e979d030590e6'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/retorno'

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=".cache"))

# Inicializa voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Pode testar com outros índices
engine.setProperty('rate', 170)

# Saudação com data
def saudacao():
    hora = datetime.now().hour
    if hora < 12:
        msg = 'Bom dia Shelby!'
    elif hora < 18:
        msg = 'Boa tarde Shelby!'
    else:
        msg = 'Boa noite Shelby!'
    data = datetime.now().strftime('%d/%m/%Y')
    engine.say(f"{msg} Hoje é {data}.")
    engine.runAndWait()

# Reconhecimento de voz
listener = sr.Recognizer()

def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:
            print('🎙️ Julie está ouvindo...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='pt-PT')
            print(f"Comando: {command}")
            return command
    except:
        return 'No Sound'

# Saudação inicial
saudacao()

# Loop principal
while True:
    command = ouvir().lower()

    if 'spotify tocar' in command:
        query = command.replace('spotify tocar', '').strip()
        results = sp.search(query, limit=5, type="track")

        if not results['tracks']['items']:
            engine.say('Música não encontrada.')
            engine.runAndWait()
            continue

        # Verifica dispositivos ativos
        devices = sp.devices()
        if not devices['devices']:
            engine.say('Nenhum dispositivo ativo. Abra o Spotify.')
            engine.runAndWait()
            continue

        # Toca a primeira música encontrada
        track = results['tracks']['items'][0]
        nome_musica = track['name']
        nome_artista = track['artists'][0]['name']
        track_uri = track['uri']

        engine.say(f'Tocando {nome_musica} por {nome_artista}')
        engine.runAndWait()
        sp.start_playback(uris=[track_uri])

    elif 'spotify pause' in command:
        sp.pause_playback()

    elif 'spotify continue' in command:
        sp.start_playback()

    elif 'mude volume para' in command:
        try:
            volume = int(command.replace('mude volume para', '').strip())
            sp.volume(volume)
        except:
            engine.say('Volume inválido.')
            engine.runAndWait()
