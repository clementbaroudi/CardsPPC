
from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer



class Player:

    def __init__(self, identifiant, l):
    
		self.identifiant=identifiant
		self.main= l
		
	
class Carte:

	def __init__(self, MoyenDeTransport, Valeur):
		self.MoyenDeTransport=MoyenDeTransport
		self.Valeur=Valeur

def entreeClavier() :
    pass

def finPartie():
    pass
    
class Game:
    pass

if __name__ == "__main__":

    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    
