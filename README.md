# Flask Cantor Application

This is a Flask Cantor application for managing user registrations, logins, and basic financial transactions. The application uses Flask, SQLAlchemy, and Flask-Login for user authentication.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Usage and installation](#installation)
4. [File Structure](#file-structure)
5. [Todo List](#todo-list)

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

<a name="installation"></a>
## Usage and installation

#### 1. Clone the repository::

            git clone https://github.com/xprcode/Cantor_Flask_Web_Aplication.git

#### 2. Create and activate a virtual environment::

            virtualenv env -p python3
            source env/Scripts/activate

#### 3. Install requirements::

            pip install flask
                        flask_session
                        flask_sqlalchemy
                        flask_login
                        wtforms
                        flask_wtf
                        email_validator

#### 4. Run the aplication

            flask run
            Open your browser and go to http://localhost:5000.
   
#### 5. Initialization of database::

To initialize the database:
            URL/init

Register a new user, login, and explore the application.

<a name="file-structure"></a>
## File structure 
- app.py: Main application file containing the Flask app and routes.
- config.cfg: Configuration file for Flask or other configurations.
- data: Dictionary with database file. 
- templates: Directory containing HTML templates for your Flask app.
- modules: Directory for Python modules, such as forms.py.
- venv: Virtual environment directory.
- README.md: Project README file with information about the project, usage, and contributions.

<a name="todo-list"></a>
## Todo List

- [x] User registration
- [x] User login/logout
- [ ] Buying and selling functionality (API, SQL)
- [ ] Viewing transaction history (SQL)
- [ ] Implementing user dashboard
- [ ] Quote function (API)

## Technologies and Libraries Used

The Flask Cantor application is built using the following technologies and libraries:

- **Flask**: A lightweight web application framework for Python.
- **Flask-Session**: An extension for handling sessions in Flask applications.
- **Flask-SQLAlchemy**: A Flask extension for SQLAlchemy, a SQL toolkit, and Object-Relational Mapping (ORM) library.
- **Flask-Login**: Provides user session management for Flask.
- **Werkzeug**: A utility library for WSGI (Web Server Gateway Interface) applications, used in Flask.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **WTForms**: A library for creating and validating web forms in Flask applications.
- **Flask-WTF**: An integration of WTForms with Flask.
- **SQLite**: A C library that provides a lightweight, disk-based database.
- **Python urllib.parse**: Library for parsing URLs.
- **Python os.path**: Module for common pathname manipulations.
- **Jinja2**: A modern and designer-friendly templating engine for Python.
- **Bootstrap**: A popular CSS framework for building responsive and visually appealing web pages.
- **jQuery**: A fast, small, and feature-rich JavaScript library.


   
