Timetable Website
A web application designed to manage classrooms and course schedules across four campuses. The application allows users to add and remove classrooms, add and remove courses, and generate and view timetables for each campus and individual classrooms.

Project Overview
The Timetable Website simplifies campus scheduling management by providing a user-friendly interface for administrators to manage course schedules across multiple campuses. With this application, administrators can:

Add and delete classrooms for each campus
Add and delete courses
Generate timetables for all four campuses
View the timetable for each specific classroom within any campus

Table of Contents
Installation
Usage
File Structure
Technology Stack
Contributing
License

Installation
Clone the Repository:
git clone https://github.com/Kaki-Liu/IT-project-2024.git
cd timetable-website

Install Dependencies: Ensure you have Python and Node.js installed. Then, install necessary Python packages:
pip install -r requirements.txt

Install any required frontend dependencies if applicable:
npm install

Set Up the Database: Configure your database connection in the settings file. Run migrations or initial setup scripts as needed:
python manage.py migrate

Run the Application: Start the development server:
python main.py
Access the Application: Open your browser and go to http://localhost:8000 to start using the Timetable Website.

Usage
1. Manage Classrooms: Add or delete classrooms across any of the four campuses.
2. Manage Courses: Add or remove courses for the scheduling system.
3. Generate Timetables: Automatically generate and review timetables for each campus.
4. View Classroom Schedules: Access the schedule of any specific classroom to see its course assignments.

File Structure
The project is organized as follows:

main.py: Main entry point of the application.
front-end/: Contains the frontend code, including HTML, CSS, and JavaScript files.
test/: Includes unit and integration tests for different modules.
feature/: Contains feature modules for specific functionalities like classroom management, course management, and timetable generation.
algorithm/: Contains algorithms for scheduling and timetable optimization.

Technology Stack
Backend: Python, Flask
Frontend: HTML, JavaScript
Database: PostgreSQL 
ORM: SQLAlchemy 
Other Tools: Docker for containerization, CI/CD pipelines for automated testing and deployment

Contributing
We welcome contributions to the Timetable Website project! Please follow these steps:

Fork the Repository: Create your own branch for any changes.
Create a New Branch: Name it something relevant, such as feature/add-classroom-management.
Commit Your Changes: Add clear, concise commit messages.
Submit a Pull Request: Ensure your code is tested and adheres to the coding standards before submitting.