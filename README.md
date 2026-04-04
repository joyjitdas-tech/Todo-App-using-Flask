# Flask Todo App

A simple **Todo application** built with **Flask** that allows users to register, log in, and manage their tasks. Users can add new tasks with a title, description, due date, and time, mark tasks as completed, edit, and delete tasks.

---

## **Features**

- User authentication: Register, login, and logout.
- Add new tasks with:
  - Title
  - Description
  - Due date
  - Deadline time
- Mark tasks as completed/uncompleted
- Edit and delete tasks
- Responsive UI
- Flash messages for actions
- Simple, clean design with CSS

---

## **Folder Structure**
todo_app/
│
├── [run.py]        # App entry point
├── app/
│   ├── init.py         # Initialize Flask, DB, login_manager
│   ├── models/
│   │   ├── init.py     # Import models
│   │   ├── [user.py]        # User model
│   │   └── [todo.py]       # Task model
│   ├── routes/
│   │   ├── init.py     # Empty
│   │   ├── [auth.py]       # Login/Register/Logout
│   │   └── [tasks.py]      # Dashboard, Add, Delete, Toggle status
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       └── add_task.html
└── venv/
