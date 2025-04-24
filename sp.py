import os  # Acesso ao sistema (como variáveis de ambiente)
import speech_recognition as sr  # Reconhecimento de voz
import spotipy  # Controle da API do Spotify
from spotipy.oauth2 import SpotifyOAuth  # Autenticação no Spotify
import pyttsx3  # Síntese de voz (fala)
from datetime import datetime  # Data e hora

# Define as credenciais do app do Spotify
os.environ['SPOTIPY_CLIENT_ID'] = '631c53df63f841d2962c9c06d746a5c6'  # ID do app Spotify
os.environ['SPOTIPY_CLIENT_SECRET'] = '4ddee1ce1dd646ce841e979d030590e6'  # Segredo do app
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/retorno'  # URL de redirecionamento

# Define as permissões e faz login no Spotify
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=".cache"))

# Configura a voz da assistente
engine = pyttsx3.init()  # Inicializa motor de voz
voices = engine.getProperty('voices')  # Lista de vozes disponíveis
engine.setProperty('voice', voices[0].id)  # Escolhe uma voz
engine.setProperty('rate', 170)  # Velocidade da fala

# Função para dar bom dia, tarde ou noite com a data
def saudacao():
    hora = datetime.now().hour  # Pega a hora atual
    if hora < 12:
        msg = 'Bom dia Shelby!'
    elif hora < 18:
        msg = 'Boa tarde Shelby!'
    else:
        msg = 'Boa noite Shelby!'
    data = datetime.now().strftime('%d/%m/%Y')  # Formata a data
    engine.say(f"{msg} Hoje é {data}.")  # Fala a saudação
    engine.runAndWait()  # Executa a fala

listener = sr.Recognizer()  # Inicializa o reconhecedor de voz

# Função para escutar e converter fala em texto
def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:  # Usa microfone
            print('🎙️ Julie está ouvindo...')
            voice = listener.listen(source)  # Escuta o áudio
            command = listener.recognize_google(voice, language='pt-PT')  # Converte para texto
            print(f"Comando: {command}")
            return command
    except:
        return 'No Sound'  # Se falhar, retorna erro genérico

saudacao()  # Executa a saudação logo no início

# Loop principal que fica ouvindo comandos
while True:
    command = ouvir().lower()  # Ouve e transforma tudo em minúsculas

    if 'spotify tocar' in command:
        query = command.replace('spotify tocar', '').strip()  # Extrai o nome da música
        results = sp.search(query, limit=5, type="track")  # Busca no Spotify

        if not results['tracks']['items']:  # Se não achou
            engine.say('Música não encontrada.')
            engine.runAndWait()
            continue

        devices = sp.devices()  # Verifica dispositivos ativos
        if not devices['devices']:  # Se nenhum dispositivo estiver tocando
            engine.say('Nenhum dispositivo ativo. Abra o Spotify.')
            engine.runAndWait()
            continue

        # Toca a primeira música encontrada
        track = results['tracks']['items'][0]  # Pega a primeira música
        nome_musica = track['name']  # Nome da música
        nome_artista = track['artists'][0]['name']  # Nome do artista
        track_uri = track['uri']  # URI da faixa

        engine.say(f'Tocando {nome_musica} por {nome_artista}')
        engine.runAndWait()
        sp.start_playback(uris=[track_uri])  # Começa a tocar no Spotify

    elif 'spotify pause' in command:
        sp.pause_playback()  # Pausa a reprodução

    elif 'spotify continue' in command:
        sp.start_playback()  # Continua a reprodução

    elif 'mude volume para' in command:
        try:
            volume = int(command.replace('mude volume para', '').strip())  # Extrai valor do volume
            sp.volume(volume)  # Altera o volume
        except:
            engine.say('Volume inválido.')  # Se deu erro
            engine.runAndWait()
