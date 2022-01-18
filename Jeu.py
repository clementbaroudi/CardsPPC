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
9: attribuer num du joueur en debut de partie
10 : envoi gagner la partie
11 : debut partie
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

            #voir cartes
            if type == "1":

                cartes.acquire()
                print("envoi des cartes")
                cartesjoueur = Deck[int(i)]

                message = "7" + "/" + str(i) + "/"
                for o in range(5):
                    message += str(cartesjoueur[o][0]) + "," +str(cartesjoueur[o][1]) + ";"
                m = message.encode()
                Queue.send(m)
                print("envoi ok")
                print(message)
                cartes.release()



            # voir offres
            elif type == "2":
                """format :
                8/_numjoueur|moyen1,numcarte1;moyen1, numcarte2;!nbcartes_numjoueur|moyen2, numcarte1 _numjoueur .../nbOffres
                / sépare les entrées
                _ sépare les joueurs
                | sépare les cartes des joueurs
                ; sépare les cartes
                ! sépare les moyens

                """
                echanges.acquire()
                print("envoi des offres")

                message = "8" + "/"
                nbOffres = len(listeechanges)
                if listeechanges == []:
                    message += "-1"
                else :
                    for e in listeechanges:
                        message +=  str(e[0]) + "|"

                        for j in e[1]:
                            message += str(j[0]) + "," +  str(j[1]) + ";"
                        message += "!" + str(e[2]) #nb cartes
                        message+= "_"
                message += "/" + str(nbOffres)
                m = message.encode()
                Queue.send(m)
                print(message)
                print("envoi ok")
                print(listeechanges)
                echanges.release()


            #ajouter offre
            elif type == "3":
                print("ajout en cours")
                moy = message[2]
                echanges.acquire()
                print("semaphore ouvert")
                #format cardex : [(moyen, num),(moyen,num),(moyen,num)]
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
                print(listeechanges)
                echanges.release()
                print("ajout OK")


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



            #accepter une offre et echanger des cartes
            elif type == "5":
                # type / i / num offre / liste cartes
                cartes.acquire()
                echanges.acquire()

                i_offre = listeechanges[int(message[2])-1][0]
                print("i offre " + i_offre)

                #liste des cartes de l'offre
                listOf = listeechanges[int(message[2])-1][1]
                print("listof")
                print(listOf)
                i_offre_int = int(i_offre)
                listEx = []
                numcartes = message[3].split("?")
                #liste des cartes de l'echange
                for t in numcartes:
                    if t != "":
                        #on ajoute la t ième carte du joueur dans le liste des cartes à échanger
                        listEx.append(Deck[int(i)][int(t)-1])
                print("listEx")
                print(listEx)
                #changer les cartes du joueur qui a fait l'offre
                k = 0
                print(Deck[i_offre_int])

                for e in Deck[i_offre_int]:
                    for f in listOf:
                        if f == e:
                            print(Deck[i_offre_int].index(e))
                            print(k)
                            Deck[i_offre_int][Deck[i_offre_int].index(e)] = listEx[k]
                            k += 1
                print(Deck[i_offre_int])

                #changer les cartes de l'autre joueur:
                k = 0
                print(Deck[int(i)])
                for e in Deck[int(i)]:

                    for f in listEx:


                        if f == e:
                            print("carte echangee")
                            Deck[int(i)][Deck[int(i)].index(e)] = listOf[k]
                            k += 1
                print(Deck[int(i)])

                #on vérifie que les cartes ne soient pas dans une autre offre
                print("verification offre en cours")
                for echange in listeechanges :
                    if echange[0] == int(i):
                        for cartes_echange_en_cours in listEx:
                            for cartes_echange_existantes in echange[1]:
                                if cartes_echange_en_cours == cartes_echange_existantes:
                                    print("la carte etait dans une offre")
                                    listeechanges.remove(echange)



                # on enlève l'offre
                listeechanges.remove(listeechanges[int(message[2])-1])

                cartes.release()
                echanges.release()

            #a faire
            # sonner la cloche
            elif type == "6":
                cartes.acquire()
                print("verification ")
                moy = Deck[i][0]
                c = 0
                for e in Deck[i:i+5]:
                    if e[0] != moy:
                        print("Vous n'avez pas 5 cartes identiques, continuez la partie")

                    else:
                        c += 1
                cartes.release()
                if c == 5:
                    clock.acquire()
                    cloche = True
                    print("Le joueur " , i , "remporte la partie!")
                    clock.release()

            elif type == "7":
                Queue.send(requete)

            elif type == "8":
                Queue.send(requete)

            elif type == "9":
                Queue.send(requete)

            elif type == "10":
                Queue.send(requete)




if __name__ == "__main__":
    #Mise en place du jeu
    cartes = Semaphore()
    echanges = Semaphore()
    listeechanges = []
    print("Serveur en service")
    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    pidJoueurs = []

    # on attend que tous les joueurs se connectent
    r = True
    nbStart = -1
    while r:
        m , t= Queue.receive()
        mess = m.decode()
        if mess:
            message = mess.split("/")
            if message[0] == "0" :
                nbStart += 1
                pidJoueurs.append(message[1])
                reponse = "9" + "/" + message[1] + "/" + str(nbStart)
                rep = reponse.encode()
                Queue.send(rep)
                print("Joueur " + str(nbStart) + " connecté")
                print(pidJoueurs)
            else:
                Queue.send(m)

        if nbStart == nbJoueurs-1:
            print("Tous les joueurs se sont connectés, la partie peut commencer")
            for pid in pidJoueurs:
                debutpartie = ("11" + "/" + pid).encode()
                Queue.send(debutpartie)
                print("debut envoyé")
            r = False

    Deck=distribuerCartes(nbJoueurs)


    #listeechanges = [[i, liste cartes], ...]
    print(Deck)
    threads = [threading.Thread(target = Game, args = (i, )) for i in range(nbJoueurs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    if clock == True:
        Queue.remove()
