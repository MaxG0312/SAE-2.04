from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host="chezxage.mysql.pythonanywhere-services.com",
            # host="serveurmysql",
            user="chezxage",
            password="BDD_meuble",
            database="chezxage$default",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()
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
