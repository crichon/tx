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

Todo (dsl écris suite à une session code...)
--------------------------------------------

    ID Proj Pri Due        Age Urg  Description
    -- ---- --- ---------- --- ---- ------------------------------------------------
    40 tx       2014-04-08 1d  11.5 finnish OrderAdmin save method
    43 tx   M   2014-04-24 16m 7.31 deploy somwhere
    46 tx   M   2014-04-24 9m   7.3 install bootstrap-admin
    47 tx   M   2014-04-24 8m   7.3 check for nicer list display
    49 tx   M   2014-04-24 8m   7.3 init database with a new current order
    50 tx   M   2014-04-24 7m   7.3 fix order_state and item_state, should be
                                    model.choiceField and not model.charField
    51 tx   M   2014-04-24 6m   7.3 rethink state logic to be as simple and clear as
                                    possible
    53 tx   M   2014-04-24 3m   7.3 override admin given choices in order to avoid
                                    possibilities of breaking state logic
    44 tx   L   2014-04-24 15m  5.2 mail 5000 python host
    45 tx   L   2014-04-24 14m  5.2 mail smdie pythoon hosting
    48 tx   L   2014-04-24 8m   5.2 automate or save user and groups rights
    52 tx   L   2014-04-24 5m   5.2 think about database backup and license

    12 tasks
