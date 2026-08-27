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

Part 4: Advanced provider search with filters, pagination, and map markers.

Part 5: Booking lifecycle and quote workflow.

Part 6: Reviews, favorites, complaints, notifications, and messaging.

Part 7: Admin analytics, charts, audit logs, security hardening, tests, and deployment notes.
