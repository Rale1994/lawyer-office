from datetime import datetime

from blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


Judgments = db.Table('judgments',
                     db.Column("judgment_id", db.Integer, db.ForeignKey('judgment.id'), nullable=False),
                     db.Column("client_id", db.Integer, db.ForeignKey('client.id'), nullable=False),
                     )


class Judgment(db.Model):
    # need to create separate table judgment
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    clients = db.relationship('Client', backref='lawyer', lazy='dynamic',
                              primaryjoin="(User.id==foreign(Client.user_id))", overlaps="judgment, user")

    # judgments = db.relationship('Client', secondary=Judgments, backref="client")
    # judgment = db.relationship('Judgment', secondary=Judgments, backref='user', lazy="select",overlaps="clients, user")


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # judgments = db.relationship("User", secondary=Judgments, backref="client")

    judgment = db.relationship('Judgment', secondary=Judgments, backref='judgment', lazy="dynamic")


db.create_all()
