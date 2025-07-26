# Najada demo
Demo project for Najada games.

# 1 Technical specification
## 1.2 User Scenarios
1. As an user I want to see list of an items with their availability.
2. From listed items as an user I want add item into the cart with note and specified quantity. Also I want to have possibility to remove any item from cart.
3. As an user I want to edit item quantity in cart.
4. As an user I want to see list of an items in my cart. See total price for all items in cart.
5. As an user I want to submit order with my cart.
6. As an user after order submit I want to see state of my order.


## 1.3 Specifics
### 1.3.1 Availability
For simplicity removes item from stock when the order is submitted. But this not only way how to resolve availability.
In theory there are cases where could be better reserving items in cart, so customer has his cart items with guaranteed availability.

### 1.3.2 Service Layer
Service layer adds a separate layers of code between views and models.
This design pattern develops uniform feel to an application and builds bridge between software and business logic.

This design pattern and methodology is inspired by Talk of Radoslav Georgiev - Django structure for scale and longevity https://www.youtube.com/watch?v=yG3ZdxBb1oo


## 1.4. Data model
<img src="data_model.png" alt="data model" width="500" height="500" />


# 2 Development
## 2.1 Local development
### 2.1.1 Prerequisites
 * Installed postgres database.
 * Python 3.10

### 2.1.2 DB Initialization
open psql:
```bash
psql -U postgres
```
and execute:
```SQL
CREATE ROLE baguetteuser WITH LOGIN PASSWORD 'mysecretpassword';
CREATE DATABASE baguettedb OWNER baguetteuser;
GRANT ALL PRIVILEGES ON DATABASE baguettedb TO baguetteuser;
\q
```
* be sure to use credentials set in .env file
### 2.1.3 Environment preparation
Create virtual env. e.g.
```bash
virtualenv venv
```
activate env.
```bash
/venv/Scripts/Activate  # source /venv/bin/activate for linux users
```

### 2.1.4 App Initialization
In `/django_project` directory Check for model changes and migrate.
```python
python .\manage.py makemigrations
python .\manage.py migrate
```
And load initial data
```python
python .\manage.py loaddata initial_data.json
```
### 2.1.5 Run server

```python
python .\manage.py runserver
```
* For local testing resources under user authentication (cart, order etc,) use Basic Auth and user `testuser` with password `password123`

## 2.2 Development with Docker
Simply run following and you are set to go in no time.
```bash
docker compose build up -d
```
* DB model check,migrations and initial data load are part of entrypoint.sh execution

## 2.3 Tests
For tests run in active virtual env.
```bash
pytest
```
## 2.4 Linting
To check linting run in `/django_project`
```bash
flake8 .
```

## 2.4 Logging
Logs are located in `/django_project/api.log`
