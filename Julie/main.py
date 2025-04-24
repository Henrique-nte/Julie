import os
from voz import falar, ouvir, saudacao
from spotify import tocar_musica, pausar, continuar, mudar_volume, spotify

def main():
    saudacao()

    while True:
        comando = ouvir().lower()

        if comando == 'no sound':
            continue

        if 'spotify tocar' in comando:
            query = comando.replace('spotify tocar', '').strip()
            tocar_musica(spotify, query)

        elif 'spotify pause' in comando:
            pausar(spotify)

        elif 'spotify continue' in comando:
            continuar(spotify)

        elif 'mude volume para' in comando:
            try:
                volume = int(comando.replace('mude volume para', '').strip())
                mudar_volume(spotify, volume)
            except:
                falar('Volume inválido.')

        elif 'ajuda' in comando:
            falar('Você pode dizer: spotify tocar, spotify pause, spotify continue, ou mude volume para 50.')

if __name__ == "__main__":
    main()