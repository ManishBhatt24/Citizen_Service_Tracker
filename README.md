# Citizen Service Request Tracker

A practical coding-challenge application built with **Python Django + SQLite + Bootstrap + Chart.js**.

## Features
- Register citizen complaints
- Categories: Water, Electricity, Road, Sanitation
- View all complaints
- Search and filter complaints
- Update complaint status: Pending / In Progress / Resolved
- Dashboard statistics
- Category-wise doughnut chart
- Server-side validation & CSRF protection
- SQLite database via Django ORM

## Run on Windows

### 1. Open terminal in this folder
```powershell
cd path\to\citizen_service_tracker
```

### 2. Install requirements
```powershell
pip install -r requirements.txt
```

### 3. Run database migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Django development server
```powershell
python manage.py runserver
```

### 5. Open browser
http://127.0.0.1:8000/

The `db.sqlite3` file is created automatically upon running migrations.

## Main routes
- `/` dashboard
- `/register/` register complaint
- `/complaints/` complaint list/search/filter
- `/complaints/<id>/status/` update status
- `/api/category-data/` chart data
