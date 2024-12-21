# Backend for Social Media App Using FastAPI

This API includes four main routes, each designed to handle specific functionalities:

### 1. **Post Route**
   - Responsible for:
     - Creating posts
     - Deleting posts
     - Updating posts
     - Viewing posts

### 2. **User Route**
   - Focuses on:
     - Creating new users
     - Retrieving user details by ID

### 3. **Authentication Route**
   - Handles:
     - User login and authentication

### 4. **Vote Route**
   - Implements a voting system:
     - Supports upvotes and "back" votes
     - Does not include logic for downvotes


---

## How to Run Locally

1. Clone the repo, create a virtual environment, and install required dependencies.

```bash
git clone https://github.com/whoIsOneZero/api_dev_course.git
cd api_dev_course
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # MacOS/Linux
pip install -r requirements.txt

```
2. Create a PostgreSQL Database
Set up a database in PostgreSQL.  
Once the database is created, add a .env file to the project directory and include the following environment variables:

```bash
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = your_database_password
DATABASE_NAME = your_database_name
DATABASE_USERNAME = your_database_username
SECRET_KEY = your_secret_key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

- To generate a secret key, you could use any of these commands:
```bash
openssl rand -base64 32 # Linux
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Run the app
```bash
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs # open in a browser

```
