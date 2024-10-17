# Inventory Management API

## Overview

The Inventory Management API is a RESTful API that allows users to manage inventory items, including creating, retrieving, updating, and deleting items. This API is built using Django and Django REST Framework, and it utilizes JWT authentication for secure access.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Running Tests](#running-tests)
- [Logging](#logging)

## Requirements

- Python 3.12 or higher
- Django 5.1 or higher
- Django REST Framework
- Django REST Framework Simple JWT

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/inventory_management.git
   cd inventory_management

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Setup

1. Database Migration: Apply the database migrations to set up your database:

```bash
python manage.py migrate
```
2. Run the Development Server:

```bash
python manage.py runserver
```
The API will be accessible at http://localhost:8000.

3. Create a Superuser (optional, for accessing the admin panel):

```bash
python manage.py createsuperuser
```

## API Documentation

For detailed API documentation, please refer to the API Documentation.

## Usage Examples
### Authentication Example

```bash
# Obtain JWT token
curl -X POST http://localhost:8000/api/token/ -d "username=yourusername&password=yourpassword"

# Use the token to access protected endpoints
curl -H "Authorization: Bearer your_token" http://localhost:8000/inventory/items/
```

### Create Item Example
```bash
curl -X POST http://localhost:8000/inventory/items/ \
-H "Authorization: Bearer your_token" \
-H "Content-Type: application/json" \
-d '{
  "name": "New Item",
  "description": "A description for the new item",
  "quantity": 20,
  "price": "29.99"
}'
```

## Running Tests

To run the unit tests, execute the following command:

```bash
python manage.py test
```

## Logging

The application includes a logging system to track API usage, errors, and other significant events. Logs can be found in the console output when the server is running.