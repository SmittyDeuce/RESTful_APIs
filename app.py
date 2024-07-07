from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    trainer_id = fields.Integer(required=True)

    class Meta:
        fields = ("name", "age", "trainer_id")

class WorkoutSessionSchema(ma.Schema):
    date = fields.Date(required=True)
    duration_min = fields.Integer(required=True)
    cal_burned = fields.Integer(required=True)
    member_id = fields.Integer(required=True)
    trainer_id = fields.Integer(required=True)

    class Meta:
        fields = ("date", "duration_min", "cal_burned", "member_id", "trainer_id")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

def get_db_connection():
    db_name = "gym_db"
    user = "root"
    password = ""
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        print("Connection to database successful")
        return conn

    except Error as e:
        print(f"Error: {e}")
        return None

@app.route("/")
def home():
    return "Welcome to the Gym"

@app.route("/members", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM members"
        cursor.execute(query)

        members = cursor.fetchall()
        return members_schema.jsonify(members)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members", methods=["POST"])
def add_members():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Validation Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member_data = (member_data["name"], member_data["age"], member_data["trainer_id"])

        query = "INSERT INTO members (name, age, trainer_id) VALUES (%s, %s, %s)"
        cursor.execute(query, new_member_data)
        conn.commit()

        return jsonify({"message": "New Member added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["PUT"])
def update_members(id):
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Validation Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member_data = (member_data["name"], member_data["age"], member_data["trainer_id"], id)

        query = "UPDATE members SET name = %s, age = %s, trainer_id = %s WHERE id = %s"
        cursor.execute(query, updated_member_data)
        conn.commit()

        return jsonify({"message": "Member information updated"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workouts", methods=["POST"])
def schedule_workout():
    try:
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout_data = (workout_data["date"], workout_data["duration_min"], workout_data["cal_burned"], workout_data["member_id"], workout_data["trainer_id"])

        query = "INSERT INTO workout_sessions (date, duration_min, cal_burned, member_id, trainer_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, new_workout_data)
        conn.commit()

        return jsonify({"message": "Workout session scheduled successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workouts/<int:id>", methods=["PUT"])
def update_workout(id):
    try:
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_workout_data = (workout_data["date"], workout_data["duration_min"], workout_data["cal_burned"], workout_data["member_id"], workout_data["trainer_id"], id)

        query = "UPDATE workout_sessions SET date = %s, duration_min = %s, cal_burned = %s, member_id = %s, trainer_id = %s WHERE id = %s"
        cursor.execute(query, updated_workout_data)
        conn.commit()

        return jsonify({"message": "Workout session updated successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workouts", methods=["GET"])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM workout_sessions"
        cursor.execute(query)

        workouts = cursor.fetchall()
        return workout_sessions_schema.jsonify(workouts)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:member_id>/workouts", methods=["GET"])
def get_member_workouts(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM workout_sessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))

        workouts = cursor.fetchall()
        return workout_sessions_schema.jsonify(workouts)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)
