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
