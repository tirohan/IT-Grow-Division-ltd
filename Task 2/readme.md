# User Management System

The User Management System is a simple Python application that allows users to create, read, update, and delete user records in a SQLite database. This project is designed for basic user data management.

## Table of Contents

- [User Management System](#user-management-system)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Database Structure](#database-structure)

## Introduction

The User Management System provides a user-friendly interface to interact with a SQLite database. Users can perform the following operations:

- Create new user records.
- Retrieve user information, either a single user or all users.
- Update user records.
- Delete user records.

This project is ideal for learning database interactions in Python and basic CRUD operations.

## Features

- Create new user records with name, age, gender, and salary.
- Retrieve user records by ID or view all users.
- Update user records with new information.
- Delete user records by ID.
- Error handling for database-related issues.

## Getting Started

Follow these instructions to set up and run the User Management System on your local machine.

### Prerequisites

Ensure you have the following software installed:

- Python 3.x
- SQLite (comes pre-installed with Python)

## Database Structure
The SQLite database used in this project has the following structure:

USERS table:
id (Primary Key): An auto-incrementing integer that uniquely identifies each user.
name: A text field for storing the user's name.
age: An integer field for the user's age.
gender: A text field for the user's gender.
salary: An integer field for the user's salary.
This structure is designed to store basic user information in a normalized form.




