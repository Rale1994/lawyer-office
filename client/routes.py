from flask import Blueprint, render_template, redirect, request, url_for, flash
from blog import db
from flask_login import login_required, current_user
from client.forms import AddClient
from blog.models import Client

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
def all_client():
    clients = Client.query.filter_by(lawyer=current_user)
    return render_template("all_clients.html", title="All client", clients=clients)


@client.route("/edit/<int:client_id>", methods=['GET', 'POST'])
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
        return redirect(url_for('users.all_client'))

    elif request.method == 'GET':
        form.f_name.data = client.first_name
        form.l_name.data = client.last_name
        form.city.data = client.city
        form.address.data = client.address
        form.phone.data = client.phone
        form.mail.data = client.mail
    return render_template("edit.html", form=form, title="Edit client", client=client)


@client.route("/delete/<int:client_id>", methods=['GET'])
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash(f"Client has been deleted!", "success")
    return redirect(url_for('client.all_client'))
