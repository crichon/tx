tx
==

Gestion de commandes pour un laboratoire de biologie via django
S'appuye principalement sur l'auto-admin, voir main/models.py et main/admin.py

Auto-admin
----------

Groupes d'utilisateurs et permissions:
 - super-utilisateur: root
 - admin: peut modifier l'état des commandes, créer des fiches fournisseurs + ???
 - utilisateur: peut ajouter, modifier (et supprimer ?) des commandes d'objets sur la dernière facture en cours, ajouter des objets et catégories

Utilisateur
-----------

Peut modifier les commandes d'objets d'une commande passée uniquement pour marquer un objet comme stocké
doit aussi pouvoir rapidement copié depuis d'anciennes commandes vers la nouvelles, pour cela sélectionner les items voulues dans commandes de produits et utiliser l'action appropriée

Admin
-----

Changer l'état d'une commande à:
 - en attente de réception:     géneration de factures prêtes à envoyées et crée une nouvelle commande courante.
 - annulée:                     crée une nouvelle commande courante, supprime l'ancienne ??
 - archivée                     ne fait rien, marque la fin du traitement d'une commande, normalement déclenché lorsque tous les objets d'une commande ont été correctement stockés

Vue publique
------------

Si temps, voir du coté de d3.js pour faire des visualisations sur les consommations du labo

Qui serait éventuellement
-------------------------

Gérer les prix, le labo n'est pas intéresser donc ...

