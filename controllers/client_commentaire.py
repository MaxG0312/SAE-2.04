#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)
    id_client = session['id_user']

    sql = '''
    SELECT m.id_meuble AS id_article,
           AVG(n.note) AS moyenne_notes,
           COUNT(n.note) AS nb_notes
    FROM meuble m
    LEFT JOIN note n ON m.id_meuble = n.id_meuble
    WHERE m.id_meuble = %s
    GROUP BY m.id_meuble
    '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    sql = '''SELECT commentaire,commentaire.id_utilisateur, u.nom, commentaire.date_publication, commentaire.id_meuble AS id_article, AVG(n.note)
                FROM commentaire
                JOIN utilisateur u ON commentaire.id_utilisateur = u.id_utilisateur
                JOIN meuble m ON commentaire.id_meuble = m.id_meuble
                JOIN note n ON m.id_meuble = n.id_meuble
                WHERE commentaire.id_meuble=%s
                GROUP BY commentaire, commentaire.id_utilisateur, u.nom, commentaire.date_publication, commentaire.id_meuble
       '''
    mycursor.execute(sql, (id_article))
    commentaires = mycursor.fetchall()

    commandes_articles = []
    nb_commentaires = []

    if article is None:
        abort(404, "pb id article")

    sql = '''
    SELECT ligne_commande.quantite AS nb_commandes_article
    FROM ligne_commande
    JOIN commande c ON c.id_commande = ligne_commande.commande_id
    WHERE c.utilisateur_id = %s AND meuble_id = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()

    sql = '''
    SELECT COUNT(commentaire) AS nb_commentaires_utilisateur
    FROM commentaire
    WHERE id_utilisateur=%s AND id_meuble=%s
    '''
    mycursor.execute(sql, (id_client, id_article))
    nb_commentaires_utilisateur = mycursor.fetchone()

    sql = '''
    SELECT COUNT(commentaire) AS nb_commentaires_total
    FROM commentaire
    WHERE id_meuble=%s
    '''
    mycursor.execute(sql, (id_article,))
    nb_commentaires_total = mycursor.fetchone()

    nb_commentaires = {
        'nb_commentaires_utilisateur': nb_commentaires_utilisateur['nb_commentaires_utilisateur'],
        'nb_commentaires_total': nb_commentaires_total['nb_commentaires_total']
    }

    sql = '''
    SELECT AVG(note) AS note
    FROM note
    WHERE id_utilisateur = %s AND id_meuble = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    note = mycursor.fetchone()
    note = note['note'] if note else None

    return render_template('client/article_info/article_details.html',
                           article=article,
                           commandes_articles=commandes_articles,
                           commentaires=commentaires,
                           note=note,
                           nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              #
        return redirect('/client/article/details?id_article='+id_article)

    date_ajout=datetime.now()
    tuple_insert = ( id_client, id_article, date_ajout,commentaire)
    sql = '''
    INSERT INTO commentaire
    VALUES (%s,%s,%s,%s,0);
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    print(id_client, 'ceci client')
    id_article = request.form.get('id_article', None)
    print(id_article, 'ceci article')
    date_publication = request.form.get('date_publication', None)
    print(date_publication, 'ceci est la date de publication')
    sql = '''
       DELETE FROM commentaire
       WHERE id_utilisateur=%s AND id_meuble=%s AND date_publication = %s
       '''
    tuple_delete=(id_client,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_insert = (note, id_client, id_article)
    print(tuple_insert)
    sql = ''' INSERT INTO note
             VALUES (%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_client, id_article)
    print(tuple_update)
    sql = ''' UPDATE note
            SET note = %s
            WHERE id_utilisateur = %s AND id_meuble = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    sql = ''' DELETE FROM note
              WHERE id_utilisateur=%s AND id_meuble = %s'''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
