# RIS Project

This is a Radiology Information System (RIS) project built with Django, designed to manage patient records, including their X-ray images and related 

## Setup

### Prerequisites

- Python 3.x
- Django 3.x

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/RIS_project.git
   cd RIS_project

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    
3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    
4. **Apply migrations:**

    ```bash
    python manage.py migrate

5. **Run the development server:**

    ```bash
    python manage.py runserver

6. **Access the application:**
        Open your web browser and navigate to http://127.0.0.1:8000/.

## Usage
- Home Page: Access the main dashboard and navigate through the application.
- Add New Patient: Add new patient records including their personal details and prescribed X-ray.
- Search Patient: Search for patient records using various criteria.
- User Authentication: Register, login, and manage user sessions.

# Project Details
## Models
- Patient: Stores patient information such as name, age, address, email, gender, prescribing doctor, and prescribed X-ray.
## Views
- Home: Renders the home page.
- Add Patient: Handles the form for adding new patient records.
- Search: Provides functionality to search for patient records.
- Authentication: Manages user registration and login.

## Templates
- add_new_patient.html: Form for adding new patient records.
- home.html: Main dashboard.
- login.html: User login page.
- register.html: User registration page.
- search_for.html: Search functionality for patient records.

