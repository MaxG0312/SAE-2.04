#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''
            SELECT
                id_type AS id_type_meuble, libelle_type as libelle,
                COUNT(meuble.id_meuble) AS nbre_meubles
            FROM type_meuble
            LEFT JOIN meuble ON meuble.type_meuble_id = type_meuble.id_type
            GROUP BY id_type_meuble, libelle; '''
    mycursor.execute(sql)

    types_article = mycursor.fetchall()
    #types_article=[]
    return render_template('admin/type_article/show_type_article.html', types_article=types_article)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle)
    mycursor = get_db().cursor()
    sql = ''' 
            INSERT INTO type_meuble(libelle_type) 
            VALUE (%s); '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté, libellé :' + libelle
    flash(message, 'alert-success')

    return redirect('/admin/type-article/show') #url_for('show_type_article')


@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()

    sql = ''' 
            SELECT 
                id_type AS id_type_meuble, libelle_type AS libelle
            FROM type_meuble WHERE id_type = %s; '''
    mycursor.execute(sql, (id_type_article,))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)


@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id_type_article', '')
    tuple_update = (libelle, id_type_article)
    mycursor = get_db().cursor()
    sql = ''' UPDATE type_meuble SET libelle_type = %s WHERE id_type = %s; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    flash(u'type de meuble modifié, id: ' + id_type_article + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')


@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()

    sql = '''
            SELECT
                id_meuble, type_meuble_id, prix_meuble AS prix,
                nom_meuble AS nom
            FROM meuble
            WHERE type_meuble_id = %s; '''
    mycursor.execute(sql, (id_type_article,))
    meubles = mycursor.fetchall()
    print(meubles)

    if not meubles:
        sql = ''' DELETE FROM type_meuble WHERE id_type = %s; '''
        mycursor.execute(sql, (id_type_article,))
        get_db().commit()

        flash(u'suppression type article , id : ' + id_type_article, 'alert-success')
        return redirect('/admin/type-article/show')
    
    else:
        #On récupère le nombre de meuble du type de l'id_type_article
        sql = '''
                SELECT
                    id_type,
                    COUNT(meuble.id_meuble) AS nbre_meubles
                FROM type_meuble
                LEFT JOIN meuble ON meuble.type_meuble_id = type_meuble.id_type
                WHERE id_type = %s
                GROUP BY id_type; '''
        mycursor.execute(sql, (id_type_article,))
        type_meuble = mycursor.fetchone()
        nbre_meubles = type_meuble['nbre_meubles']

        #On procède à la suppression de tous les meubles de type id_type_article
        for meuble in meubles:
            sql = ''' DELETE FROM meuble WHERE nom_meuble = %s AND type_meuble_id = %s;'''
            mycursor.execute(sql, (meuble['nom'], id_type_article))
            get_db().commit()
        
        sql = ''' DELETE FROM type_meuble WHERE id_type = %s; '''
        mycursor.execute(sql, (id_type_article,))
        get_db().commit()

        if nbre_meubles == 1:
            message = u'suppression type meuble , id : ' + id_type_article + ', nombres de meuble supprimé : ' + str(nbre_meubles) + '.'
            flash(message, 'alert-success')
            return redirect('/admin/type-article/show')  

        else:  
            message = u'suppression type meuble , id : ' + id_type_article + ', nombres de meubles supprimés : ' + str(nbre_meubles) + '.'
            flash(message, 'alert-success')
            return redirect('/admin/type-article/show')





