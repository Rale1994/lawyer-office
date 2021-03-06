import os

from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from blog import db, app
from flask_login import login_required, current_user
from client.forms import AddClient
from blog.models import Client, Judgment
from judgment.forms import AddJudgments
from sqlalchemy import or_
from datetime import datetime, timedelta

client = Blueprint("client", __name__)


@client.route("/add_client", methods=["POST", "GET"])
@login_required
def add_client():
    form = AddClient()
    if form.validate_on_submit():
        new_client = Client(first_name=form.f_name.data,
                            last_name=form.l_name.data,
                            city=form.city.data,
                            address=form.address.data,
                            phone=form.phone.data,
                            mail=form.mail.data,
                            lawyer=current_user)

        db.session.add(new_client)
        db.session.commit()
        flash(f"Client has added", "success")
        return redirect(url_for('client.add_client'))

    return render_template("add_client.html", title="Add client", form=form)


@client.route("/all_client")
@login_required
def all_client():
    clients = Client.query.filter_by(lawyer=current_user)
    return render_template("all_clients.html", title="All clients", clients=clients)


@client.route("/search", methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "{0}".format(search_value)
        results = Client.query.filter(or_(Client.first_name.like(search), Client.last_name.like(search))).filter(
            Client.user_id == current_user.id).all()
        for res in results:
            print(res.last_name)
        return render_template("all_clients.html", title="All clients", clients=results)
    else:
        return redirect(url_for("client.all_client"))


@client.route("/edit/<int:client_id>", methods=['GET', 'POST'])
@login_required
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    form = AddClient()
    if form.validate_on_submit():
        client.first_name = form.f_name.data
        client.last_name = form.l_name.data
        client.city = form.city.data
        client.address = form.address.data
        client.phone = form.phone.data
        client.mail = form.mail.data

        print(form.address.data)
        db.session.commit()
        return redirect(url_for('client.all_client'))

    elif request.method == 'GET':
        form.f_name.data = client.first_name
        form.l_name.data = client.last_name
        form.city.data = client.city
        form.address.data = client.address
        form.phone.data = client.phone
        form.mail.data = client.mail
    return render_template("edit.html", form=form, title="Edit client", client=client)


@client.route("/delete/<int:client_id>", methods=['GET'])
@login_required
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash(f"Client has been deleted!", "success")
    return redirect(url_for('client.all_client'))


@client.route("/add_judgments/<int:client_id>", methods=['POST', 'GET'])
@login_required
def add_judgments(client_id):
    client_jdg = Client.query.get_or_404(client_id)
    form = AddJudgments()
    if form.validate_on_submit():
        if request.files:
            file = request.files['inputFile']
            file.save(
                os.path.join('C:/Users/Korisnik/Desktop/Python/rados-project/blog/static/documents', file.filename))
        judgment_date = form.date_of_judgment.data
        date_obj = datetime.strptime(judgment_date, '%d.%m.%Y %H:%M')
        print(type(file.filename))
        judgment = Judgment(title=form.title.data,
                            content=form.content.data,
                            date_of_judgment=date_obj,
                            document=file.read(),
                            client_id=client_jdg.id)
        db.session.add(judgment)
        db.session.commit()
        flash('Judgment has added', 'success')
        return redirect(url_for('client.all_client'))
    return render_template("add_judgments.html", title="Add judgment", form=form, client=client)


@client.route("/responsibilities", methods=['GET'])
@login_required
def responsibilities():
    start_day = datetime.today().date()
    end_day = datetime.today().date() + timedelta(days=1)
    judgments = Judgment.query.filter(Judgment.date_of_judgment.between(start_day, end_day)).order_by(
        Judgment.date_of_judgment.asc()).all()

    if not judgments:
        return render_template("responsibilities.html", title="Responsibilities")
    all_clients = {

    }
    for judgment in judgments:
        all_clients[judgment.id] = Client.query.filter(Client.id == judgment.client_id).all()
    return render_template("responsibilities.html", judgments=judgments, clients_list=all_clients,
                           title="Responsibilities")


@client.route("/responsibilities_next_day", methods=['GET'])
@login_required
def responsibilities_next_day():
    start_day = datetime.today().date()+ timedelta(days=1)
    end_day = datetime.today().date() + timedelta(days=8)
    judgments = Judgment.query.filter(Judgment.date_of_judgment.between(start_day, end_day)).order_by(
        Judgment.date_of_judgment.asc()).all()

    if not judgments:
        return render_template("responsibilities.html", title="Responsibilities")
    all_clients = {

    }
    for judgment in judgments:
        all_clients[judgment.id] = Client.query.filter(Client.id == judgment.client_id).all()
    return render_template("responsibilities.html", judgments=judgments, clients_list=all_clients,
                           title="Responsibilities")





def get_client_for_combo():
    fname_and_lname = [(client.first_name, client.last_name) for client in
                       Client.query.filter_by(lawyer=current_user).all()]
    result = map(join_tuple_string, fname_and_lname)
    lista = list(result)
    return lista


def join_tuple_string(strings_tuple) -> str:
    return ' '.join(strings_tuple)
