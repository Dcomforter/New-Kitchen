# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Dcomforters' Kitchen** — a Django restaurant web app for menu browsing, table reservations, and food ordering. Live at https://dcomforter.pythonanywhere.com.

## Common Commands

```bash
# Run development server
python manage.py runserver

# Apply migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Run all tests
python manage.py test

# Run a single test class or method
python manage.py test newapp.tests.BookingModelTest
python manage.py test newapp.tests.BookingModelTest.test_booking_fields

# Collect static files (needed before container deployment)
python manage.py collectstatic --noinput

# Create admin superuser
python manage.py createsuperuser
```

## Container / CI

```bash
# Local dev with Docker
docker-compose up --build           # runs on port 8200

# Podman (used by Jenkins CI)
podman compose up -d --build        # runs on port 8600, uses Containerfile
```

The `entrypoint.sh` runs `migrate` and optionally `loaddata all_data.json` before starting the server — place fixture data in `all_data.json` at the project root to seed the DB on container start.

The `Jenkinsfile` drives the Podman-based CI/CD pipeline. `Jenkinsfile-AKS` targets Kubernetes (EKS/GKE) deployments provisioned via Terraform.

## Architecture

```
secondproject/     # Django project config (settings, root URLs, wsgi/asgi)
newapp/            # Single Django app — all business logic lives here
  models.py        # Booking, Menu, Order
  views.py         # All view functions (no class-based views)
  urls.py          # All URL patterns
  cart.py          # Cart class — thin wrapper around request.session['cart']
  forms.py         # BookingForm, OrderForm
  templates/       # App-level templates
    partials/      # _header.html, _footer.html
  static/          # CSS, JS, images
staticfiles/       # collectstatic output (do not edit directly)
media/             # User-uploaded images (Menu.image field)
```

### Key architectural points

**Session-based cart** — `cart.py:Cart` stores items as `{str(item_id): {quantity, order_notes}}` in `request.session['cart']`. `views.py:view_cart` includes a migration shim that converts legacy `int` values to dicts. The `Cart` class and raw session dict are both used across views — prefer the `Cart` class for new code.

**Order flow** — There are two order paths: `menu_details` (inline on the item page, sets `fulfilled=True` by default) and the cart checkout flow (`add_to_cart` → `checkout` → `submit_order`, sets `fulfilled=False`). The `Order.fulfilled` default differs between these paths.

**Static files** — WhiteNoise serves static files in production. `STATIC_ROOT` is `staticfiles/`; app static files live under `newapp/static/`. Media uploads go to `media/` and are served via Django only when `DEBUG=True`.

**Database** — SQLite (`db.sqlite3`) for development. A PostgreSQL config is commented out in `settings.py` for production use.

**No authentication on customer-facing views** — the Django admin (`/admin`) is the only auth-gated interface.

## Models

| Model | Purpose |
|-------|---------|
| `Booking` | Table reservation — name, contact, guest count, country (django-countries), date/time auto-stamped |
| `Menu` | Menu item — food_name, cuisine, price, prep_time, calories, image (ImageField), is_featured flag |
| `Order` | Per-item order record — FK to Menu, customer info, quantity, notes, fulfilled flag |

## Notable Issues to Be Aware Of

- `SECRET_KEY` in `settings.py` is hardcoded and should be moved to an environment variable for any non-local deployment.
- `ALLOWED_HOSTS = ['*']` in settings — restrict this in production.
