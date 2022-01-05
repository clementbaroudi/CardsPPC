from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc
import random
import os

cloche = Lock()
semaphore = Semaphore(0)

""" etats player"""

class Stateplayer:
    wait = 1
    echange = 2
    faire_offre = 3
    Sonner_cloche = 4




def Player(i, ):
    while True :

        #wait
        if state[i] == 1:
            showcartes(i)
            showechanges()
            supp = input("Voulez-vous supprimer une de vos offres? (oui/non)")
            if supp = "oui":
                suppof = input("Laquelle?")
                m = (suppof).encode()
                mq.send(m, type = 4)

            echan = input("Voulez-vous accepter un des échanges proposés? (oui/non)")
            if echan == "oui":
                state[i] = 2
            else :
                off = input ("Voulez-vouz faire une nouvelle offre? (oui/non)")
                if off == "oui":
                    state[i] = 3
                

        #échanger ses cartes contre une offre existante
        if state[i] == 2:
            #voir la liste des offres
            m = str("ok"").encode()
            mq.send(m, type = 2)
            num = input("Quelle offre voulez-vous?")
            offre = listeechanges[num]
            nbcartes = offre[1].length() + 1

            #voir les cartes du joueur
            m = str(i).encode()
            mq.send(m, type = 1)

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
                mq.send(m, type = 5)




        #proposer une offre
        if state[i] == 3:

            showcartes(i)
            moy = input ("quel moyen de transport voulez vous echanger?")

            cartes[]  # toutes les cartes de ce moyen de transport du joueurs
            print("Combien de cartes voulez vous échanger? ( Vous en avez " + cartes.length() + ")")
            nb = int(input())
            while nb > cartes.length() or nb > 3:
                print ("Veuillez indiquer un nombre correct")
                print("Combien de cartes voulez vous échanger? ( Vous en avez " + cartes.length() + ")")
                nb = int(input())

            cartesech = cartes[0:(nb-1)] #cartes que le joueur veut échanger

            m = cartesech.encode()
            mq.send(m, type = 3)


            """occupé = True
            while occuppe == True:
                if not sem.acquire():
                    sem.release()
                    print("Un échange est déjà en cours, veuillez patienter")
                else:
                    listechanges.append([i, cartesech[]])
                    sem.release()"""

        #sonner la cloche
        if state[i] == 4:
            m = str("ok").encode()
            mq.send(m, type = 6)


#pour montrer les cartes du joueur
def showcartes(i):
    print("Voulez-vous voir vos cartes? (oui/non)")
    rep = input()
    if rep == oui:
        m = str(i).encode()
        mq.send(m, type = 1)

#afficher toutes les offres
def showechanges():
    print("Voulez-vous voir les offres? (oui/non)")
    rep = input()
    if rep == oui:
        m = str("ok"").encode()
        mq.send(m, type = 2)






def creation():
    enseignes = ["avion","voiture","train","velo","pieton"]
    valeurs = [1,2,3,4,5]
    return [(x,y) for x in enseignes for y in valeurs]

def get_carte(cartes):
    # Fonction génératrice
    NewCartes=cartes[0:5*nbJoueurs]
    sabot = random.sample(NewCartes, 5*nbJoueurs)
    while sabot:
        # tant qu'il reste des cartes dans le sabot
        yield sabot.pop()

def distribuerCartes(nbJoueurs):
	joueurs = [[] for i in range(nbJoueurs)]
	# création du générateur de cartes
	gen = get_carte(creation())
	for i in range(5):
	    for j in joueurs:
	        try:
	            j.append(next(gen))
	        except StopIteration:
	            pass
	return joueurs

def entreeClavier() :
    pass

def finPartie():
    pass

def Game():
    pass

if __name__ == "__main__":
    #Mise en place du jeu
    key=128
    queue=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    print("Serveur en service")
	nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
	Deck=distribuerCartes(nbJoueurs)
    with multiprocessing.Pool(processes = 4) as pool :
        listen=True
        while listen:
            requete,t = queue.receive()
            demande = str(requete.decode())
            if demande == "Type 1":

            elif demande == "Type 2":

            elif demande == "Type 3":

            elif demande == "Type 4":

            elif demande == "Type 5":

            elif demande == "Type 6":

            else:
                print("Requête non reconnue")
                reponse = "Requête non reconnue"
                reponse.encode()
                queue.send(reponse)
        print("Closing connexion")

    '''
	echanges = Semaphore(0)
	state = [State.wait for i in range(nbJoueurs)]
	threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]'''





for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
