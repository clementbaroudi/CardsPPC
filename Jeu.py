from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc
import random

key = 128
cloche = Lock()
semaphore = Semaphore(0)


Queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

value = 1
while value:
    try:
        value = int(input())
    except:
        print("Input error, try again!")
    message = str(value).encode()
    mq.send(message)

mq.remove()
    try:
        value = int(input())
    except:
        print("Input error, try again!")
    message = str(value).encode()
    mq.send(message)

mq.remove()


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

	nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
	Deck=distribuerCartes(nbJoueurs)
	for j in Deck:
		print(j)
	echanges = Semaphore(0)
	state = [State.wait for i in range(nbJoueurs)]
	threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]





for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
