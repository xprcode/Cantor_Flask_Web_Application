# Flask Cantor Application

This is a Flask Cantor application for managing user registrations, logins, and basic financial transactions. The application uses Flask, SQLAlchemy, and Flask-Login for user authentication.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Todo List](#todo-list)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The Flask Cantor application provides functionality for user registration, login, buying, selling, and viewing transaction history. It uses Flask for web development, SQLAlchemy for database interaction, and Flask-Login for user authentication.

## Prerequisites

- Python 3
- Flask
- Flask-Session
- Flask-SQLAlchemy
- Flask-WTF
- WTForms

## Installation


## Usage and installation

### 1. Clone the repository::

            git clone https://github.com/xprcode/Cantor_Flask_Web_Aplication.git

### 2. Create and activate a virtual environment::

            virtualenv env -p python3
            source env/Scripts/activate

### 3. Install requirements::

pip install flask
            flask_session
            flask_sqlalchemy
            flask_login
            wtforms
            flask_wtf
            email_validator

### 4. Run the aplication

flask run
Open your browser and go to http://localhost:5000.
   
### 5. Initialization of database::

To initialize the database:
URL/init

Register a new user, login, and explore the application.



### 6. File structure 
- app.py: Main application file containing the Flask app and routes.
- config.cfg: Configuration file for Flask or other configurations.
- data: Dictionary with database file. 
- templates: Directory containing HTML templates for your Flask app.
- modules: Directory for Python modules, such as forms.py.
- venv: Virtual environment directory.
- README.md: Project README file with information about the project, usage, and contributions.

## Todo List

- [x] User registration
- [x] User login/logout
- [ ] Buying and selling functionality
- [ ] Viewing transaction history
- [ ] Implementing user dashboard
- [ ] Enhancing security measures


   
