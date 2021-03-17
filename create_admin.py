from passlib.hash import  bcrypt
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from sfms.users.models import User, Role
from sfms import db

print(f'Introduce a username please: ')
username = str(input())

print(f'Introduce a password: ')
password = str(input())
print(f'Repeat the password: ')
rep_password = str(input())
while password != rep_password:
    print(f'Repeat the password please: ')
    rep_password = str(input())


hash_pass = bcrypt.hash(password)
admin_role = db.session.query(Role).filter_by(name='admin').first()
if not admin_role:
    admin = User(username=username, password=hash_pass, active=True)
    admin.roles.append(Role(name='admin'))
else:
    admin = User(username=username, password=hash_pass, active=True, roles=[admin_role])

db.session.add(admin)
try:
    db.session.commit()
except IntegrityError:
    print(f'Error: User with same username already exists')
    exit(1)

print(f'Admin user created')
