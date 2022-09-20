# HowToApply
HowToApply is a platform that aids the students wanting to apply to certain universities. Here, users can browse the information in a united platform, rather than it being scattered across different websites.

## Installation
1. Clone the repository
    ```
    $ git clone https://github.com/pgmatev/HowToApply
    $ cd HowToApply/
    ```
2. Initialise a virtual environment
    ```
    $ virtualenv venv
    $ source venv/bin/activate
    ```
3. Install the requirements
    ```
    $ pip3 install -r requirements.txt
    ```
4. Set up the database <br>
You need to install PostgreSQL
https://www.postgresql.org/download/ <br>
Then you have to create the database
    ```
    $ psql -U postgres
    postgres=# CREATE DATABASE hta;
    postgres=# quit
    ```
    Make sure that the credentials in the project match <br>
    inside ``HowToApply/hta/settings.py``
    ```
    DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'hta', # should be the name of the database

        'USER': 'postgres', # should match the user owning the database

        'PASSWORD': 'postgres', # user's password

        'HOST': 'localhost',

        'PORT': '5432',

    }
    ```
5. Populate the database
    ```
    $ python3 manage.py migrate
    $ python3 manage.py loaddata subjects.json
    ```
    Additionally you can create an admin 
    ```
    $ python3 manage.py createsuperuser
    ```
6. Run the server
    ```
    $ python3 manage.py runserver
    ```
## Admin guide
To access the admin panel go to ``localhost:8000/admin`` <br>
After registering a university, an admin has to activate it from the user registry in the admin section <br>
