import pyttsx3
import speech_recognition as sr
from datetime import datetime
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

# Lock para evitar conflito de múltiplas threads usando o engine ao mesmo tempo
lock_engine = threading.Lock()

def falar(texto):
    with lock_engine:
        engine.say(texto)
        engine.runAndWait()

def falar_async(texto):
    def falar_thread():
        with lock_engine:
            engine.say(texto)
            engine.runAndWait()
    threading.Thread(target=falar_thread).start()

# Função utilitária para verificar dispositivos Spotify ativos
def dispositivo_ativo(sp):
    devices = sp.devices()
    if not devices['devices']:
        falar_async('Nenhum dispositivo do Spotify está ativo. Abra o app e reproduza algo primeiro.')
        return None
    return devices['devices'][0]['id']  # retorna o primeiro dispositivo ativo

# Função para tocar música com verificação de dispositivo
def tocar_com_verificacao(sp, uri):
    device_id = dispositivo_ativo(sp)
    if device_id:
        sp.start_playback(device_id=device_id, uris=[uri])
    
def saudacao():
    hora = datetime.now().hour
    if hora < 12:
        msg = 'Bom dia Shelby!'
    elif hora < 18:
        msg = 'Boa tarde Shelby!'
    else:
        msg = 'Boa noite Shelby!'
    data = datetime.now().strftime('%d/%m/%Y')
    falar(f"{msg}") #Hoje é {data}.")

def ouvir(modo_teste=False):
    if modo_teste:
        return input("Digite o comando: ")

    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('🎙️ Julie está ouvindo...')
            voz = listener.listen(source)
            comando = listener.recognize_google(voz, language='pt-PT')
            print(f"Comando: {comando}")
            return comando
    except:
        return 'no sound'
