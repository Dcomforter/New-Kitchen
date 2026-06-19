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
  urls.py          # All URL patterns (server-rendered views)
  api_views.py     # DRF API views (menu/cart/order)
  api_urls.py      # URL patterns for the DRF API, mounted at /api/
  serializers.py   # DRF serializers (Menu, Order, Cart)
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

**Order flow** — There are two order paths: `menu_details` (inline on the item page, sets `fulfilled=True` by default) and the cart checkout flow (`add_to_cart` → `checkout` → `submit_order`, sets `fulfilled=False`). The `Order.fulfilled` default differs between these paths. The DRF equivalents mirror this: `MenuOrderAPIView` (POST `/api/menu/<id>/order/`) sets `fulfilled=True`; `CartCheckoutAPIView` (POST `/api/cart/checkout/`) sets `fulfilled=False`.

**Static files** — WhiteNoise serves static files in production. `STATIC_ROOT` is `staticfiles/`; app static files live under `newapp/static/`. Media uploads go to `media/` and are served via Django only when `DEBUG=True`.

**Database** — SQLite (`db.sqlite3`) for development. A PostgreSQL config is commented out in `settings.py` for production use.

**No authentication on customer-facing views** — the Django admin (`/admin`) is the only auth-gated interface. This is why the Order API is write-only (see below).

## API (Django REST Framework)

Mounted at `/api/` (`secondproject/urls.py` → `newapp/api_urls.py`). Built with plain `APIView`/`generics` classes, not `ModelViewSet`+router, so each endpoint's exposure can be controlled individually.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/menu/` | GET | List menu items, supports `?featured=true` |
| `/api/menu/<id>/` | GET | Retrieve one menu item |
| `/api/menu/<id>/order/` | POST | Create a single order (mirrors `menu_details`, `fulfilled=True`) |
| `/api/cart/` | GET | Current session cart + grand total |
| `/api/cart/add/<id>/` | POST | Add item to cart (`quantity`, `order_notes`) |
| `/api/cart/items/<id>/` | PATCH, DELETE | Adjust quantity (`action: increase\|decrease`) or remove item |
| `/api/cart/checkout/` | POST | Create one `Order` per cart line (mirrors `submit_order`, `fulfilled=False`), clears cart |

**`Order` is intentionally write-only** — there is no GET/list/detail endpoint for orders. Since the site has no authentication anywhere, a public read endpoint would leak other customers' names/emails via ID enumeration. Do not add a read endpoint for `Order` without adding auth first.

**`cart.html`'s quantity +/− buttons call the API directly** (`PATCH /api/cart/items/<id>/`) instead of a Django view — this replaced the old `update_quantity` view, which has been deleted. The rest of the cart flow (`add_to_cart`, `remove_from_cart`, `checkout`, `submit_order`) still uses standard server-rendered views; only this one interaction was rewired to the API.

## Models

| Model | Purpose |
|-------|---------|
| `Booking` | Table reservation — name, contact, guest count, country (django-countries), date/time auto-stamped |
| `Menu` | Menu item — food_name, cuisine, price, prep_time, calories, image (ImageField), is_featured flag |
| `Order` | Per-item order record — FK to Menu, customer info, quantity, notes, fulfilled flag |

## Notable Issues to Be Aware Of

- `SECRET_KEY` reads from the `DJANGO_SECRET_KEY` env var (`settings.py`), falling back to the old hardcoded dev value if unset. Set `DJANGO_SECRET_KEY` for any non-local deployment.
- `DEBUG = True` is intentional for now — the app is still in active development. Don't flip it to `False` without being asked; it also gates the `media/` static serving and the dev-only URL patterns.
- `ALLOWED_HOSTS = ['*']` in settings — restrict this in production.
- `setuptools<81` is pinned in `requirements.txt` — `django-countries` imports `pkg_resources`, which was removed in `setuptools>=81`.
