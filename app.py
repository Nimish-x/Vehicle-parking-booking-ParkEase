from functools import wraps
from flask import Flask, abort, request, send_from_directory
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user, auth_required
from backend.models import db, Users, Roles, Admin, ParkingLot, ParkingSpot, Reservation
from backend.routes.auth import auth_bp
from flask_security.utils import hash_password
from flask_cors import CORS
from datetime import datetime
from backend.mail import send_mail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, 
     supports_credentials=True)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///vehicle_parking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'your_salt')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my_secret_key')
app.config['SECURITY_PASSWORD_HASH'] = os.environ.get('SECURITY_PASSWORD_HASH', 'argon2')
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION'] = True
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = ['session', 'basic']
app.config['WTF_CSRF_ENABLED'] = False

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)

with app.app_context():
    db.create_all()
    if not Admin.query.first():
        admin = Admin(
            email="admin@example.com",
            password=hash_password("adminpassword"),
            username="admin_user"
        )
        db.session.add(admin)
    
    user_role = user_datastore.find_role('user')
    if not user_role:
        user_role = user_datastore.create_role(name='user')
        db.session.commit()
    
    if not user_datastore.find_user(email="user@example.com"):
        user = user_datastore.create_user(
            email="user@example.com",
            password=hash_password("userpassword"),
            username="regular_user",
            roles=[user_role]
        )
        db.session.commit()


class UserApi(Resource):
    def get(self, user_id):
        user = Users.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {"user_id": user.id, "username": user.username, "user_email": user.email}

    def post(self):
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return {"error": "Missing required fields"}, 400
        user_role = user_datastore.find_role('user')
        if not user_role:
            user_role = user_datastore.create_role(name='user', description='Default user role')
            db.session.commit()

        user = user_datastore.create_user(
            email=data['email'],
            password=hash_password(data['password']),
            username=data.get('username', ''),
            phone=data.get('phone'),
            roles=[user_role]
        )
        db.session.commit()
        return {"message": "User created successfully", "user_id": user.id}

    def delete(self, user_id):
        user = Users.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

    def put(self, user_id):
        user = Users.query.get(user_id)
        data = request.get_json()
        if not user:
            return {"error": "User not found in database"}, 404
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = hash_password(data['password'])
        user.username = data.get('username', user.username)
        db.session.commit()
        return {"message": "User fields updated successfully"}, 200

class CurrentUserApi(Resource):
    method_decorators = [auth_required()] 

    def get(self):
        user = current_user
        return {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "phone": user.phone,
        }

    def put(self):
        user = current_user
        data = request.get_json()
        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            user.username = data['username']
        if 'phone' in data:
            user.phone = data['phone']
        if 'password' in data:
            user.password = hash_password(data['password'])
        db.session.commit()
        return {"message": "User updated successfully"}

class ParkingLotApi(Resource):
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"error": "Parking lot not found"}, 404
        return {"id": lot.id, "address": lot.address, "price": lot.price}

    def post(self):
        data = request.get_json()
        lot = ParkingLot(
            address=data['address'], price=data['price'],
            prime_location=data['prime_location'], no_of_spots=data['no_of_spots']
        )
        db.session.add(lot)
        db.session.commit()
        return {"message": "Lot creation successful"}, 201

    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"error": "Lot not found"}, 404
        db.session.delete(lot)
        db.session.commit()
        return {"message": "Parking lot deletion successful"}, 200

    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"error": "Parking Lot not found"}, 400
        data = request.get_json()
        if 'address' in data:
            lot.address = data['address']
        if 'price' in data:
            lot.price = data['price']
        if 'prime_location' in data:
            lot.prime_location = data['prime_location']
        if 'no_of_spots' in data:
            lot.no_of_spots = data['no_of_spots']
        db.session.commit()
        return {'message': 'Data Fields updated successfully'}, 200

class ParkingLotListApi(Resource):
    def get(self):
        lots = ParkingLot.query.all()
        results = []
        for lot in lots:
            results.append({
                "id": lot.id,
                "address": lot.address,
                "prime_location": lot.prime_location,
                "price": lot.price,
                "no_of_spots": lot.no_of_spots
            })
        return results, 200

class ReservationApi(Resource):
    def get(self, r_id):
        reservation = Reservation.query.get(r_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404
        return {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "spot_id": reservation.spot_id,
            "parking_fee": reservation.parking_fee
        }

    def post(self):
        data = request.get_json()
        reservation = Reservation(
            user_id=data["user_id"],
            spot_id=data["spot_id"],
            parking_time=data["parking_time"],
            leaving_time=data["leaving_time"],
            parking_fee=data["parking_fee"]
        )
        db.session.add(reservation)
        db.session.commit()
        return {"message": "Reservation created", "reservation_id": reservation.id}, 201

    def delete(self, reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404
        spot = ParkingSpot.query.get(reservation.spot_id)
        if spot:
            spot.status = 'A'
        
        reservation.leaving_time = datetime.utcnow() 
        # db.session.delete(reservation)  

        db.session.commit()
        return {"message": "Reservation released, history kept"}, 200

class ReservationListApi(Resource):
    def get(self):
        reservations = Reservation.query.all()
        results = []
        for res in reservations:
            s = ParkingSpot.query.get(res.spot_id)
            results.append({
                "id": res.id,
                "user_id": res.user_id,
                "spot_id": res.spot_id,
                "parking_time": res.parking_time.strftime("%Y-%m-%d %H:%M:%S") if res.parking_time else None,
                "leaving_time": res.leaving_time.strftime("%Y-%m-%d %H:%M:%S") if res.leaving_time else None,
                "parking_fee": res.parking_fee,
                "Availability": s.status
            })
        return results, 200


class ParkingLotAvailabilityApi(Resource):
    def get(self):
        lots = ParkingLot.query.all()
        data = []
        for lot in lots:
            free_spots_count = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            data.append({
                "id": lot.id,
                "address": lot.address,
                "prime_location": lot.prime_location,
                "price": lot.price,
                "total_spots": lot.no_of_spots,
                "free_spots": free_spots_count
            })
        return data


class ParkingLotBookSpotApi(Resource):
    @auth_required()  # user must be logged in
    def post(self, lot_id):
        free_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if not free_spot:
            return {"error": "No available spots in this parking lot"}, 400

        free_spot.status = 'B'  

        reservation = Reservation(
            user_id=current_user.id,
            spot_id=free_spot.id,
            parking_time=datetime.utcnow(),
            leaving_time=None,  
            parking_fee=ParkingLot.query.get(lot_id).price
        )
        db.session.add(reservation)
        db.session.commit()
        return {"message": "Spot booked successfully", "reservation_id": reservation.id}
    
class MyBookingsApi(Resource):
    @auth_required()
    def get(self):
        # To query all reservations of current_user
        reservations = Reservation.query.filter_by(user_id=current_user.id).all()

        bookings = []
        for res in reservations:
            spot = ParkingSpot.query.get(res.spot_id)
            lot = ParkingLot.query.get(spot.lot_id) if spot else None

            bookings.append({
                "id": res.id,
                "spot_id": res.spot_id,
                "parking_time": res.parking_time.isoformat() if res.parking_time else None,
                "leaving_time": res.leaving_time.isoformat() if res.leaving_time else None,
                "parking_fee": res.parking_fee,
                "lot_address": lot.address if lot else None
            })

        return bookings   
#Logic for Promotional and Summary Api
class SendPromotionalEmailApi(Resource):
    @auth_required()
    def post(self):
        try:
            from backend.CeleryApp import send_promotional_emails_task
            send_promotional_emails_task.delay()
            return {"message": "Promotional emails sending started"}, 202
        except Exception as e:
            app.logger.error(f"Error triggering promotional emails task: {e}")
            return {"error": str(e)}, 500


class SendParkingSummaryEmailApi(Resource):
    @auth_required()
    def post(self):
        try:
            from backend.CeleryApp import send_parking_summary_emails_task
            send_parking_summary_emails_task.delay() 
            return {"message": "Parking summary emails sending started"}, 202
        except Exception as e:
            app.logger.error(f"Error triggering parking summary emails task: {e}")
            return {"error": str(e)}, 500
      
# Special check decorator for admin
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403, description="Admin access required")
        return f(*args, **kwargs)
    return decorated

class AdminParkingLotUpdateApi(Resource):

    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"error": "Parking Lot not found"}, 404

        data = request.get_json()
        changed = False

        if 'price' in data:
            lot.price = data['price']
            changed = True

        if 'no_of_spots' in data:
            lot.no_of_spots = data['no_of_spots']
            changed = True

        if changed:
            db.session.commit()
            return {"message": "Parking lot price and spots updated successfully"}
        else:
            return {"error": "No updatable fields provided"}, 400
        from flask_security import current_user
from flask import abort
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403, description="Admin access required")
        return f(*args, **kwargs)
    return decorated


class AdminUserListApi(Resource):

    def get(self):
        users = Users.query.all()
        results = []
        for user in users:
            results.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "active": user.active,
                
            })
        return {"users": results}, 200
class AdminBookingSummaryApi(Resource):
    # auth_required()

    def get(self):
        lots = ParkingLot.query.all()
        summary = []
        for lot in lots:
            active_bookings_count = (
                Reservation.query.join(ParkingSpot, Reservation.spot_id == ParkingSpot.id)
                .filter(ParkingSpot.lot_id == lot.id, Reservation.leaving_time.is_(None))
                .count()
            )
            summary.append({
                "lot_id": lot.id,
                "address": lot.address,
                "active_bookings": active_bookings_count
            })
        return {"summary": summary}, 200



api.add_resource(UserApi, '/api/user', '/api/user/<int:user_id>')
api.add_resource(ParkingLotApi, '/api/parking_lot/<int:lot_id>','/api/parking_add')
api.add_resource(ReservationApi, '/api/reservation', '/api/reservation/<int:reservation_id>')
api.add_resource(ParkingLotAvailabilityApi, '/api/parking_lots/availability')
api.add_resource(ParkingLotBookSpotApi, '/api/parking_lots/<int:lot_id>/book')
api.add_resource(MyBookingsApi,'/api/my_bookings')
api.add_resource(CurrentUserApi, '/api/user/current')
api.add_resource(ReservationListApi,'/api/reservations')
api.add_resource(ParkingLotListApi, '/api/parking_lot')
api.add_resource(SendPromotionalEmailApi, '/api/admin/send_promotional_email')
api.add_resource(SendParkingSummaryEmailApi, '/api/admin/send_parking_summary_email')
api.add_resource(AdminParkingLotUpdateApi, '/api/admin/parking_lot/<int:lot_id>/update')
api.add_resource(AdminUserListApi, '/api/admin/users')
api.add_resource(AdminBookingSummaryApi, '/api/admin/bookings_summary')    







@app.route('/profile')
@login_required
def profile():
    return {"message": f"Welcome, {current_user.email}!"}


app.register_blueprint(auth_bp, url_prefix='/api/auth')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
