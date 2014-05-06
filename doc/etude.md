Système de gestion pour un laboratoire de biologie
==================================================
*Réalisé dans le cadre d'une TX pour l'Université de Technologie de Compiègne*


Intoduction
-----------

La laboratoire de biologie de l'utc shouaite un système permettant de faciliter et centraliser les commandes de matériels et leur suivi.


Etude de l'existant
-------------------

Actuellement, une personne et en charge de la centralisation des commandes (l'administrateur), il récupere et traite l'ensemble des demandes de matériels, transmises principalement sous forme de documents manuscrits non structurés. Il va ensuite génerer des fichiers sous format xls (fichier excel) fesant office de bon de commande.
Pour chaque objets fesant l'office d'une requête, l'administrateur est en charge de trouver le fournisseur le plus adéquat, puis de génerer un fichier excel par fournisseur, contenant l'ensemble des produits voulues disponibles dans le stock du dit fournisseur.

Les commandes de produits se font suivant une fréquence variable. Pour le moment l'administrateur choisi une date de manière arbitraire à partir de laquelle il valide la commande courante, entamme le processus d'envoie et dresse une nouvelle liste pour la commande suivante. La taille d'une commande peut varier de quelques objets à une centaine.

A la réception d'une commande, la personne en charge des stocks annonce la réception du matériel et notifie les personnes concernées. Ces personnes doivent alors s'occuper du stockage des objets.

Cette organisation naturelle présente quelques inconvénients majeurs. Il est difficille de garder une trace exhaustive de l'ensemble du matériel, elle nécessite beaucoup d'interactions humaines et donc, est source de nombreux quipropos, qui a stocké quels matériels, quand, quelles produits sont manquants dans la commande, etc...


Objectifs de la solution visée
------------------------------

Un premier point concerne la *centralisation* des informations et la *traçabilitée*. L'utilisation d'une interface commune permet à chacun de connaître l'état d'une commande, quels sont les produits actuellement présent dans la futur commmande, et de maintenir un historique des opérations dans le système. On devra pouvoir savoir qui à fait quoi, quand et pour qui (un besoin soulevé et celui de pouvoir éffectuer des actions pour d'autres utilisateurs, dues à la mobilité horaire du personelle).
En conséquence, il est impératif de garantir l'intégrité des données. Les commandes validées ne doivent pas être modifiable et archivées de manière à faciliter leurs consultations ultérieures.

Dans un second temps, il serait appréciable d'automatiser la création de factures (fichier xls) en fonctions des différents fournisseur, afin de simplifier le travail de l'administrateur.

Enfin, afin de ne pas trop perturber les habitudes des chercheurs, il faut que le système soit le plus agréable et simple d'utilisation que possible.


Solution envisagée
------------------

 * google docs
 * site web
 * système distribué


Scénarios d'utilisations
------------------------


Choix techniques et justifications
----------------------------------


Méthode de travail
------------------


Conclusion
----------

Produit devellopé
=================

Models et gestion des états
---------------------------

Groupes et droits
-----------------

Interface et fonctionnalitées
-----------------------------



