# Smart University Academic Management System (SUAMS)

A beginner-friendly Python 3 + Tkinter desktop project for a Software Engineering assignment. It uses fictional demo data stored in Python lists and dictionaries. There is no database, backend server, or online API. Data changes reset when the application closes.

## Features

- Four demo roles with role-specific navigation: Student, Teacher, Administrator, Examination Controller.
- Admission application review and approval/rejection.
- Course registration with duplicate checks and an 18-credit limit.
- Semester enrollment with duplicate-enrollment prevention.
- Examination form submission and controller approval.
- Automatic sequential examination routine generation with unique rooms and time slots.
- Continuous assessment total, grade, GPA and pass/fail calculation.
- Teacher-student advising records and comments.
- Observer-pattern academic notifications.
- Student performance table and optional Matplotlib bar chart.
- Demo student, teacher, course, semester, admission, examination, mark, advising and notification data.

## Requirements

- Windows 10/11 (also works on other desktop systems with Tkinter)
- Python 3.10 or newer recommended
- Tkinter (included with standard Windows Python installation)
- Matplotlib is optional; install it to display the analytics chart.

## Run on Windows

1. Extract the ZIP file.
2. Open the extracted `SUAMS` folder in Visual Studio Code.
3. Open Terminal in that folder.
4. Run:

```bash
python -m pip install -r requirements.txt
python main.py
```

If you do not want the optional chart, you can run `python main.py` without installing Matplotlib.

## Demo login credentials

| Role | Username | Password |
|---|---|---|
| Student | `student` | `1234` |
| Teacher | `teacher` | `1234` |
| Administrator | `admin` | `1234` |
| Examination Controller | `exam` | `1234` |

The student demo account uses student ID `S-1001`.

## Run tests

```bash
python -m unittest -v
```

The test suite covers course registration, GPA/grade calculation, the 18-credit limit, semester enrollment integration, examination-form eligibility, black-box cases, and result-processing decisions.

## Software Engineering concepts

### Agile / Scrum

The work can be divided into short iterations: (1) login and role navigation, (2) admission and registration, (3) examination and routine, (4) results and advising, and (5) testing and release. A small task list can act as the product backlog; each iteration ends with a working demonstration.

### Observer Design Pattern

`NotificationService` in `core.py` stores observer callbacks. A notification page subscribes to the service. When the administrator publishes a notice, the service adds it to the notification list and notifies each registered observer. This is a simple implementation of the Observer pattern.

### Modular Programming

The application separates login, dashboard, admission, course registration, semester enrollment, examination, result processing, advising, notifications, analytics, and demo data into separate Python files. Shared business rules are in `core.py`.

### Software Quality Assurance (SQA)

- Input validation: required fields, numeric marks, mark ranges, duplicate courses, and credit limits are checked.
- Error handling: invalid actions show clear error messages.
- Code review: review each feature branch before merging.
- Coding standards: descriptive names, small functions, and consistent formatting.
- Testing: run the unit and integration test suite before release.

### Testing notes

- Unit tests check individual business rules such as grade calculation and course registration.
- Integration tests check course registration with semester enrollment and examination eligibility.
- Black-box tests check expected outcomes for a 19-credit selection and a valid exam form.
- White-box testing: `calculate_result()` has multiple decision points for required fields, mark ranges, and pass/fail status. Basis-path testing identifies independent paths through these decisions and creates test inputs to exercise each path.

## Git and GitHub workflow

Use `main` for the stable version. Develop each module on a separate feature branch, open a Pull Request, review the code, merge approved work, and tag a release.

```bash
git init
git add .
git commit -m "Initial SUAMS project"
git branch -M main
git remote add origin https://github.com/USERNAME/SUAMS.git
git push -u origin main

git checkout -b feature/course-registration
# make changes
git add .
git commit -m "Add course registration"
git push -u origin feature/course-registration
# Open a Pull Request on GitHub, review, then merge into main.

git checkout main
git pull origin main
git tag -a v1.0.0 -m "SUAMS version 1.0.0"
git push origin v1.0.0
```

Replace `USERNAME` with your GitHub username.

## Development tools

- **Visual Studio Code:** edit Python files, use the integrated terminal, run the application, and debug errors.
- **GitHub:** store source code, track changes, collaborate through branches and Pull Requests, review code, and publish release tags.

## Project structure

```text
SUAMS/
├── main.py
├── login.py
├── dashboard.py
├── base_page.py
├── core.py
├── admission.py
├── course_registration.py
├── semester_enrollment.py
├── examination.py
├── routine_generator.py
├── result_processing.py
├── advising.py
├── notifications.py
├── analytics.py
├── demo_data.py
├── test_suams.py
├── requirements.txt
└── README.md
```

## Scope and classroom-demo notes

This is an educational prototype, not a production university system. Authentication is demonstration-only, data is held in memory, and the routine generator uses a simple sequential schedule. The routine assigns a different room to each course and does not attempt advanced timetable optimization. Use fictional data only.
