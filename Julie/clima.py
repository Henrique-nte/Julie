import requests
import os
from datetime import datetime, timedelta
from voz import falar_async
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_KEY")
CIDADE = "Jaraguá do Sul"

URL = "https://api.openweathermap.org/data/2.5/forecast"

# dia: 'hoje' ou 'amanha'
def obter_previsao(dia='hoje'):
    try:
        params = {
            'q': CIDADE,
            'appid': API_KEY,
            'lang': 'pt_br',
            'units': 'metric'
        }
        resposta = requests.get(URL, params=params).json()
        


        if resposta.get("cod") != "200":
            falar_async("Não consegui obter a previsão do tempo.")
            print("Não consegui obter a previsão do tempo.")
            return

        agora = datetime.now()
        alvo = agora if dia == 'hoje' else agora + timedelta(days=1)
        data_alvo = alvo.strftime('%Y-%m-%d')

        previsoes = [item for item in resposta["list"] if item["dt_txt"].startswith(data_alvo)]
        if not previsoes:
            falar_async("Sem dados de previsão disponíveis.")
            print("Sem dados de previsão disponíveis.")
            return

        temp = previsoes[0]['main']['temp']
        clima = previsoes[0]['weather'][0]['description']

        falar_async(f"A previsão para {dia} em {CIDADE} é de {clima}, com temperatura de {temp:.0f} graus Celsius.")
        print(f"A previsão para {dia} em {CIDADE} é de {clima}, com temperatura de {temp:.0f} graus Celsius.")

    except Exception as e:
        print("Erro ao obter previsão:", e)
        falar_async("Houve um erro ao buscar a previsão do tempo.")
