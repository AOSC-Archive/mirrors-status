from flask_sqlalchemy import SQLAlchemy, Model
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Mirror(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    main = db.Column(db.Boolean, default=False)
    area = db.Column(db.String())
    name = db.Column(db.String())
    url = db.Column(db.String())
    last_update_url = db.Column(db.String())
    repo_last_update = db.Column(db.DateTime())
    last_fetch = db.Column(db.DateTime())
    last_fetch_status_code = db.Column(db.Integer())
    last_fetch_status = db.Column(db.String())


    def __repr__(self):
        return '<Mirror %r>' % self.name


class Config(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    last_update = db.Column(db.DateTime())
