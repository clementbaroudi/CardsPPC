from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc

state = 1
""" touches
s : supprimer
a : ajouter
c : Sonner_cloche
v = voir carte
o = voir offres
e = echanger
"""


key = 42
Queue=sysv_ipc.MessageQueue(key)

""" etats player"""

class Stateplayer:
    wait = 1
    echange = 2
    faire_offre = 3
    Sonner_cloche = 4


def letsGo(i):
    global state
    #wait
    if state == 1:
        touche = input("que voulez vous faire?")
        if touche == "v":
            showcartes(i)


        elif touche == "o":
            showechanges(i)


        elif touche == "s":
            suppof = input("Laquelle? (entrez le moyen de transport)")
            message = "4" + "/" +  str(i) + "/" + str(suppof)
            m = message.encode()
            Queue.send(m)


        elif touche == "a":
            state = 3

        elif touche == "c":
            message = "6" + "/" + str(i)
            m = message.encode()
            Queue.send(m)


        elif touche == "e":
            state = 2


    #échanger ses cartes contre une offre existante
    elif state== 2:
        #voir la liste des offres
        showechanges(i)


        num = input("Quelle offre voulez-vous? (la première vaut 1)")


        #voir les cartes du joueur
        showcartes(i)

        print("Quelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
        nb = int(input())
        while nb > 5 or nb < 1:
            print ("Veuillez indiquer un nombre correct")
            print("Quelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
            nb = int(input())

        if nbcartes > 1:
            print("Quelle est la deuxième carte que vous voulez échanger? (chiffre entre 1 et 5 )")
            nb2 = int(input())
            while nb2 > 5 or nb2 < 1 or nb2 == nb:
                print ("Veuillez indiquer un nombre correct")
                print("Quelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                nb2 = int(input())

                if nbcartes > 2:
                    print("Quelle est la troisième carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                    nb3 = int(input())
                    while nb3 > 5 or nb3 < 1 or nb3 == nb or nb3 == nb2:
                        print ("Veuillez indiquer un nombre correct")
                        print("Quelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                        nb3 = int(input())

            cartesoff = (nb, nb2, nb3)
            m = cartesoff.encode()
            Queue.send(m, type = 5)




    #proposer une offre
    elif state == 3:
        print(state , i)
        showcartes(i)
        moy = input ("quel moyen de transport voulez vous echanger?")
        mess = "3" + "/" + str(i) + "/" + moy
        print(mess)
        text = mess.split("/")
        print(type(text))
        m = mess.encode()
        Queue.send(m)

        print("votre offre a été ajoutée")
        state = 1






    #sonner la cloche
    elif state== 4:
        m = str("6 " + "/" + str(i)).encode()
        Queue.send(m)

    print("state" , state)
    return state

"""pour montrer les cartes du joueur"""
def showcartes(i):
    num = str("1" + "/" + str(i)).encode()
    Queue.send(num)
    print("demande envoyée")
    listen = True
    while listen:
        requete,t = Queue.receive()
        mess = str(requete.decode())
        message= mess.split("/")
        type = message[0]
        if message:
            print("cartes recues")
            if type == "7":
                cards = message[1]
                print(cards)
            listen = False



""" afficher tous les échanges proposés"""
def showechanges(i):

    num = str("2" + "/" + str(i)).encode()
    Queue.send(num)
    print("demande envoyée")
    listen = True
    while listen:
        requete,t = Queue.receive()
        mess = str(requete.decode())
        message= mess.split("/")
        type = message[0]
        if message:

            if type == "8":
                print("offre recues")
                cards = message[1]
                print(cards)
            listen = False
    nbcartes = message[2]



if __name__ == "__main__":
    m = str("0" + "/" + "start").encode()
    # à faire : serveur envoie num du joueur

    print("start")
    Queue.send(m)
    print("commencer")

    while True:
        letsGo(0)
