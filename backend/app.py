# student data (backend)
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with frontend

# Sample data for demonstration
students = {
    "101": {
        "first_name": "Ayas",
        "last_name": "Rehman",
        "semester": "Fall",
        "year": 2024,
        "courses": [
            {
                "course_number": "INFO530",
                "course_name": "Systems Development",
                "section_number": "001",
                "meeting_room": "Room 2125",
                "meeting_days": "MW",
                "meeting_times": "5:30pm - 6:45pm",
                "instructor_name": "Dr. Ugo Etudo",  # Fixed missing closing quotation mark here
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
        "courses": [
            {
                "course_number": "INFO540",
                "course_name": "Data Analytics",
                "section_number": "002",
                "meeting_room": "Room 202",
                "meeting_days": "TTh",
                "meeting_times": "1:00 PM - 2:30 PM",
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
                "meeting_times": "9:00 AM - 10:00 AM",
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
        "courses": [
            {
                "course_number": "INFO530",
                "course_name": "Systems Development",
                "section_number": "001",
                "meeting_room": "Room B2125",
                "meeting_days": "MW",
                "meeting_times": "5:30pm - 6:45pm",
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
        "courses": [
            {
                "course_number": "MATH200",
                "course_name": "Calculus II",
                "section_number": "004",
                "meeting_room": "Room 404",
                "meeting_days": "TTh",
                "meeting_times": "11:00 AM - 12:30 PM",
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
                "meeting_times": "2:00 PM - 3:00 PM",
                "instructor_name": "Dr. Blue",
                "num_students": 35,
                "description": "Introduction to classical mechanics.",
                "modality": "Fully remote"
            }
        ]
    }
}

# Route to handle student login
@app.route('/login', methods=['POST'])
def login():
    student_id = request.json.get('student_id')
    student = students.get(student_id)
    if student:
        return jsonify(student), 200
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

if __name__ == '__main__':
    app.run(debug=True)
