from turtle import back
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import not_
# from sqlalchemy import not_, null
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Employee(db.Model, UserMixin):

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Menu(db.Model, UserMixin):

    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    menu_items = db.relationship("MenuItem", back_populates="menu")


class MenuItem(db.Model, UserMixin):

    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu_type_id = db.Column(db.Integer, db.ForeignKey("menu_item_types.id"), nullable=False)

    menu = db.relationship("Menu", back_populates="menu_items")
    type = db.relationship("MenuItemType", back_populates="item_types")

class MenuItemType(db.Model, UserMixin):

    __tablename__ = "menu_item_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    item_types = db.relationship("MenuItem", back_populates="type")

class Table(db.Model, UserMixin):

    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship("Order", back_populates="table_order")

class Order(db.Model, UserMixin):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"),not_nullable=True )
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"),not_nullable=True)
    finished = db.Column(db.Boolean, not_nullable=True)

    table_order = db.relationship("Table", back_populates="orders")
    order_deets = db.relationship("OrderDetail", back_populates="one_order")


class OrderDetail(db.Model, UserMixin):

    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"),not_nullable=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"),not_nullable=True)

    one_order = db.relationship("Orders", back_populates="order_deets")
