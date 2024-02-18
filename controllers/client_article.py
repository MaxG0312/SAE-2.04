#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' 
            SELECT 
                id_meuble, type_meuble_id, materiau_id,
                nom_meuble AS nom, stock, largeur, hauteur, 
                prix_meuble AS prix, fournisseur, marque, image_meuble as image
            FROM meuble '''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()

    sql_type = '''
            SELECT
                id_type AS id_type_meuble,
                libelle_type as libelle
            FROM type_meuble; '''
    mycursor.execute(sql_type)
    type_meuble = mycursor.fetchall()

    sql_panier = '''
            SELECT
                utilisateur_id, meuble_id, quantite,
                date_ajout, meuble.nom_meuble AS nom, meuble.prix_meuble AS prix,
                meuble.stock
            FROM ligne_panier
            INNER JOIN meuble on ligne_panier.meuble_id = meuble.id_meuble;'''
    mycursor.execute(sql_panier)
    articles_panier = mycursor.fetchall()

    # utilisation du filtre
    list_param = []
    conditions = []

    if "filter_word" in session:
        conditions.append("nom_meuble LIKE %s")
        list_param.append("%" + session["filter_word"] + "%")

    if "filter_prix_min" in session or "filter_prix_max" in session:
        conditions.append("prix_meuble BETWEEN %s AND %s")
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])

    if "filter_types" in session:
        conditions.append("(" + " OR ".join(["type_meuble_id = %s"] * len(session['filter_types'])) + ")")
        list_param.extend(session['filter_types'])
        
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    mycursor.execute(sql, tuple(list_param))
    meubles = mycursor.fetchall()

    mycursor.execute(sql_type)
    type_meuble = mycursor.fetchall()

    mycursor.execute(sql_panier)
    articles_panier = mycursor.fetchall()
    
    #prise en compte des commentaires et des notes
    #sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    #articles =[]


    # pour le filtre
    #types_article = []

    #articles_panier = []

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , meubles=meubles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , type_meuble=type_meuble
                           )
