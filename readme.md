# Project Setup Guide

## Environment Setup

Activate the virtual environment:
```sh
.\.venv\Scripts\activate
```

## Database Migrations
Run the following commands to apply migrations and set up the database:
```sh
python manage.py makemigrations
python manage.py migrate
```

## Superuser Creation
Create a superuser for Django admin access:
```sh
python manage.py createsuperuser
```

## Running the Server

### Start Development Server (HTTP)
```sh
python manage.py runserver
```

### Start Secure Server (HTTPS)
Ensure `django-extensions` is installed:
```sh
pip install django-extensions
```
Run the server with an SSL certificate:
```sh
python manage.py runserver_plus --cert-file cert.crt
```

### Run Server on a Specific Host/IP
To run on a specific IP address:
```sh
python manage.py runserver_plus 192.168.1.5:8000 --cert-file cert.crt
```
Available IP Addresses:
- 192.168.1.3
- 192.168.1.4
- 192.168.1.5

## Additional Commands

### Run Scripts in Django Shell
Execute scripts using the Django shell:
```sh
python manage.py shell < all_permissions.py
python manage.py shell < all_role_has_permissions.py
```

---
This guide ensures a structured approach to setting up and running the project efficiently.

