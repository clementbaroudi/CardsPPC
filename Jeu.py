from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc

cloche = Lock()
semaphore = Semaphore(0)
Queue = sysv_ipc.MessageQueue(key)








class Carte:

	def __init__(self, MoyenDeTransport, Valeur):
		self.MoyenDeTransport=MoyenDeTransport
		self.Valeur=Valeur

def distribuerCartes(nbJoueurs):


def entreeClavier() :
    pass

def finPartie():
    pass

def Game():
    pass

if __name__ == "__main__":

    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    echanges = Semaphore(0)
    state = [State.wait for i in range(nbJoueurs)]
    threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]


for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
