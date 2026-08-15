# Gujarati Matrimonial MVP (Django)

Family-friendly matrimonial MVP focused on profile quality and interest flow.

## Stack

- Django
- Django REST Framework
- JWT (SimpleJWT)
- SQLite by default, PostgreSQL supported via environment variables
- Django Templates + Bootstrap UI

## MVP features

- Registration/Login/Forgot password
- JWT auth APIs for login/register/refresh
- Rich Gujarati profile:
  - About me
  - Education & career
  - Family
  - Gujarati background
  - Partner preferences
- Photo upload/delete + primary photo
- Profile completion %
- Activate/deactivate profile
- Browse/search/filter/sort profiles
- Send/accept/decline/withdraw interests
- Shortlist
- Block and report profile
- Django Admin management
- English + Gujarati language switch foundation

## Project apps

- `accounts` - registration, login, JWT auth
- `profiles` - profile, preference, photos
- `matching` - compatibility and recommended matches
- `interests` - interests and block
- `shortlists` - dedicated shortlist module and pages
- `search` - browse/filter
- `reports` - reporting flow
- `locations` - locations and communities
- `common` - shared base models and success stories

## Run locally

```powershell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000

## PostgreSQL (optional)

Set:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

If `POSTGRES_DB` is present, Django uses PostgreSQL.

## Email verification

Email verification is intentionally disabled right now and kept for future implementation.
