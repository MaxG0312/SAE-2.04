#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    #selection des articles d'un panier
    # sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s; '''
    sql = '''
            SELECT
                utilisateur_id, meuble_id, quantite,
                date_ajout, meuble.nom_meuble AS nom, meuble.prix_meuble AS prix,
                meuble.stock
            FROM ligne_panier
            INNER JOIN meuble on ligne_panier.meuble_id = meuble.id_meuble
            WHERE utilisateur_id = %s; '''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    #articles_panier = []
    if len(articles_panier) >= 1:
        #calcul du prix total du panier
        sql = ''' SELECT SUM(quantite*prix_meuble) AS prix_total FROM ligne_panier
                    INNER JOIN meuble on ligne_panier.meuble_id = meuble.id_meuble
                    WHERE utilisateur_id = %s; '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None

    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    id_client = session['id_user']

    # Sélection du contenu du panier de l'utilisateur
    sql = '''
            SELECT
                utilisateur_id, meuble_id, quantite,
                date_ajout, meuble.nom_meuble AS nom, meuble.prix_meuble AS prix,
                meuble.stock
            FROM ligne_panier
            INNER JOIN meuble on ligne_panier.meuble_id = meuble.id_meuble
            WHERE utilisateur_id = %s; '''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')

    # Création de la commande
    date_achat = datetime.now()
    sql = ''' INSERT INTO commande(utilisateur_id, etat_id, date_achat) VALUES (%s, %s, %s) '''
    mycursor.execute(sql, (id_client, 1, date_achat))

    # Récupération de l'id de la commande insérée
    mycursor.execute(''' SELECT last_insert_id() as last_insert_id ''')
    commande_id = mycursor.fetchone()['last_insert_id']

    # Traitement pour chaque article du panier
    for item in items_ligne_panier:
        # Suppression d'une ligne de panier
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s AND meuble_id = %s; '''
        mycursor.execute(sql, (id_client, item['meuble_id']))

        # Ajout d'une ligne de commande
        tuple_commande = (commande_id, item['meuble_id'], item['prix'], item['quantite'])
        sql = ''' INSERT INTO ligne_commande(commande_id, meuble_id, prix, quantite)
                  VALUES (%s, %s, %s, %s) '''
        mycursor.execute(sql, tuple_commande)

    get_db().commit()
    return redirect('/client/article/show')

# def client_commande_add():
#     mycursor = get_db().cursor()

#     # choix de(s) (l')adresse(s)

#     id_client = session['id_user']

#     #selection du contenu du panier de l'utilisateur
#     sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s '''
#     mycursor.execute(sql, id_client)
#     items_ligne_panier = mycursor.fetchall()
    
#     if items_ligne_panier is None or len(items_ligne_panier) < 1:
#         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
#         return redirect('/client/article/show')
#                                            # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
#     a = datetime.strptime('my date', "%b %d %Y %H:%M")

#     #creation de la commande
#     sql = ''' INSERT INTO commande() '''

#     sql = '''SELECT last_insert_id() as last_insert_id'''
#     # numéro de la dernière commande
#     for item in items_ligne_panier:
#         #suppression d'une ligne de panier
#         sql = ''' DELETE FROM ligne_panier WHERE utilisateur = %s AND meuble_id = %s; '''

#         #ajout d'une ligne de commande
#         sql = ''' INSERT INTO ligne_commande(commande_id, meuble_id, quantite, date_ajout)
#                 VALUES (%s, %s, %s, %s) '''

#     get_db().commit()
#     flash(u'Commande ajoutée','alert-success')
#     return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    #selection des commandes ordonnées par état puis par date d'achat descendant
    sql = ''' 
            SELECT 
                id_commande, date_achat, SUM(quantite) AS nbr_articles, quantite*prix as prix_total,
                etat_id, etat.libelle
            FROM commande
            JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
            JOIN etat ON etat.id_etat = commande.etat_id
            WHERE utilisateur_id = %s
            GROUP BY id_commande, date_achat, etat_id, etat.libelle, quantite, prix
            ORDER BY etat_id, date_achat DESC; '''
    mycursor.execute(sql, id_client)
    commandes = mycursor.fetchall()

    #Sélection des articles commandés par un utilisateur
    sql = ''' 
            SELECT 
                nom_meuble AS nom, quantite, prix, quantite*prix as prix_ligne
            FROM ligne_commande
            JOIN meuble ON meuble.id_meuble = ligne_commande.meuble_id
            JOIN commande ON commande.id_commande = ligne_commande.commande_id
            WHERE utilisateur_id = %s; '''
    mycursor.execute(sql, id_client)
    articles_commande = mycursor.fetchall()

    #Pour les adresses de livraison
    commande_adresses = None

    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        #selection du détails d'une commande
        sql_detail_commande = '''
                                SELECT 
                                    nom_meuble AS nom, quantite, prix, quantite*prix as prix_ligne
                                FROM ligne_commande
                                JOIN meuble ON meuble.id_meuble = ligne_commande.meuble_id
                                WHERE commande_id = %s; '''
        mycursor.execute(sql_detail_commande, id_commande)

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

