# Helpdesk Lite

A lightweight internal helpdesk system for managing employee support tickets.


<img width="1880" height="762" alt="Screenshot 2026-07-14 054828" src="https://github.com/user-attachments/assets/83392a72-3a5b-48ab-af7c-ea2b92db6b49" />

<img width="1722" height="931" alt="Screenshot 2026-07-14 054847" src="https://github.com/user-attachments/assets/46e0c4ee-67cb-43ee-a940-eba7f6af6cb9" />

<img width="1861" height="822" alt="Screenshot 2026-07-14 054804" src="https://github.com/user-attachments/assets/dd3444ed-2676-468e-946b-c03445a3294b" />


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
