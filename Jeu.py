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
9: envoyer nb cartes dans l'offre
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

def Game(i):
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
                echanges.acquire()
                print("envoi des offres")

                message = "8" + "/"
                if listeechanges == []:
                    message += "il n'y a pas d'offres"
                else :
                    for e in listeechanges:
                        message += "joueur " + str(e[0]) + " ->  "
                        for j in e[1]:
                            message += str(j[0]) + " " +  str(j[1]) + ";"
                        message += "\n"
                m = message.encode()
                Queue.send(m)
                print("envoi ok")
                echanges.release()


            #ok sem
            #ajouter offre
            elif type == "3":
                print("ajout en cours")
                moy = message[2]
                echanges.acquire()
                print("semaphore ouvert")
                cardex = []
                p = 0
                for e in Deck[int(i)]:
                    if e[0] == moy and p < 3:
                        p += 1
                        cardex.append(e)
                        print(cardex)
                        print(p)
                nbCartes = len(cardex)

                listeechanges.append([i, cardex, nbCartes])
                echanges.release()
                print("ajout OK")

            #ok sem
            #supprimer offre
            elif type == "4":
                # type / i / moy
                moy = message[2]
                echanges.acquire()
                print("semaphore ouvert")
                for e in listeechanges:
                    if e[0] == i and e[1][0][0] == moy :
                        print("offre trouvée")
                        listeechanges.remove(e)
                        echanges.release()
                        print("suppression ok")


            #ok sem
            #accepter une offre et echanger des cartes
            elif type == "5":
                # type / i / num offre / liste cartes
                cartes.acquire()
                echanges.acquire()

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


#marche pas
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
    Deck = [[('avion', 4), ('bateau', 1), ('bateau', 3), ('avion', 5), ('voiture', 2)]]

    #listeechanges = [[i, liste cartes], ...]
    print(Deck)
    threads = [threading.Thread(target = Game, args = (i, )) for i in range(nbJoueurs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
