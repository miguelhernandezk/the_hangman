import colorama
from colorama import Fore
from colorama import Style
import random
import os
import unidecode

HANGMANPICS = ['''
      +---+
      |   |
      |
      |
      |
      |
   =========''', '''
      +---+
      |   |
      |   😳
      |
      |
      |
   =========''', '''
      +---+
      |   |
      |   😳
      |   |
      |
      |
   =========''', '''
      +---+
      |   |
      |   😖
      |  /|
      |
      |
   =========''', '''
      +---+
      |   |
      |   🥵
      |  /|\\
      |
      |
   =========''', '''
      +---+
      |   |
      |   🥵
      |  /|\\
      |  /
      |
   =========''', '''
      +---+
      |   |
      |   😵
      |  /|\\
      |  / \\
      |
   =========''']

alphabet = {"a": "A", 
           "b": "B", 
           "c": "C",
           "d": "D",
           "e": "E",
           "f": "F",
           "g": "G",
           "h": "H",
           "i": "I",
           "j": "J",
           "k": "K",
           "l": "L",
           "m": "M",
           "n": "N",
           "ñ": "Ñ",
           "o": "O",
           "p": "P",
           "q": "Q",
           "r": "R",
           "s": "S",
           "t": "T",
           "u": "U",
           "v": "V",
           "w": "W",
           "x": "X",
           "y": "Y",
           "z": "Z"
        }

def print_hangman(hangman_status):
    # De un archivo a parte leemos la presentación del juego y las intrucciones. Mostramos el estatus del hangman.
    # Con colorama podemos poner colores al texto en consola
    with open("./archivos/header.txt", "r", encoding="utf-8") as f:
        for line in f:
            print(Fore.BLUE + Style.BRIGHT + line.replace("\n", "") + Style.RESET_ALL)
    print(HANGMANPICS[hangman_status])
    if hangman_status == 0:
        print(Fore.GREEN + Style.BRIGHT + "Emojibert is safe... 🥳" + Style.RESET_ALL)
    elif hangman_status <  4:
        print(Fore.YELLOW + Style.BRIGHT + "It seems Emojibert is suffering 😥" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "Emojibert will not resist for longer! HURRY UP! 🥴" + Style.RESET_ALL)


def hangman():
    # Se inicializa la lista que contendrá las palabras que se lean del archivo data
    words = []
    game_over = False
    hangman_status = 0
    guessed_word = []
    previous_status_word = []
    win_game = False

    print_hangman(hangman_status)

    # Se leen las palabras del archivo "data" y se almacenan en la lista que creamos antes
    with open("./archivos/data.txt", "r", encoding="utf-8") as fdata:
        for line in fdata:
            words.append(line.replace("\n", ""))

    # Se obtiene una palabra al azar para poder jugar. 
    game_word = words[random.randint(0,len(words)-1)]
    print("\n" + game_word + "\n")
    
    # Se ponen guiones bajjos por cada letra en la palabra elegida al azar
    for i in range(len(game_word)):
        guessed_word.append("_  ") # Almacena las letras que va adivinando el usuario
        previous_status_word.append("_  ") # Utilizado para comprobar cambios (y así saber si se han adivinado nuevas letras)
    
    # Mientras el usuario no haya perdido o ganado
    while game_over == False and win_game == False:
        os.system("clear") # Limpiamos pantalla
        print_hangman(hangman_status) # Imprimimos instrucciones y "ahorcado" nuevamente
        
        # Descomenta la siguiente línea de código para ver la palabra elegida en la consola:
        # print("\n" + game_word + "\n")

        # Imprimimos un guión bajo por cada letra en la palabra. Después imprimimos 
        # las letras del alfabeto que aun no ha introducido el usuario
        for i in range(len(game_word)):
            print(guessed_word[i], end = "")
        print("\n")
        for key, value in alphabet.items():
            print(Fore.CYAN + Style.BRIGHT + value+"\u0332  " + Style.RESET_ALL, end = "")

        # Le pedimos al usuario que introduzca una letra y le quitamos acentos en caso de que la ponga con acentos.
        # Le impedimos que ingrese números
        user_input = unidecode.unidecode(input("\nEnter one letter: "))
        assert user_input.isnumeric() == False, "Why on earth would you enter a number? Now Emojibert is dead and his soul will haunt you for the rest of your life 😵 -> 💀 -> 👻"
        
        # Si la letra que introdujo el usuario está dentro de la palabra aleatoria, 
        # la rellenamos para mostrarle al usuario que adivinó/descubrió una letra
        for i in range(len(game_word)):
            if user_input.lower() == unidecode.unidecode(game_word[i]):
                guessed_word[i] = game_word[i].upper() + "  "

        # Eliminamos la letra que introdujo el usuario para ayudarlo a adivinar
        for key, value in alphabet.items():
            if key == unidecode.unidecode(user_input.lower()):
                alphabet[key] = "_"
        
        # Comparamos cadenas para ver si ha habido cambios
        # Si hay cambios, significa que el usuario descubrió una nueva letra
        # Si no hay cambios, significa que el usuario no descubrió ninguna letra, por lo
        #   que debemos incrementar el contador hangman_status para imprimir una nueva parte del hangman
        if set(previous_status_word) == set(guessed_word):
            hangman_status += 1

        # Actualizamos la cadena a comparar para el siguiente ciclo
        previous_status_word = [i for i in guessed_word]

        # Revisamos qué es lo que ha adivinado el usuario.
        for i in range(len(guessed_word)):
            # Si alguno de los caracteres sigue siendo guión bajo, es porque no ha adivinado todas las falabras. 
            if guessed_word[i] == "_  ":
                win_game = False
                break
            # en otro caso, si llegas al final dela cadena y ningun caracter es un espacio en blanco o guion bajo, es que ganaste. 
            elif guessed_word[i] == previous_status_word[i] and i == len(guessed_word) - 1:
                win_game = True
        
        # Dado que el hangman tiene 6 partes, si alcanzamos este limite entonces perdemos
        if hangman_status >= 6:
            game_over = True
    
    # Salimos del while solo si ganamos o perdemos. Imprimimos cómo quedó el hangman al final del juego
    print_hangman(hangman_status)
    if hangman_status >= 6:
        print(Fore.RED + Style.BRIGHT + "\nYou didn't make it on time. Now Emojibert is dead and his soul will haunt you 'till the end of time 😵 -> 💀 -> 👻" + Style.RESET_ALL)
    else:
        print_hangman(0)
        print(Fore.MAGENTA + Style.BRIGHT + "\nYou saved Emojibert. He fell in love with you 😍." + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "Now you are married 👰🏻‍♀️👨🏻‍⚖️" + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "And you have a beautiful baby 👉🏼 👶🏽, Congrats, soldier!" + Style.RESET_ALL)


        



def run():
    colorama.init()
    hangman()


if __name__ == '__main__':
    run()