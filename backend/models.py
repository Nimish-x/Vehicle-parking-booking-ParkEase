from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import uuid


db = SQLAlchemy()


USER_ROLE = 'user'
ADMIN_ROLE = 'admin'


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Roles(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    desc = db.Column(db.String(200))

    def __repr__(self):
        return f'<Role {self.name}>'


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.BigInteger, unique=True)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)

    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Roles', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def is_admin(self):
        return any(role.name == ADMIN_ROLE for role in self.roles)

    def __repr__(self):
        return f'<User {self.email}>'


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f'<Admin {self.email}>'


class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    prime_location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    no_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ParkingLot {self.address}>'


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), default='A', nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))

    def __repr__(self):
        return f'<ParkingSpot {self.id}>'


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parking_time = db.Column(db.DateTime)
    leaving_time = db.Column(db.DateTime)
    parking_fee = db.Column(db.Integer)

    def __repr__(self):
        return f'<Reservation {self.id}>'


class JobLog(db.Model):
    __tablename__ = 'job_logs'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')
    run_at = db.Column(db.DateTime)
    message = db.Column(db.String(255))

    def __repr__(self):
        return f'<JobLog {self.job_name}>'
