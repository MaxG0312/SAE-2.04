#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article

    sql = "SELECT * FROM ligne_panier WHERE meuble_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM meuble WHERE id_meuble = %s", (id_article))
    article = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_article)
        sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND meuble_id = %s"
        mycursor.execute(sql, tuple_update)

        # Update du stock
        tuple_update_stock = (quantite, id_article)
        sql = "UPDATE meuble SET stock = stock - %s WHERE id_meuble = %s"
        mycursor.execute(sql, tuple_update_stock)
    else:
        tuple_insert = (id_client, id_article, quantite)
        sql = "INSERT INTO ligne_panier(utilisateur_id, meuble_id, quantite, date_ajout) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
        mycursor.execute(sql, tuple_insert)

        # Update du stock
        tuple_update_stock = (quantite, id_article)
        sql = "UPDATE meuble SET stock = stock - %s WHERE id_meuble = %s"
        mycursor.execute(sql, tuple_update_stock)
    get_db().commit()

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    # Sélection de la ligne du panier pour l'article et l'utilisateur connecté
    sql = "SELECT * FROM ligne_panier WHERE meuble_id = %s AND utilisateur_id = %s;"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        # Mise à jour de la quantité dans le panier => -1 article
        tuple_update = (quantite, id_article, id_client)
        sql = ''' UPDATE ligne_panier SET quantite = quantite-%s WHERE meuble_id = %s AND utilisateur_id = %s; '''
        mycursor.execute(sql, tuple_update)

        # Mise à jour du stock de l'article : stock = stock + quantite de la ligne pour l'article
        sql_update_stock = ''' UPDATE meuble SET stock = stock + %s WHERE id_meuble = %s; '''
        mycursor.execute(sql_update_stock, (quantite, id_article))
    else:
        # Suppression de la ligne de panier
        tuple_update = (id_article, id_client)
        sql = ''' DELETE FROM ligne_panier WHERE meuble_id = %s AND utilisateur_id = %s; '''
        mycursor.execute(sql, tuple_update)

        # Mise à jour du stock de l'article : stock = stock + quantite de la ligne pour l'article
        sql_update_stock = ''' UPDATE meuble SET stock = stock + %s WHERE id_meuble = %s; '''
        mycursor.execute(sql_update_stock, (article_panier['quantite'], id_article))

    get_db().commit()
    return redirect('/client/article/show')



@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    #sélection des lignes de panier
    sql = ''' SELECT * FROM ligne_panier;'''
    mycursor.execute(sql)
    items_panier = mycursor.fetchall()
    #items_panier = []

    for item in items_panier:
        #suppression de la ligne de panier de l'article pour l'utilisateur connecté
        #print(item)
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s; '''
        mycursor.execute(sql, client_id)
        
        #mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
        sql2=''' UPDATE meuble SET stock = stock + %s WHERE id_meuble = %s '''
        mycursor.execute(sql2, (item['quantite'], item['meuble_id']))

        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    #id_declinaison_article = request.form.get('id_declinaison_article')

    #Sélection de la ligne du panier
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND meuble_id = %s; '''
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()


    sql = ''' DELETE FROM ligne_panier WHERE meuble_id = %s AND utilisateur_id = %s; '''
    mycursor.execute(sql, (id_article, id_client))

    #mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
    sql2='''UPDATE meuble SET stock = stock + %s WHERE id_meuble = %s '''
    mycursor.execute(sql2, (article_panier['quantite'], id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
