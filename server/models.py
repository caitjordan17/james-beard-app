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
    restuarant_chef = db.relationship(
        'Restaurant_chef', back_populates='restaurant')

    def __repr__(self):
        return f'<ID: {self.id}, Restaurant: {self.restaurant_name}>'


class Chef(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    serialize_rules = ('-restaurant.id', '-restaurant.award_cat',
                       '-restaurant.award_year', '-restaurant.award_level',)  # to-add

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # relationships
    restuarant_chef = db.relationship(
        'Restaurant_chef', back_populates='chef')

    def __repr__(self):
        return f'<ID: {self.id}, Name: {self.name}>'


class Restaurant_chef(db.Model, SerializerMixin):
    __tablename__ = "restaurant_chefs"
    id = db.Column(db.Integer, primary_key=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship(
        'Restaurant', back_populates='restaurant_chef')
    chef_id = db.Column(db.Integer, db.ForeignKey('chefs.id'))
    chef = db.relationship('Chef', back_populates='restaurant_chef')

    def __repr__(self):
        return f'<ID: {self.id}, {self.restaurant_id}, {self.chef_id}>'
