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
            FROM meuble; '''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()

    sql = '''
            SELECT
                id_type AS id_type_meuble,
                libelle_type as libelle
            FROM type_meuble; '''
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()

    sql = '''
            SELECT
                utilisateur_id, meuble_id, quantite,
                date_ajout, meuble.nom_meuble AS nom, meuble.prix_meuble AS prix,
                meuble.stock
            FROM ligne_panier
            INNER JOIN meuble on ligne_panier.meuble_id = meuble.id_meuble;'''
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()

    list_param = []
    condition_and = ""
    # utilisation du filtre
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
