import tweepy
import credentials
import csv
import re
import os
import os.path


auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)

api = tweepy.API(auth)

## obtains data

def followers_count():
    user_search = input("Introduce el usuario del cuál quieres saber el número de seguidores: ")
    user = api.get_user(user_search)
    return user.followers_count;

def timeline_user():
    user_search = input("Introduce el nombre del usuario para sacar su timeline: ");
    palabra = input("Buscar: ")
    numero_de_Tweets = int(input(u"Número de tweets a capturar: "))
    return tweepy.Cursor(api.search, palabra, id=str(user_search)).items(numero_de_Tweets)

def tweets_search(palabra="Trump", times=100, lenguanje="en"):
    palabra = input("Buscar: ")
    numero_de_Tweets = int(input(u"Número de tweets a capturar: "))
    lenguaje = input("Idioma [es/en]:")
    return tweepy.Cursor(api.search, palabra, lang=lenguaje).items(numero_de_Tweets)


## formatting csv text

a, b = 'áéíóúü', 'aeiouu'
trans = str.maketrans(a, b)

def remove_url(str):
    return re.sub(r"http\S+", "", str)


def removeSign(str):
    return re.sub(r"\?|(\¿)|(…)|(RT)|(\"\")|(\")|(\.)|(«)|(»)|(“)|(”) +", "", str)


def removeEnye(str):
    return re.sub(r"(n)/i", "n", str)

def strip_undesired_chars(tweet):
    stripped_tweet = tweet.replace('\n', ' ').replace('\r', '')
    char_list = [stripped_tweet[j] for j in range(
        len(stripped_tweet)) if ord(stripped_tweet[j]) in range(65536)]
    stripped_tweet = ''
    for j in char_list:
        stripped_tweet = stripped_tweet+j

    removed_url = stripped_tweet.translate(trans)
    return removeEnye(removeSign((remove_url(removed_url))))

## write csv

def write_csv_type_of_param(nombre_archivo_salida,outtweets, type):
    with open(nombre_archivo_salida, type, newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if type == "w":
            writer.writerow(['id', 'created_at', 'text',
                                'retweet_count', 'favorite_count'''])
        writer.writerows(outtweets)
    pass
def write_csv(tweets):
    nombre_archivo_salida = input("Introduce el nombre del archivo csv de salida (si el archivo ya existe se añaden los nuevos datos al mismo): ");
    outtweets = [(tweet.id_str.translate(trans), tweet.created_at, strip_undesired_chars(
        tweet.text), tweet.retweet_count, str(tweet.favorite_count)+'') for tweet in tweets]

    if os.path.isfile(nombre_archivo_salida):
        write_csv_type_of_param(nombre_archivo_salida,outtweets, "a");
    else:
        write_csv_type_of_param(nombre_archivo_salida,outtweets, "w");

## Menú de entrada

def menu():
    os.system('clear')
    print ("Tweepy data - desarrollado por susomejias")
    print ("\t1 - Obtener número de seguidores de un usuario")
    print ("\t2 - Obtener timeline de un usuario")
    print ("\t3 - Busqueda por palabra")
    print ("\t9 - salir")

def muestraMenu():

    while True:
        # Mostramos el menu
        menu()
    
        # solicituamos una opción al usuario
        opcionMenu = input("inserta un numero valor >> ")
    
        if opcionMenu=="1":
            print ("")
            print(followers_count());
            input("pulsa una tecla para continuar")
        elif opcionMenu=="2":
            print ("")
            write_csv(timeline_user());
            input("pulsa una tecla para continuar")
        elif opcionMenu=="3":
            print ("")
            write_csv(tweets_search());
            input("pulsa una tecla para continuar")
        elif opcionMenu=="9":
            break
        else:
            print ("")
            input("pulsa una tecla para continuar")

muestraMenu();
