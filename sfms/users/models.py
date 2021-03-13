from flask_user import UserMixin
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from sfms import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False, server_default='')
    active = Column(Boolean(), nullable=False, server_default='0')

    roles = db.relationship('Role', secondary='user_roles')


# Defines the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)


# Defines the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))


