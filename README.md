# Gym Management API

This Flask application manages gym members and workout sessions using MySQL as the database backend.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Flask
- Flask-Marshmallow
- mysql-connector-python

2. **Set up MySQL database:**

- Create a database named `gym_db`.
- Configure MySQL user credentials (`user`, `password`, `host`) in `app.py`.

3. **Run the application:**

## API Endpoints

### Members

- **GET** `/members`

Retrieves all gym members.

- **POST** `/members`

Adds a new member.

- **PUT** `/members/<int:id>`

Updates a specific member.

### Workouts

- **POST** `/workouts`

Schedules a workout session.

- **PUT** `/workouts/<int:id>`

Updates a workout session.

- **GET** `/workouts`

Retrieves all workout sessions.

- **GET** `/members/<int:member_id>/workouts`

Retrieves all workout sessions for a specific member.