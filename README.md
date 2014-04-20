tx
==

Gestion de commandes pour un laboratoire de biologie via django
S'appuye principalement sur l'auto-admin, voir main/models.py et main/admin.py

Demo à https://guarded-forest-1734.herokuapp.com/admin/
admin, admin

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
    36 tx   M   2014-04-24 10d 12.4 catch 403 error on edit orderitems
    38 tx   M   2014-04-24 10d 12.4 init database with a new current order
    34 tx   L   2014-04-24 10d 10.3 mail 5000 python host
    35 tx   L   2014-04-24 10d 10.3 mail smdie pythoon hosting
    37 tx   L   2014-04-24 10d 10.3 automate or save user and groups rights
    39 tx   L   2014-04-24 10d 10.3 think about database backup and license
    52 tx       2014-04-21 1d   9.5 create doc and user guide
    50 tx   M              1d  4.91 split admin code in utils and action at least
    53 tx                  1d  1.01 override some msg in english to french
    54 tx                  6s     1 fix xls or rethink it

    10 tasks
