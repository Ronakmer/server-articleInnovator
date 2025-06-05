# Project Setup Guide

## Environment Setup

Activate the virtual environment:

```sh
.\.venv\Scripts\activate
```

## Database Migrations

Run the following commands to apply migrations and set up the default database:

```sh
python manage.py makemigrations
python manage.py migrate
```

For the second app `AIMessageService` with its own database (`ai_messages_db`), run:

```sh
python manage.py makemigrations AIMessageService
python manage.py migrate --database=ai_messages_db
```

## Superuser Creation

Create a superuser for Django admin access on the default database:

```sh
python manage.py createsuperuser
```

To create a superuser for the second database:

```sh
python manage.py createsuperuser --database=ai_messages_db
```

## Running the Server

### Create SSL Certificate File (`cert.crt`)

If you don’t have an SSL certificate yet, you can create a self-signed certificate using OpenSSL:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.crt -days 365 -nodes
```

This command generates a new private key (`key.pem`) and a self-signed certificate (`cert.crt`) valid for 365 days.

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

* 192.168.1.3
* 192.168.1.4
* 192.168.1.5

## Additional Commands

### Run Scripts in Django Shell

Execute scripts using the Django shell:

```sh
python manage.py shell < all_permissions.py
python manage.py shell < all_role_has_permissions.py
```

---

Let me know if you want me to tailor this further or add anything else!
