# Flask Cantor Application
This is a Flask Cantor application for managing user registrations, logins, and basic financial transactions. The application uses Flask, SQLAlchemy, and Flask-Login for user authentication.
## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Usage and installation](#installation)
4. [File Structure](#file-structure)
5. [Database Structure](#database)
6. [Todo List](#todo-list)
7. [Technologies and libraries used](#tech)

<a name="introduction"></a>
## Introduction
The Flask Cantor application provides functionality for user registration, login, buying, selling, and viewing transaction history. It uses Flask for web development, SQLAlchemy for database interaction, and Flask-Login for user authentication.
<a name="prerequisites"></a>
## Prerequisites
- Python 3
- Flask
- Flask-Session
- Flask-SQLAlchemy
- Flask-WTF
- WTForms
- Requests
 
<a name="installation"></a>
## Usage and installation
#### 1. Clone the repository::
            git clone https://github.com/xprcode/Cantor_Flask_Web_Aplication.git
#### 2. Create and activate a virtual environment::
            virtualenv env -p python3
            source env/Scripts/activate
#### 3. Install requirements::
            pip install flask
                        flask-session
                        flask-sqlalchemy
                        flask-login
                        wtforms
                        flask-wtf
                        flask-migrate
                        email-validator
                        requests
                        python-dotenv

#### 4. Run the aplication

            flask run
            Open your browser and go to http://localhost:5000.
   
#### 5. Initialization of database::
To initialize the database:
- flask db init
- flask db migrate -m "initializing db"
- flask db upgrade
Register a new user, login, and explore the application.


<a name="database"></a>
## Database Structure

### User Class

The `User` class represents a user in the application and is used to interact with the database. It is defined as follows:

### Attributes:
- id: Primary key for the user.
- name: Unique username for the user.
- password: User's password (Note: Storing passwords using password hashing and salting).
- email: User's email address
#### Relationships:
- portfolio: User's currency portfolio records.
- history: User's transaction history.

### Portfolio Class

The `Portfolio` class represents the currencies refered amounts which a user has.

### History

The `History` class represents all buy and sell actions made by a customer.


<a name="todo-list"></a>
## Todo List

- [x] User registration
- [x] User login/logout
- [x] Buying functionality 
- [x]Selling functionality 
- [ ] Viewing transaction history )


<a name="(#tech)"></a>
## Technologies and libraries used

The Flask Cantor application is built using the following technologies and libraries:

- **Flask**: Flask-Session, Flask-SQLAlchemy, Flask-Login, Flask-WTF,
- **Werkzeug**,
- **SQLAlchemy**,
- **WTForms**,
- **Python urllib.parse**,
- **Python os.path**,
- **Jinja2**,
- **Bootstrap**,


   
