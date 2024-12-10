from sqlalchemy.orm import relationship

import db
from sqlalchemy import String, Column, Integer, Float, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Base, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    name= Column (String(150), unique= True, nullable= False)
    email = Column (String (200), unique=True, nullable= False)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    income = relationship('Income', backref='user', lazy=True)
    expenses = relationship('Expense', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

class Income(db.Base):
    __tablename__ = "incomes"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Income {self.amount}>'

class Expense(db.Base):
    __tablename__ = "expenses"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.amount}>'