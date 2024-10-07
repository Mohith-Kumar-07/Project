// frontend/static/js/app.js
function fetchStudentSchedule() {
    const studentId = document.getElementById('student-id').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ student_id: studentId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displaySchedule(data);
        }
    })
    .catch(error => console.error('Error:', error));
}

function displaySchedule(studentData) {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('schedule-section').style.display = 'block';
    document.getElementById('schedule-heading').innerText = `${studentData.semester}, ${studentData.year} Schedule for ${studentData.first_name} ${studentData.last_name}`;

    const courseList = document.getElementById('course-list');
    courseList.innerHTML = ''; // Clear previous content

    studentData.courses.forEach(course => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>${course.course_number}: ${course.course_name}</strong><br>
            Section: ${course.section_number}, Room: ${course.meeting_room}<br>
            Days: ${course.meeting_days}, Time: ${course.meeting_times}<br>
            <button onclick="viewCourseDetails('${course.course_number}')">View Details</button>
        `;
        courseList.appendChild(listItem);
    });
}

function viewCourseDetails(courseNumber) {
    fetch(`http://127.0.0.1:5000/course/${courseNumber}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(`Course: ${data.course_name}\nInstructor: ${data.instructor_name}\nStudents: ${data.num_students}\nDescription: ${data.description}\nModality: ${data.modality}`);
        }
    })
    .catch(error => console.error('Error:', error));
}
