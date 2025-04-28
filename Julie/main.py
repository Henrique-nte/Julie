import os
from clima import obter_previsao
from voz import falar, falar_async, ouvir, saudacao, tocar_com_verificacao
from spotify import tocar_musica, pausar, continuar, mudar_volume, ajuda, spotify


def main():
    #saudacao()

    while True:
        comando = ouvir().lower()

        if comando == 'no sound':
            continue

        if 'até mais julie' in comando:
            falar('Até logo Shelby!')
            print('Julie: Até logo Shelby!')
            break  # Isso sai do loop e termina o programa

        if 'spotify tocar' in comando:
            query = comando.replace('spotify tocar', '').strip()
            tocar_musica(spotify, query)

        elif 'spotify pause' in comando:
            print('Song pausado...')
            pausar(spotify)

        elif 'spotify continue' in comando:
            print('Song continuando...')
            continuar(spotify)

        elif 'mude volume para' in comando:
            try:
                volume = int(comando.replace('mude volume para', '').strip())
                mudar_volume(spotify, volume)
            except:
                falar_async('Volume inválido.')
                print('Julie: Volume inválido.')

        elif 'ajuda' in comando:
            falar_async('Claro Shelby.')
            ajuda()

        elif 'previsão do tempo' in comando:
            if 'amanhã' in comando:
                obter_previsao(dia='amanha')
            else:
                obter_previsao(dia='hoje')

if __name__ == "__main__":
    main()
