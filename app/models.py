import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {"id": self.id, "username": self.username}
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ["username", "email"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Entreprenuers(db.Model):
    Id = db.Column(db.String(32), primary_key=True)
    Company_name = db.Column(db.String(32))
    Country_HQ = db.Column(db.String(40))
    Last_funding_round_raised_type = db.Column(db.String(200))
    Last_funding_round_raised_amount = db.Column(db.String(200))
    Largest_round = db.Column(db.String(200))
    Amount = db.Column(db.String(200))
    Main_sector = db.Column(db.String(200))
    Business_Model = db.Column(db.String(200))
    company_description_length = db.Column(db.String(200))
    company_age = db.Column(db.String(200))
    existance_of_headquarters = db.Column(db.String(200))
    headquarter_city = db.Column(db.String(200))
    existance_of_Other_offices = db.Column(db.String(200))
    exiatence_of_assigned_country = db.Column(db.String(200))
    number_of_operational_countries = db.Column(db.String(200))
    number_of_investors = db.Column(db.String(200))
    number_of_founders = db.Column(db.String(200))
    female_co_founder = db.Column(db.String(200))
    number_of_categories = db.Column(db.String(200))
    attended_accelerator = db.Column(db.String(200))
    number_of_employees = db.Column(db.String(200))
    have_website = db.Column(db.String(200))
    top_level_domain_name = db.Column(db.String(200))
    existance_of_twitter_account = db.Column(db.String(200))
    existance_of_linkedin_account = db.Column(db.String(200))
    existance_of_facebook_account = db.Column(db.String(200))
    company_description_clusters = db.Column(db.String(200))

    def __repr__(self):
        return "<Entreprenuers %r>" % self.id


class Transactions(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    post_date = db.Column(db.DateTime)
    title = db.Column(db.String(200))
    amount = db.Column(db.Float)
    funding_round = db.Column(db.String(200))
    investors = db.Column(db.String(200))
    link = db.Column(db.String(200))
    country = db.Column(db.String(200))
    main_sector = db.Column(db.String(200))
    number_of_investors = db.Column(db.Float)
    source_name = db.Column(db.String(200))

    def __repr__(self):
        return "<Transactions %r>" % self.id


class Investors(db.Model):
    Id = db.Column(db.String(32), primary_key=True)
    Investor = db.Column(db.String(200))
    length_of_post_description = db.Column(db.Float)
    post_description_cluster = db.Column(db.String(200))
    Investor_class = db.Column(db.String(200))
    status = db.Column(db.String(200))
    age = db.Column(db.Float)
    employees = db.Column(db.String(200))
    headquarters = db.Column(db.String(200))
    number_of_offices = db.Column(db.Float)
    female_key_people = db.Column(db.String(200))
    investor_type = db.Column(db.String(200))
    impact_focus = db.Column(db.String(200))
    investment_stage = db.Column(db.String(200))
    number_investing_stages = db.Column(db.Float)
    min_ticket_size_range = db.Column(db.Float)
    max_ticket_size_range = db.Column(db.Float)
    number_sector_focus = db.Column(db.Float)
    Sector_focus = db.Column(db.String(200))
    africa_portfolio = db.Column(db.String(200))
    len_africa_portfolio = db.Column(db.Float)
    sector_of_focus = db.Column(db.String(200))
    portfolio_size = db.Column(db.Float)
    activity_in_africa = db.Column(db.String(200))
    existance_of_exits = db.Column(db.String(200))
    exits = db.Column(db.String(200))
    geographical_focus = db.Column(db.String(200))
    website = db.Column(db.String(200))
    top_level_domain_name = db.Column(db.String(200))
    linkedin_link = db.Column(db.String(200))
    twitter_link = db.Column(db.String(200))
    facebook_link = db.Column(db.String(200))

    def __repr__(self):
        return "<Investors %r>" % self.id

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

