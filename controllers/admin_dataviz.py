#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def note_moyenne():
    mycursor = get_db().cursor()

    # Requête pour récupérer les noms des meubles et leur note moyenne
    sql = '''
    SELECT m.nom_meuble, COALESCE(AVG(n.note), 0) AS note_moyenne
    FROM meuble m
    LEFT JOIN note n ON m.id_meuble = n.id_meuble
    GROUP BY m.nom_meuble
    '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()

    # Création des listes de labels et de valeurs pour le graphique
    labels = [str(row['nom_meuble']) for row in datas_show]
    values = [float(row['note_moyenne']) for row in datas_show]

    return render_template('admin/dataviz/dataviz_etat_1.html',
                           datas_show=datas_show,
                           labels=labels,
                           values=values)