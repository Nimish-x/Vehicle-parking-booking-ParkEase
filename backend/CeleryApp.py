from app import app, db 
from backend.models import Users, Reservation
from backend.mail import send_mail
from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0'
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

# to Send promotional emails asynchronously
@celery.task(name='backend.CeleryApp.send_promotional_emails_task')
def send_promotional_emails_task():
    with app.app_context():
        try:
            user_ids = db.session.query(Reservation.user_id).distinct()
            users = Users.query.filter(Users.id.in_(user_ids)).all()

            for user in users:
                subject = "Special Offer from ParkEase"
                body = (
                    f"Hello {user.username},\n\n"
                    "Enjoy our exclusive offers just for you!\n"
                    "Visit the app for more details.\n\n"
                    "Best regards,\nParkEase Team"
                )
                send_mail(user.email, subject, body)
            return "Promotional emails sent successfully"
        except Exception as e:
            return f"Error sending promotional emails: {e}"

# to Send parking summary emails asynchronously
@celery.task(name='backend.CeleryApp.send_parking_summary_emails_task')
def send_parking_summary_emails_task():
    with app.app_context():
        try:
            user_ids = db.session.query(Reservation.user_id).distinct()
            users = Users.query.filter(Users.id.in_(user_ids)).all()

            for user in users:
                reservations = Reservation.query.filter_by(user_id=user.id).all()

                summary_lines = []
                for res in reservations:
                    parking_time = res.parking_time.strftime("%Y-%m-%d %H:%M") if res.parking_time else "N/A"
                    leaving_time = res.leaving_time.strftime("%Y-%m-%d %H:%M") if res.leaving_time else "Ongoing"
                    summary_lines.append(
                        f"Spot ID: {res.spot_id}, Parked from {parking_time} to {leaving_time}, Fee: Rs. {res.parking_fee}"
                    )
                summary_text = "\n".join(summary_lines) if summary_lines else "You currently have no parking reservations."

                subject = "Your ParkEase Parking Summary"
                body = (
                    f"Hello {user.username},\n\n"
                    "Here is a summary of your recent parking activity:\n\n"
                    f"{summary_text}\n\n"
                    "Thank you for using ParkEase!\n\n"
                    "Best regards,\nParkEase Team"
                )
                send_mail(user.email, subject, body)
            return "Parking summary emails sent successfully"
        except Exception as e:
            return f"Error sending parking summary emails: {e}"

# # Schedule example (optional)
# celery.conf.beat_schedule = {
#     'send_promotional_emails_daily': {
#         'task': 'backend.CeleryApp.send_promotional_emails_task',
#         'schedule': crontab(hour=9, minute=0),
#         'args': ()
#     },
#     'send_parking_summary_nightly': {
#         'task': 'backend.CeleryApp.send_parking_summary_emails_task',
#         'schedule': crontab(hour=0, minute=0),
#         'args': ()
#     },
# }
