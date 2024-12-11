
# Attendance Management System - Backend

## Overview
This is a Django-based backend for an Attendance Management System. It provides APIs for managers to create rosters and for staff to mark attendance using webcam-captured images. The system supports roles (Manager and Staff), roster management, and attendance with image capture.

---

## Features
### Authentication & Authorization
- **Roles**: Manager and Staff.
- **Manager Privileges**:
  - Create, edit, and view staff rosters.
  - Define working days, shifts, and weekly offs for staff.
- **Staff Privileges**:
  - View assigned shifts.
  - Mark attendance within a specified time frame.

### Roster Management
- Add and manage staff members.
- Assign shifts with customizable timings and weekly offs.

### Attendance Management
- Staff can mark attendance by capturing an image using a webcam.
- Validate attendance within a 1-hour window of the shift start time.
- Save attendance data, including timestamp and captured image.

---

## Installation
### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd attendance-management-system
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': '<database_name>',
           'USER': '<database_user>',
           'PASSWORD': '<database_password>',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints
### Authentication
- **Token**: `POST /api/token/`

### Manager APIs
- **Create Roster**: `POST /api/roster/`
- **Edit Roster**: `PUT /api/roster/{id}/`
- **View Roster**: `GET /api/roster/`

### Staff APIs
- **View Shifts**: `GET /api/shifts/`
- **Mark Attendance**: `POST /api/attendance/`

### Attendance API Example Request
**Endpoint**: `POST /api/attendance/`
**Payload**:
```json
{
  "webcam": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...",
}
```
**Response**:
```json
{
  "id": 1,
  "staff": 5,
  "image": "attendance_images/5_20241211.png",
  "shift": 2
}
```

---

## Code Highlights
### Attendance Validation Logic
- Validates the current time against multiple shifts.
- Ensures attendance is marked within 1 hour of a shift start time.

### Base64 Image Handling
- Decodes and saves base64 webcam image as a file.
- Handles errors such as invalid padding.

---


