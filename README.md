# Task Management Application

A simple and responsive Task Management Application developed as an internship project. It helps users organize their tasks, track completion status, and manage their work efficiently.

## Features

- **User Registration:** Create an account using a username, email, and password.
- **User Login:** Log in securely using registered credentials.
- **Task Management:** Add, view, update, and delete tasks.
- **Task Status:** Mark tasks as pending or completed.
- **Database Integration:** Store user accounts and tasks in MySQL.
- **User Data Isolation:** Each user can access only their own tasks.
- **Responsive Design:** Designed to work on desktop and mobile screens.
- **API Integration:** Use Flask routes and JavaScript Fetch API for dynamic task operations.

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- MySQL
- Git and GitHub

## Project Structure

```text
TaskManager/
├── app.py
├── database.py
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── signup.html
├── static/
│   ├── style.css
│   └── script.js
├── .env
├── .gitignore
└── README.md
```

## Setup and Installation

1. Install Python and MySQL.
2. Clone this repository:

   ```bash
   git clone https://github.com/ansitamishra29/task-management-application.git
   ```

3. Open the project folder:

   ```bash
   cd task-management-application
   ```

4. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows Command Prompt:

   ```bash
   venv\Scripts\activate.bat
   ```

5. Install the required packages:

   ```bash
   pip install Flask mysql-connector-python python-dotenv
   ```

6. Create a MySQL database named `task_manager_db` and set up the `users` and `tasks` tables according to the project schema.

7. Create a `.env` file in the project root and add your own local configuration:

   ```text
   DB_PASSWORD=your_mysql_password
   SECRET_KEY=your_long_random_secret
   ```

   Replace the example values with your own credentials. Never upload `.env` to GitHub.

8. Start the application:

   ```bash
   python app.py
   ```

9. Open `http://127.0.0.1:5000` in your browser.

## Security Notes

- Passwords are stored as hashes rather than plain text.
- Database credentials and the Flask secret key are kept in the local `.env` file.
- The `.env` file and virtual environment are excluded from Git using `.gitignore`.

## Purpose

This project demonstrates practical application development skills, including authentication, database connectivity, CRUD operations, API handling, responsive UI design, and version control.
