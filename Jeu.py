from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc
import random
import os

"""liste types
0 : commencer partie
1: voir cartes
2: voir echanges
3: ajouetr offre
4: supprimer offre
5: accepter offre
6: sonner la cloche
7: recevoir cartes
8: recevoir listeechanges
"""

cloche = Lock()
clock = False

key=42
Queue=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)





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

def accessSem(sem):
    print("essaie d'acceder au sem")
    if not sem.acquire():
        sem.release()
        print("Veuillez patienter")


    sem.acquire()
    print("semaphore ouvert")




if __name__ == "__main__":
    #Mise en place du jeu
    cartes = Semaphore()
    echanges = Semaphore()
    listeechanges = []
    print("Serveur en service")
    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    r = True
    while r:
        m , t= Queue.receive()
        mess = m.decode()
        if mess:
            print(mess)
            r = False


    Deck=distribuerCartes(nbJoueurs)

    #listeechanges = [[i, liste cartes], ...]
    print(Deck)
    with multiprocessing.Pool(processes = 4) as pool :
        listen=True
        while listen:
            requete,t = Queue.receive()
            mess = str(requete.decode())

            if mess :
                print("message recu")
                message= mess.split("/")
                print(message)
                type = message[0]
                i = message[1]
                #a faire
                if type == "0":
                    ""
                    #compte le nb de joueurs qui entrent dans la partie et lance la partie si ça correspnd au nombre entré

                #ok sem
                #voir cartes
                elif type == "1":

                    cartes.acquire()
                    print("envoi des cartes")
                    cartesjoueur = Deck[int(i)]

                    message = "7" + "/"
                    for o in range(5):
                        message += str(cartesjoueur[o][0]) + " , " +str(cartesjoueur[o][1]) + " ; "
                    m = message.encode()
                    Queue.send(m)
                    print("envoi ok")
                    cartes.release()


                #ok sem
                # voir offres
                elif type == "2":
                    accessSem(echanges)
                    print(listeechanges)
                    echanges.release()


                #ok sem
                #ajouter offre
                elif type == "3":
                    print("ajout en cours")
                    moy = message[2]
                    echanges.acquire()
                    cardex = []
                    for e in Deck[int(i)]:
                        p = 0
                        if e[0] == moy and p < 3:
                            p += 1
                            cardex.append(e)
                    listeechanges.append([i, cardex])
                    echanges.release()
                    print("ajout OK")

                #ok sem
                #supprimer offre
                elif type == "4":
                    # type / i / moy
                    moy = message[2]
                    accessSem(echanges)
                    for e in listeechanges:
                        if e[0] == i :
                            for k in e[1]:
                                if k[1] == moy:
                                    accessS
                                    listeechanges.remove(e)
                                    echanges.release()


                #ok sem
                #accepter une offre et echanger des cartes
                elif type == "5":
                    # type / i / num offre / liste cartes
                    accessSem(cartes)
                    accessSem(echanges)
                    i_offre = listeechanges[message[2][0]]
                    listOf = listeechanges[message[2][1]]
                    listEx = message[3]
                    #changer les cartes du joueur qui a fait l'offre
                    k = 0
                    for e in Deck[i_offre:i_offre+5]:
                        for f in listOf:
                            if e == f:
                                Deck[index(e)] = listEx[k]
                                k += 1

                    #changer les cartes de l'autre joueur:
                    k = 0
                    for e in Deck[i:i+5]:
                        for f in listEx:
                            if e == f:
                                Deck[index(e)] = listOf[k]
                                k += 1

                    # on enlève l'offre
                    for e in listeechanges:
                        for f in listOf:
                            if e == f:
                                listeechanges.remove(e)

                    cartes.release()
                    echanges.release()

                #a faire
                # sonner la cloche
                elif type == "6":
                    accessSem(cartes)
                    moy = Deck[i][0]
                    c = 0
                    for e in Deck[i:i+5]:
                        if e[0] != moy:
                            print("Vous n'avez pas 5 cartes identiques, continuez la partie")
                            cartes.release()
                        else:
                            c += 1
                    if c == 5:
                        print("Bravo le joueur " , i , "remporte la partie!")



                else:
                    print("Requête non reconnue")
                    reponse = "Requête non reconnue"
                    reponse.encode()
                    Queue.send(reponse)

        print("Closing connexion")

    '''
	echanges = Semaphore(0)
	state = [State.wait for i in range(nbJoueurs)]
	threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]'''





for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
