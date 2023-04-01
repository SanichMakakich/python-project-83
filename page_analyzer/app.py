from flask import Flask, render_template, \
    get_flashed_messages, flash, request, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.connected import connect_to_db, insert_to_db
from datetime import datetime
from page_analyzer.validate import is_valid

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/', methods=['GET'])
def index():
    message = get_flashed_messages(with_categories=True)
    data = []
    errors = []
    return render_template('index.html',
                           data=data,
                           errors=errors,
                           message=message)


@app.route('/urls', methods=["GET"])
def get_sites():
    request = '''SELECT * from urls ORDER BY urls.id DESC'''
    responce = connect_to_db(request)
    return render_template('urls.html',
                           data=responce)


@app.route('/urls', methods=["POST"])
def post_sites():
    data = request.form.to_dict()
    errors = is_valid(data)

    if errors:
        flash(f"{errors['name']}")
        if errors.get('id'):
            return redirect(url_for('id_sites', id=errors['id']))
        else:
            return render_template("index.html",
                                   data=data,
                                   errors=errors)

    current_datetime = datetime.now()

    sql_query = f'''INSERT INTO urls(name, created_at)
                    VALUES('{data['url']}','{current_datetime}')'''

    insert_to_db(sql_query)
    flash("Страница успешно добавлена", 'success')

    return redirect(url_for('get_sites'))


@app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    message = get_flashed_messages(with_categories=True)
    sql_query = f'''SELECT * FROM urls WHERE id={id}'''

    responce = connect_to_db(sql_query)
    return render_template("url_id.html",
                           message=message,
                           id=id,
                           data=responce)
