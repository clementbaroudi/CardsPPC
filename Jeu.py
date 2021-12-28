
from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer


mutexPioche = multiprocessing.Lock()
mutexQueue = multiprocessing.Lock()

class Joueur:

    def __init__(self, identifiant, l):
    
		self.identifiant=identifiant
		self.main= l
		
	
class Carte:

	def __init__(self, couleur):
		self.couleur=couleur

def entreeClavier() :
    pass

def finPartie():
    pass


if __name__ == "__main__":
    n = int(input("Combien de joueurs y aura-t-il ?\n"))
    print(n)
