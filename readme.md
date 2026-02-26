# ParkEase - Vehicle Parking Booking System

ParkEase is a comprehensive web application designed to simplify vehicle parking management and booking. It provides an intuitive interface for users to find and reserve parking spots, and a robust admin dashboard for managing parking lots, active bookings, and users.

## 🚀 Features

### For Users:
- **User Authentication:** Secure signup, login, and profile management using Argon2 hashing.
- **Find Parking Lots:** Browse available parking lots, view total spots, pricing, and prime locations.
- **Book a Spot:** Reserve available parking spots in real-time.
- **My Bookings:** View active and past parking reservations with timestamps and fees.

### For Administrators:
- **Dashboard & Analytics:** Visual charts using Chart.js to monitor bookings and system usage.
- **Manage Parking Lots:** Add, update, and remove parking lots and their capacities.
- **User Management:** View all registered users and their activity status.
- **Automated Email Notifications:** Asynchronous background tasks (via Celery) to send:
  - Promotional emails
  - Nightly parking summaries to users

---

## 💻 Tech Stack

### Frontend
- **Framework:** Vue 3 + Vite
- **State Management:** Pinia
- **Routing:** Vue Router
- **Data Visualization:** Chart.js & vue-chartjs
- **Styling:** Custom CSS

### Backend
- **Framework:** Flask & Flask-RESTful
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Flask-Security-Too (Role-based access control)
- **Background Tasks:** Celery + Redis (Message Broker)
- **Email Sending:** SMTP (MailHog for local development)

---

## 🛠️ Local Setup & Installation

### Prerequisites
- Python 3.x
- Node.js & npm (v16+ recommended)
- Redis server (for Celery tasks)
- MailHog (for testing local emails)

### 1. Clone the Repository
```bash
git clone https://github.com/Nimish-x/Vehicle-parking-booking-ParkEase.git
cd Vehicle-parking-booking-ParkEase
```

### 2. Backend Setup
```bash
# Set up environment variables
cp .env.example .env

# Edit .env and provide your secret keys
# SECRET_KEY=your_secret_key
# SECURITY_PASSWORD_SALT=your_salt

# Install Python dependencies
pip install -r backend/requirements.txt

# Run the Flask App
python app.py
```
*The Flask api runs on `http://127.0.0.1:5000`*

### 3. Frontend Setup
```bash
cd frontend

# Install Node modules
npm install

# Run the Vite Dev Server
npm run dev
```
*The Vue frontend runs on `http://localhost:5173`*

### 4. Running Background Tasks (Celery & Email)

**Start Redis:** Ensure your local Redis server is running on `redis://localhost:6379/0`.

**Start MailHog:** Start MailHog to capture emails locally.
```bash
mailhog
```
*Access the MailHog web interface at `http://localhost:8025/`*

**Start Celery Worker:**
Open a new terminal window in the root directory:
```bash
celery -A backend.CeleryApp.celery worker --loglevel=info
```

---

## 🗄️ Database Reset Command
If you ever need to clear broken reservations during development:
```sql
DELETE FROM reservations WHERE spot_id NOT IN (SELECT id FROM parking_spot);
```
