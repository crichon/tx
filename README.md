tx
==

Gestion de commandes pour un laboratoire de biologie via django
S'appuye principalement sur l'auto-admin, voir main/models.py et main/admin.py

Auto-admin
----------

Groupes d'utilisateurs et permissions:
 - super-utilisateur: root
 - admin: peut modifier l'état des commandes, créer des fiches fournisseurs 
 - utilisateur: peut ajouter, modifier et supprimer des commandes d'objets sur la dernière facture en cours, ajouter des objets et catégories, modifier l'état des objets attachés à une commande reçue.

Utilisateur
-----------

Peut modifier les commandes d'objets d'une commande passée uniquement pour marquer un objet comme stocké, manquant ou annullé.
doit aussi pouvoir rapidement copié depuis d'anciennes commandes vers la nouvelles, pour cela sélectionner les items voulues dans commandes de produits et utiliser l'action appropriée

Admin
-----

Changer l'état d'une commande à:
 - en attente de réception:     géneration de factures prêtes à envoyées et crée une nouvelle commande courante, bloque la possibillité de modification direct sur les objets attachés à la commande.
 - reçue:                       marque les objets attachés à la commande comme en attente de stockage, les utilisateurs peuvent les marqués avec l'état approprié
 - annulée:                     crée une nouvelle commande courante, supprime l'ancienne ??
 - archivée                     ne fait rien, marque la fin du traitement d'une commande, normalement déclenché lorsque tous les objets d'une commande ont été correctement stockés

Les transisitions se font celon l'ordre:

    en cours                    -> annulée ou en attente de réception
    en attente de réception     -> annulée ou reçue
    reçue                       -> stocké (automatique, lorsque tout les objets ont été marqués


Vue publique
------------

Si temps, voir du coté de d3.js pour faire des visualisations sur les consommations du labo

Qui serait éventuellement
-------------------------

Gérer les prix, le labo n'est pas intéresser donc ...

Todo 
--------------------------------------------
dsl écris suite à une session code...

Merci taskwarrior ;)


    ID Proj Pri Due        Age Urg  Description
    -- ---- --- ---------- --- ---- ---------------------------------------------
    34 tx   M   2014-04-24 9d  11.8 deploy somwhere
    38 tx   M   2014-04-24 9d  11.8 check for nicer list display
    40 tx   M   2014-04-24 9d  11.8 init database with a new current order
    35 tx   L   2014-04-24 9d  9.68 mail 5000 python host
    36 tx   L   2014-04-24 9d  9.68 mail smdie pythoon hosting
    39 tx   L   2014-04-24 9d  9.68 automate or save user and groups rights
    41 tx   L   2014-04-24 9d  9.67 think about database backup and license
    55 tx       2014-04-21 1h  8.92 create doc and user guide
    52 tx   M              2h   4.9 split admin code in utils and action at least

    11 tasks
