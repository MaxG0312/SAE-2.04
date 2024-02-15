from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

# project_folder = os.path.expanduser('/home/userdepinfo/Travail/sae_test/SAE-2_04')  # adjust as appropriate (avec le dossier où se trouve le fichier .env et app.py)
# load_dotenv(os.path.join(project_folder, '.env'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host=os.environ.get("HOST"),
            user=os.environ.get("LOGIN"),
            password=os.environ.get("PASSWD"),
            database=os.environ.get("DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db
