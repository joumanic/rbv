
# Radio Buena Vida Project

This project is a web application built with Django (backend) and React (frontend), with PostgreSQL as the database. It also integrates with Dropbox for image storage.

## Table of Contents

- Prerequisites
- Setup
- Running the Application
- Testing
- Deployment
- Contributing
- License

## Prerequisites

Before setting up the project, ensure you have the following installed on your local machine:

- Python 3.11 or higher
- Node.js and npm (for frontend development)
- PostgreSQL (database)

## Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/radio-buena-vida.git
cd radio-buena-vida
```

### 2. Set Up the Backend

#### 2.1. Create a Virtual Environment

```
python -m venv venv
```

#### 2.2. Activate the Virtual Environment

- On Windows:
  ```
  venv\Scripts\activate
  ```

- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

#### 2.3. Install Dependencies

```
pip install -r requirements.txt
```

#### 2.4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```
DJANGO_SECRET_KEY=your_django_secret_key
DEBUG=True
DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
```

Replace `your_django_secret_key` and `your_dropbox_access_token` with your actual values.

#### 2.5. Apply Database Migrations

```
python manage.py migrate
```

#### 2.6. Create a Superuser

```
python manage.py createsuperuser
```

### 3. Set Up the Frontend

#### 3.1. Navigate to the Frontend Directory

```
cd frontend
```

#### 3.2. Install Frontend Dependencies

```
npm install
```

### 4. Running the Application

#### 4.1. Start the Backend Server

```
python manage.py runserver
```

#### 4.2. Start the Frontend Development Server

In a new terminal window (make sure the virtual environment is activated):

```
cd frontend
npm start
```

### 5. Testing

To run tests for the Django backend:

```
python manage.py test
```

### 6. Deployment

For deployment, we use Render for the backend and Vercel for the frontend.

#### 6.1. Backend Deployment on Render

1. Push your code to GitHub.
2. Log in to [Render](https://render.com).
3. Create a new web service and connect it to your GitHub repository.
4. Set the environment variables in Render:
   - `DJANGO_SECRET_KEY`
   - `DROPBOX_ACCESS_TOKEN`
5. Configure the build and start commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `daphne -b 0.0.0.0:8000 radio_buena_vida.asgi:application`

#### 6.2. Frontend Deployment on Vercel

1. Push your frontend code to GitHub.
2. Log in to [Vercel](https://vercel.com).
3. Create a new project and import your GitHub repository.
4. Configure the build and output settings:
   - **Build Command**: `npm run build`
   - **Output Directory**: `frontend/build`

### 7. Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your code follows the project's style guidelines and includes appropriate tests.

### 8. License

This project is licensed under the MIT License.
