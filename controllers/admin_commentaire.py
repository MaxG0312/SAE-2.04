#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)

    # Requête pour récupérer les commentaires de l'article spécifié
    sql_commentaires = '''
    SELECT u.nom, c.commentaire, c.valider, c.id_utilisateur, c.date_publication, c.id_meuble AS id_article
    FROM commentaire c
    JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
    WHERE c.id_meuble = %s
    ORDER BY c.date_publication ASC
    '''
    mycursor.execute(sql_commentaires, (id_article,))
    commentaires = mycursor.fetchall()

    # Requête pour récupérer les détails de l'article spécifié
    sql_article = '''
    SELECT nom_meuble
    FROM meuble
    WHERE id_meuble = %s
    '''
    mycursor.execute(sql_article, (id_article,))
    article = mycursor.fetchone()

    return render_template('admin/article/show_article_commentaires.html',
                           commentaires=commentaires,
                           article=article
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''
    DELETE FROM commentaire
    WHERE id_utilisateur = %s AND id_meuble = %s AND date_publication = %s
    '''
    tuple_delete = (id_utilisateur, id_article, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article=' + id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html', id_utilisateur=id_utilisateur, id_article=id_article, date_publication=date_publication)

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']  # 1 admin
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''
    INSERT INTO commentaire (id_utilisateur, id_meuble, date_publication, commentaire, valider)
    VALUES (%s, %s, %s, %s, 1)  -- La valeur 1 indique que le commentaire est validé
    '''
    tuple_add = (id_utilisateur, id_article, date_publication, commentaire)
    mycursor.execute(sql, tuple_add)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article=' + id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()
    sql = '''
    UPDATE commentaire
    SET valider = 1  -- Marquer les commentaires comme validés (lus par l'administrateur)
    WHERE id_meuble = %s
    '''
    mycursor.execute(sql, (id_article,))
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article=' + id_article)