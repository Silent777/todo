# Event Handler

## Description
This is the source code of the service which is called "Event Handler". This app provides flexible and effective event management.

## Technologies
* Python (3.6.3)
* PostgreSQL (9.5.9)
* Django (1.11)

## Install
For the next steps of service installation, you will need setup of Ubuntu OS

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```


### Go to the cloned repository and install requirement project's packages
```
pip install -r requirements.txt
```

* Go to the `/event_handler` project directory and create your own local_settings.py in the folder with settings.py and configure correct database connection.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_custom_db_name',
        'USER': 'your_custom_db_user',
        'PASSWORD': 'your_password_for_user_above',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


* Go to the folder with `manage.py` file and run migrate files
```
python manage.py migrate
```

## Run Project


### Django
Go to the folder with `manage.py` file, run api
```
python manage.py runserver
```
