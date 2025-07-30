For Celery
celery -A backend.CeleryApp.celery worker --loglevel=info
For mailhog just run "mailhog" in terminal and open http://localhost:8025/

Just in case:
DELETE FROM reservations
WHERE spot_id NOT IN (SELECT id FROM parking_spot);
