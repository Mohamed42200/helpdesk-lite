# Helpdesk Lite

A lightweight internal helpdesk system for managing employee support tickets.

## Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** SQLite
- **Frontend:** HTML, CSS, Vanilla JavaScript

## Quick Start

```bash
cd helpdesk-lite
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Seed Accounts

| Role     | Username   | Password     |
|----------|------------|--------------|
| Admin    | admin      | admin123     |
| Agent    | agent1     | agent123     |
| Employee | employee1  | employee123  |

Employees can also self-register at `/register/`.

## API Endpoints

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| POST   | /api/register               | Employee registration    |
| POST   | /api/login                  | Login                    |
| POST   | /api/tickets                | Create ticket            |
| GET    | /api/tickets/my             | My/assigned tickets      |
| GET    | /api/tickets/all            | All tickets (admin)      |
| GET    | /api/tickets/reports        | Reports (admin)          |
| PATCH  | /api/tickets/:id/status     | Update status            |
| POST   | /api/tickets/:id/comment    | Add comment              |
| POST   | /api/tickets/:id/close      | Close ticket             |
| GET    | /api/users                  | List users (admin)       |
| POST   | /api/users                  | Create user (admin)      |
| PATCH  | /api/users/:id              | Update user (admin)      |
| GET    | /api/faq                    | List FAQ                 |
| POST   | /api/faq                    | Create FAQ (admin)       |
| PATCH  | /api/faq/:id                | Update FAQ (admin)       |
| DELETE | /api/faq/:id                | Delete FAQ (admin)       |

## Email Notifications

Uses Django console email backend. Notifications print to the terminal for:

- Registration
- Ticket creation
- New comments
- Status updates
- Ticket resolved
