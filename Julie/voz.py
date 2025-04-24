#import pyttsx3
#import speech_recognition as sr
from datetime import datetime

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def saudacao():
    hora = datetime.now().hour
    if hora < 12:
        msg = 'Bom dia Shelby!'
    elif hora < 18:
        msg = 'Boa tarde Shelby!'
    else:
        msg = 'Boa noite Shelby!'
    data = datetime.now().strftime('%d/%m/%Y')
    falar(f"{msg} Hoje é {data}.")

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
