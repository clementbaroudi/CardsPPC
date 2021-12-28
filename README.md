Baroudi Clément
Rosalie Biedermann
3TC G1

# Projet PPC - Cambiecolo


Principe: 

L’objectif est d’avoir 5 cartes du même moyen de transport en échangeant nos cartes avec les autres joueurs.
Il y a autant de moyens de transport que de joueurs (au max 5: avion, voiture, train, vélo, à pied), c’est-à-dire, pour 3 joueurs il y a donc 15 cartes en jeu.  Chaque joueur reçoit 5 cartes au hasard.
Les joueurs procèdent à des échanges de cartes : ils peuvent échanger 1 à 3 cartes identiques sans préciser de quel transport il s’agit. Le premier joueur intéressé par l’échange récupère les cartes et donne autant de ses cartes en échange.. 
Une cloche est placée au milieu des joueurs : le premier qui réunit 5 cartes identiques la fait sonner pour indiquer sa victoire et remporte les points associés à son moyen de transport.


Design:

Processus:

game : gère le déroulement du jeu, c’est-à-dire les différentes offres d’échanges et la cloche

player: interagit avec l’utilisateur, game et les autres player; gère la main du joueur et lui permet de faire et recevoir des offres d’échanges


Les offres courantes sont stockées dans une mémoire partagée ( → Semaphore) accessible aux player pour qu’ils puissent mettre à jour leurs offres et voir les offres des autres player. La communication entre les player se fait dans une message queue.













Etats game:

Début de partie : attend nombre de joueurs
nombre de joueurs entré -> crée les thread player qui correspond au nombre de joueurs et créer le deck de cartes et distribue les cartes
Implémente la file d’attente
wait : attend une offre d’échanges
Reçoit une offre d’échange                             Boucle while cloche==false
Déclarer que l’offre a été acceptée     
Faire l’échange de cartes
enlever les cartes échangées de la queue
Fin: un joueur a sonné la cloche





















Etats player:

wait : montre les cartes au joueur et lui montre les offres d’échange
le joueur fait une offre → il ajoute l’échange dans la shared memory
le joueur accepte une offre → demande au joueur quelles carte il veut échanger
cartes entrées → on bloque le sémaphore, on met à jour les cartes du joueur, on vérifie si les cartes échangées sont pas dans une offre
une offre du joueur est acceptée (flag de game) → on met à jour les cartes avec les cartes échangées
les 5 cartes sont identiques → ring bell



 








Points supplémentaires :

• les relations entre les processus (parent-enfant ou non liés) 

Le processus game crée autant de threads du processus player qu’il y a de joueurs. 

• les messages échangés entre les processus ainsi que leurs types 
RING BELL : boolean stocké dans un Lock 
MAKE OFFER : boolean stocké dans un Sémaphore
QUEUE : tableau stocké dans un Sémaphore

• les structures de données stockées dans la mémoire partagée et leur mode d'accès 

Les offres sont sous la forme d’une liste ( entier numéro joueur, entier nombre cartes, cartes ,...). Toutes les offres sont stockées dans un sémaphore accessible par un seul thread à la fois.

• signaux échangés entre les processus, le cas échéant, et leurs types 
On n’utilise pas de signaux, pour la communication inter-process

• tubes impliqués dans la communication de processus par paires, le cas échéant, et leurs types
On va utiliser des pipes pour les échanges de cartes, pour la communication entre les processus game et player.


Plan d’implémentation : 

Nous commencerons par créer une structure carte qui a deux attributs : un attribut “moyen de transport” qui vaut avion, train, voiture, vélo ou chaussures et un entier compris entre 1 et 5. Une carte sera donc de la forme avion 3, voiture 1, …
Ensuite, on implémentera  player et game sans les sémaphores et on effectuera des tests avec seulement 2 joueurs pour s’assurer de la bonne communication entre les 2 processus.
On pourra ensuite ajouter les sémaphores et tester à nouveau avec 2 joueurs.
Une fois qu’ils n’y aura plus d’erreurs, on testera avec plus de 2 joueurs pour observer le comportement du message queue et l’optimiser.

