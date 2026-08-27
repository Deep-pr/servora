# Servora

Advanced Local Service Finder & Booking Web Application

Tagline: **Trusted Services. Right Near You.**

## Current Build Status

This repository is being built part by part.

Part 1 includes:
- Django project and modular app structure
- Environment-based settings
- Custom user model with customer/provider/admin roles
- Core service, provider, booking, quote, payment, review, messaging, notification, complaint, and audit models
- Bootstrap/Django-template public UI foundation
- Provider search and profile pages
- Leaflet map placeholder
- Chart.js dashboard placeholder
- Demo seed command with 12 categories and 20 providers

Part 2 includes:
- Separate customer and provider registration flows
- Automatic customer/provider profile creation
- Role-aware dashboards for customer, provider, and admin users
- Editable customer and provider profile forms
- Django admin registration for major models
- Basic registration and dashboard access tests

Part 3 includes:
- Provider service add/edit/delete workflow
- Provider verification document upload workflow
- File type and size validation for verification documents
- Admin-only service category create/edit/delete workflow
- Dashboard links for provider onboarding and category management
- Tests for service management, verification upload, and category permissions

Part 4 includes:
- Advanced provider search filters for category, rating, price, experience, emergency availability, and location text
- Radius filtering and nearest sorting when latitude/longitude are supplied
- Paginated provider results
- Leaflet map markers generated from provider coordinates
- Demo provider coordinates around Tinsukia
- Search tests for filtering and distance sorting

Part 5 includes:
- Customer booking request workflow from provider profiles
- Customer and provider booking list pages
- Booking detail page with lifecycle status visibility
- Provider actions for accepting, rejecting, confirming, starting, completing, rescheduling, and disputing bookings
- Provider quote creation and customer quote accept/reject flow
- Demo bookings and quotes in seed data
- Tests for booking creation, status updates, and quote acceptance

Part 6 includes:
- Customer reviews for completed bookings
- Provider rating recalculation after reviews
- Favorite provider save/remove workflow
- Complaint submission and complaint tracking pages
- In-app notifications with unread counter and mark-all-read action
- Basic customer-provider conversations and message history
- Notifications triggered by bookings, quotes, reviews, complaints, and messages
- Tests for reviews, favorites, complaints, notifications, and messaging

Part 7 includes:
- Staff-only analytics dashboard
- Chart.js datasets for booking trends, user growth, service popularity, status distribution, peak hours, and locations
- Data insights for most requested services, cancellation trends, and top provider performance
- Audit log page for recent authenticated mutating actions
- Audit middleware that stores action metadata without request bodies or sensitive values
- Additional secure cookie, referrer policy, and header settings
- Analytics tests and final project test pass

## Tech Stack

- Python
- Django
- Django ORM
- Django Authentication
- PostgreSQL-ready configuration
- HTML, CSS, JavaScript
- Bootstrap 5
- Django Templates
- Chart.js
- OpenStreetMap + Leaflet

No React, Vue, or Angular.

## Local Setup

```bash
cd /Users/deepprasadsah/Desktop/Projects/servora
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Demo Users

After running `python manage.py seed_data`:

- Customer: `customer1` / `Customer@123`
- Providers: `provider1` through `provider20` / `Provider@123`

## PostgreSQL Configuration

Create a database and user in PostgreSQL:

```sql
CREATE DATABASE servora_db;
CREATE USER servora_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE servora_db TO servora_user;
```

Then set these values in `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=servora_db
DB_USER=servora_user
DB_PASSWORD=change-this-password
DB_HOST=localhost
DB_PORT=5432
```

For quick development, the default settings fall back to SQLite when no PostgreSQL environment is provided.

To use PostgreSQL locally, copy `.env.example` to `.env` after creating the database and update the password before running migrations.

## Useful Pages

- Home: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Provider search: `http://127.0.0.1:8000/providers/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Staff analytics: `http://127.0.0.1:8000/analytics/`
- Staff audit logs: `http://127.0.0.1:8000/analytics/audit-logs/`

## Security Notes

- Secrets and database credentials belong in `.env`, never directly in source code.
- `.env`, SQLite database files, media uploads, static build output, and Python caches are ignored by Git.
- Django authentication, password hashing, CSRF middleware, XSS-aware templates, ORM query building, role checks, and staff-only decorators are used throughout the project.
- Verification documents are not shown on public provider profiles.
- Payment records store status and gateway references only. Card numbers, CVV values, banking passwords, and raw payment credentials must never be stored.
- Audit logging records authenticated mutating actions, status codes, and IP address metadata without request bodies.

## Deployment Notes

Before deployment:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=use-a-long-random-secret
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_ENGINE=django.db.backends.postgresql
```

Then run:

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

Use a production WSGI/ASGI server, configure HTTPS, set secure proxy headers at the hosting layer, and store media files in a private or access-controlled location when documents are sensitive.

## GitHub Upload Guide

1. Create a new repository on GitHub named `servora`.
2. In Terminal, run:

```bash
cd /Users/deepprasadsah/Desktop/Projects/servora
git init
git add .
git commit -m "Part 1: scaffold Servora Django application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/servora.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Suggested Part Plan

Part 1: Project scaffold, roles, core models, public UI, seed data.

Part 2: Registration flows for customer/provider, role dashboards, profile forms. Complete.

Part 3: Service category management, provider services, verification upload workflow. Complete.

Part 4: Advanced provider search with filters, pagination, and map markers. Complete.

Part 5: Booking lifecycle and quote workflow. Complete.

Part 6: Reviews, favorites, complaints, notifications, and messaging. Complete.

Part 7: Admin analytics, charts, audit logs, security hardening, tests, and deployment notes. Complete.
