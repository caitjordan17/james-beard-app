from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    serialize_rules = ('-chef.restaurants', '-chef.id',)  # to-add

    # ensure this works with scraper
    id = db.Column(db.Integer, primary_key=True)
    # nullable with entries where rest is NA
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    award_cat = db.Column(db.String, nullable=False)
    award_level = db.Column(db.String, nullable=False)
    award_year = db.Column(db.Integer, nullable=False)

    # relationships
    chef = db.relationship('Chef', back_populates='restaurants')
    chef_id = db.Column(db.Integer, db.ForeignKey('chefs.id'))

    def __repr__(self):
        return f'<ID: {self.id}, Restaurant: {self.restaurant_name}>'


class Chef(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    serialize_rules = ('-restaurant.id', '-restaurant.award_cat',
                       '-restaurant.award_year', '-restaurant.award_level',)  # to-add

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # relationships
    restaurants = db.relationship(
        'Restaurant', back_populates='chef', cascade='all, delete-orphan')  # do we want cascade?

    def __repr__(self):
        return f'<ID: {self.id}, Name: {self.name}>'
