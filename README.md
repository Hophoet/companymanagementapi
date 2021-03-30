# XEARTH

## Setup

### Install dependencies from dependencies file:
```bash
pip install -r requirements.txt
```

### Perform database migration:
```bash
python manage.py check
python manage.py migrate
```

## Run Development Server

```bash
python manage.py runserver
```
Local api is at http://localhost:8000

Hosted on heroku api is at  https://companymanagementapi.herokuapp.com/, `user: admin`, `password: password`

## Testing

### Run tests:
```bash
python manage.py test
```

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 14 tests in 0.025s

OK
Destroying test database for alias 'default'...
```

### Run tests with coverage:
```bash
coverage run manage.py test
```

### Check coverage report:
```bash
coverage report
```

