import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with the frontend

# Sample data for demonstration
students = {
    "101": {
        "first_name": "Ayas",
        "last_name": "Rehman",
        "semester": "Fall",
        "year": 2024,
        "password": "SecurePass1@",  # Example password
        "courses": [
            {
                "course_number": "INFO530",
                "course_name": "Systems Development",
                "section_number": "001",
                "meeting_room": "Room 2125",
                "meeting_days": "MW",
                "meeting_times": "17:30 - 18:45",
                "instructor_name": "Dr. Ugo Etudo",
                "num_students": 30,
                "description": "An introduction to systems development.",
                "modality": "Hybrid"
            }
        ]
    },
    "102": {
        "first_name": "Madhumitha",
        "last_name": "Pollamreddy",
        "semester": "Fall",
        "year": 2024,
        "password": "SecurePass2@",
        "courses": [
            {
                "course_number": "INFO540",
                "course_name": "Data Analytics",
                "section_number": "002",
                "meeting_room": "Room 202",
                "meeting_days": "TTh",
                "meeting_times": "17:30 - 18:45",
                "instructor_name": "Dr. White",
                "num_students": 25,
                "description": "A course on data analysis techniques.",
                "modality": "Hybrid"
            },
            {
                "course_number": "CS101",
                "course_name": "Introduction to Computer Science",
                "section_number": "003",
                "meeting_room": "Room 303",
                "meeting_days": "MWF",
                "meeting_times": "09:00 - 10:00",
                "instructor_name": "Prof. Brown",
                "num_students": 50,
                "description": "Basic concepts in computer science.",
                "modality": "In-person"
            }
        ]
    },
    "103": {
        "first_name": "Mohith",
        "last_name": "Prasanna",
        "semester": "Fall",
        "year": 2024,
        "password": "SecurePass3@",
        "courses": [
            {
                "course_number": "INFO530",
                "course_name": "Systems Development",
                "section_number": "001",
                "meeting_room": "Room B2125",
                "meeting_days": "MW",
                "meeting_times": "17:30 - 18:45",
                "instructor_name": "Dr. Ugo Etudo",
                "num_students": 30,
                "description": "An introduction to systems development.",
                "modality": "Hybrid"
            }
        ]
    },
    "104": {
        "first_name": "Bob",
        "last_name": "Smith",
        "semester": "Fall",
        "year": 2024,
        "password": "SecurePass4@",
        "courses": [
            {
                "course_number": "MATH200",
                "course_name": "Calculus II",
                "section_number": "004",
                "meeting_room": "Room 404",
                "meeting_days": "TTh",
                "meeting_times": "11:00 - 12:30",
                "instructor_name": "Dr. Green",
                "num_students": 40,
                "description": "Advanced calculus concepts.",
                "modality": "In-person"
            },
            {
                "course_number": "PHYS150",
                "course_name": "Physics I",
                "section_number": "005",
                "meeting_room": "Room 505",
                "meeting_days": "MWF",
                "meeting_times": "14:00 - 15:00",
                "instructor_name": "Dr. Blue",
                "num_students": 35,
                "description": "Introduction to classical mechanics.",
                "modality": "Fully remote"
            }
        ]
    }
}

# Function to validate password with constraints
def is_valid_password(password):
    if (len(password) < 8 or
        not re.search("[a-z]", password) or
        not re.search("[A-Z]", password) or
        not re.search("[0-9]", password) or
        not re.search("[@#$%^&+=]", password)):
        return False
    return True

# Function to check if login time is 15 minutes before class
def is_login_before_class(course):
    current_time = datetime.now().strftime("%H:%M")  # Get current time
    class_times = course['meeting_times'].split('-')  # Split meeting times by '-'
    class_start_time = class_times[0].strip()  # Extract start time and remove extra spaces

    try:
        # Convert time strings to datetime objects for comparison
        current_time_obj = datetime.strptime(current_time, "%H:%M")
        class_start_time_obj = datetime.strptime(class_start_time, "%H:%M")

        # Calculate time difference
        time_diff = class_start_time_obj - current_time_obj

        # Check if login is within 15 minutes before class starts
        return 0 < time_diff.total_seconds() <= 15 * 60
    except ValueError as e:
        print(f"Error parsing time: {e}")
        return False

# Route to handle student login
@app.route('/login', methods=['POST'])
def login():
    student_id = request.json.get('student_id')
    password = request.json.get('password')

    student = students.get(student_id)
    if student:
        # In practice, you should compare hashed passwords
        if password == student['password']:
            # Check if any course is about to start in 15 minutes
            for course in student['courses']:
                if is_login_before_class(course):
                    return jsonify({
                        "message": "Login successful",
                        "alert": f"Your class {course['course_name']} starts in 15 minutes!",
                        "alert_color": "red",
                        "student": student
                    }), 200

            return jsonify({"message": "Login successful", "student": student}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "Student not found"}), 404

# Route to fetch course details
@app.route('/course/<course_number>', methods=['GET'])
def course_details(course_number):
    for student in students.values():
        for course in student['courses']:
            if course['course_number'] == course_number:
                return jsonify(course), 200
    return jsonify({"error": "Course not found"}), 404

# Route to register a new student
@app.route('/register', methods=['POST'])
def register():
    student_id = request.json.get('student_id')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')

    # Validate password
    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain one lowercase letter, one uppercase letter, one number, and one special character."}), 400

    # Check if student already exists
    if student_id in students:
        return jsonify({"error": "Student already exists"}), 400
    else:
        # Register the student (In practice, you should hash the password before storing it)
        students[student_id] = {
            "first_name": first_name,
            "last_name": last_name,
            "semester": "Fall",  # Default value; you can adjust as needed
            "year": 2024,        # Default value; adjust as necessary
            "password": password,
            "courses": []
        }
        return jsonify({"message": "Student registered successfully"}), 201

# Fix the main entry point
if __name__ == '__main__':
    app.run(debug=True)
