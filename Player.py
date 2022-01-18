from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc
import os

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

""" etats player

    wait = 1
    echange = 2
    faire_offre = 3
    Sonner_cloche = 4
    Supprimer_offre = 5
    """


def letsGo(i):
    global state
    #wait

    if state == 1:
        entreeKo = True
        while entreeKo:
            entreeKo = False
            touche = input("Que voulez vous faire?\n\nv : voir vos cartes \no : voir les offres en cours \na: ajouter une offre\ns : supprimer une offre\ne: accepter une offre\nc : sonner la cloche\n")
            if touche == "v":
                showcartes(i)


            elif touche == "o":
                showechanges(i)


            elif touche == "s":
                state = 5



            elif touche == "a":
                state = 3

            elif touche == "c":
                state = 4


            elif touche == "e":
                state = 2

            else :
                print("\nVeuillez entrer une valeur correcte")
                entreeKo = True


    #échanger ses cartes contre une offre existante
    elif state== 2:
        #voir la liste des offres
        nbOffres,nbcartes, list_offresJoueur = showechanges(i)
        nbcartes_int = int(nbcartes)
        nbOffres_int = int(nbOffres)

        if nbOffres_int == 0:
            print("\nVous ne pouvez pas faire d'échange")
        else:
            while True:
                try:
                    numOff = int(input("\nQuelle offre voulez-vous? (la première vaut 1)"))
                    break
                except ValueError:
                    print("\nEntrez une valeur correcte")
            while numOff in list_offresJoueur:
                numOff = int(input("\nVous ne pouvez pas accepter votre propre offre"))

            while numOff > nbOffres_int or numOff < 1:
                numOff = int(input("\nLe nombre entré n'est pas valide. \nQuelle offre voulez-vous? (la première vaut 1)"))

            #voir les cartes du joueur
            showcartes(i)
            NotSure = True
            while NotSure :
                print("\nNombre de cartes :")
                print(nbcartes)
                cartesoff = []
                print("\nQuelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                print("ATTENTION: si la carte est déjà dans une offre, cette offre sera supprimée")
                while True:
                    try:
                        nb = int(input())
                        break
                    except ValueError:
                        print("\nEntrez une valeur correcte")
                while nb > 5 or nb < 1 :
                    print ("\nVeuillez indiquer un nombre correct")
                    print("\nQuelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                    nb = int(input())
                cartesoff.append(nb)


                if int(nbcartes) > 1:
                    print("\nQuelle est la deuxième carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                    while True:
                        try:
                            nb2 = int(input())
                            break
                        except ValueError:
                            print("\nEntrez une valeur correcte")
                    while nb2 > 5 or nb2 < 1 or nb2 == nb:
                        print ("\nVeuillez indiquer un nombre correct")
                        print("\nQuelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                        nb2 = int(input())
                    cartesoff.append(nb2)


                    if int(nbcartes) > 2:
                        print("\nQuelle est la troisième carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                        while True:
                            try:
                                nb3 = int(input())
                                break
                            except ValueError:
                                print("\nEntrez une valeur correcte")

                        while nb3 > 5 or nb3 < 1 or nb3 == nb or nb3 == nb2:
                            print ("\nVeuillez indiquer un nombre correct")
                            print("\nQuelle est la première carte que vous voulez échanger? (chiffre entre 1 et 5 )")
                            nb3 = int(input())
                        cartesoff.append(nb3)

                cartesoff_str = ""
                for carte in cartesoff:
                    cartesoff_str += str(carte) + "?"
                print(cartesoff)
                print(cartesoff_str)
                while True:
                    ok = input("\nVoulez-vous échanger vos cartes ? (oui / non)")
                    if ok == "non":
                        NotSure = True
                        break
                    elif ok == "oui" :
                        NotSure = False
                        break
                    else :
                        print("\nentrez une valeur correcte")


                m = "5" + "/" + str(i) + "/" +  str(numOff) + "/" + cartesoff_str
                m_encode = m.encode()
                Queue.send(m_encode)

        state = 1


    #proposer une offre
    elif state == 3:
        list_moyen = showcartes(i)
        print(list_moyen)
        moy = input ("\nQuel moyen de transport voulez vous echanger?")
        while moy not in list_moyen:
            print("Votre entrée n'est pas valide")
            moy = input ("\nQuel moyen de transport voulez vous echanger?")
        mess = "3" + "/" + str(i) + "/" + moy
        print(mess)
        text = mess.split("/")
        print(type(text))
        m = mess.encode()
        Queue.send(m)
        moyens_offre.append(moy)
        print(moyens_offre)
        print("\nVotre offre a été ajoutée")
        state = 1






    #sonner la cloche
    elif state == 4:
        m = str("6 " + "/" + str(i)).encode()
        Queue.send(m)



    #supprimer une offre
    elif state == 5:
        nbOffres, list_moyen = showplayeroffer(i)
        if nbOffres == 0:
            state = 1
        else :

            suppof = input("\nLaquelle? (entrez le moyen de transport)\n")
            while suppof not in list_moyen:
                ("\nCette offre n'existe pas")
                suppof = input("\nLaquelle? (entrez le moyen de transport)\n")
            print("\nOffre supprimée")
            moyens_offre.remove(suppof)
            print(moyens_offre)
            message = "4" + "/" +  str(i) + "/" + str(suppof)
            m = message.encode()
            Queue.send(m)
            state = 1

    return state

"""pour montrer les cartes du joueur"""
def showcartes(i):
    num = str("1" + "/" + str(i)).encode()
    Queue.send(num)
    listen = True
    while listen:
        requete,t = Queue.receive()
        mess = str(requete.decode())
        message= mess.split("/")
        type = message[0]
        if message:

            if message[1] == str(i):
                if type == "7":
                    list_moyen = []
                    print("\nVos cartes sont:")
                    cartes_str = ""
                    cards = message[2]
                    splitcartes = cards.split(";")
                    for carte in splitcartes:
                        if carte != "":
                            cartes_str += carte + " ; "
                            splitmoyen = carte.split(",")
                            print(splitmoyen)
                            cartes_str += splitmoyen[0] + " , " + splitmoyen[1] + " | "
                            if splitmoyen[0] not in list_moyen:
                                list_moyen.append(splitmoyen[0])

                    """print(cards)"""

            listen = False
    return list_moyen



""" afficher tous les échanges proposés"""
def showechanges(i):

    num = str("2" + "/" + str(i)).encode()
    Queue.send(num)
    listen = True
    while listen:
        requete,t = Queue.receive()
        mess = str(requete.decode())
        message= mess.split("/")
        type = message[0]
        if message:
            if type == "8":
                print("\nOffres recues")
                string = ""
                #on sépare les différentes offres
                splitjoueurs = message[1].split("_")
                nbcartes = 0
                nbOffres = 0
                list_offresJoueur = []
                for e in splitjoueurs:
                    if e == "-1":
                        string += "Il n'y a pas d'offres"
                    elif e != "" :
                        # on sépare le joueur et ses cartes
                        splitjoueurcarte = e.split("|")

                        string += " Joueur " + splitjoueurcarte[0] + " : "
                        if int(splitjoueurcarte[0]) == i :
                            list_offresJoueur.append(splitjoueurs.index(e) + 1)
                        #on sépare les cartes et le nombre de cartes
                        splitcartesnombre = splitjoueurcarte[1].split("!")
                        nbcartes = splitcartesnombre[1]
                        #on sépare chaque carte
                        splitcartes = splitcartesnombre[0].split(";")



                        for f in splitcartes:
                            if f != '':
                                string += f + "; "

                        string += "   nombre de cartes : " + nbcartes + "\n"
                        nbOffres= message[2]

                print(string)
            listen = False

    return (nbOffres, nbcartes, list_offresJoueur)


#pour voir seulement les échanges du joueur
def showplayeroffer(i):

    num = str("2" + "/" + str(i)).encode()
    Queue.send(num)
    listen = True
    NoOffer = False
    while listen:
        requete,t = Queue.receive()
        mess = str(requete.decode())
        message= mess.split("/")
        type = message[0]
        if message:
            if type == "8":
                string = "Vos offres sont :"
                splitjoueurs = message[1].split("_")
                list_moy = []
                # e = _numjoueur|moyen1,numcarte1;moyen1, numcarte2;!nbcartes
                for e in splitjoueurs:
                    if e != '':

                        splitjoueurcarte = e.split("|")
                        # g = [_numjoueur ; (moyen1,numcarte1;moyen1, numcarte2;!nbcartes)]
                        if splitjoueurcarte[0] == str(i):
                            splitnbcartes = splitjoueurcarte[1].split("!")
                            #splitnbcartes = [(moyen1,numcarte1;moyen1, numcarte2) ; (nbcartes)]
                            splitcartesmoyens = splitnbcartes[0].split(";")
                            #splitcartesmoyens = [(moyen1,numcarte1);(moyen1, numcarte2)]
                            for f in splitcartesmoyens:
                                if f != '':
                                    moyencarte = f.split(",")
                                    moyen = moyencarte[0]
                                    if moyen not in list_moy:
                                        list_moy.append(moyen)
                                    string += f + "; "
                            string += "\n"

                        if string == "Vos offres sont :":
                            string = "Vous n'avez pas d'offre en cours"
                            NoOffer = True
                        string += "\n"
                print(string)
            listen = False
    nbOffresj= message[2]
    if NoOffer :
        return (0,0)
    else:
        return (nbOffresj,list_moy)


if __name__ == "__main__":
    moyens_offre = []
    pid = os.getpid()
    m = str("0" + "/" + str(pid)).encode()
    i = 0
    print("Connexion établie avec le serveur, en attente d'autres joueurs...")
    Queue.send(m)

    # pour recevoir le num du joueur
    numRecu = True
    while numRecu:
        m , t= Queue.receive()
        mess = m.decode()
        if mess:
            message = mess.split("/")
            if message[0] == "9" :
                if message[1] == str(pid):
                    i = int(message[2])
                    print("\nVous êtes le joueur " + str(i) + ". \nJe vous souhaite la bienvenue !")
                    numRecu = False
            else:
                Queue.send(m)

    JoueursConnectes = False
    while JoueursConnectes == False:
        m , t= Queue.receive()
        mess = m.decode()
        if mess:
            message = mess.split("/")
            if message[0] == "11" :
                print("\nTous les joueurs sont connectés, la partie peut commencer.\n")

                JoueursConnectes = True
            else :
                Queue.send(m)

    while True:
        letsGo(i)
