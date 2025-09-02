# Scalable FastAPI Application Template

A clean and modular FastAPI project template designed to grow with multiple endpoints, including authentication, order management, and database integration. This project is structured to make adding new routes, models, and features simple and maintainable.

## Features

- Modular route organization (`auth`, `orders`, etc.)
- Ready-to-use FastAPI application setup
- Database integration with SQLAlchemy and Alembic
- Automatic migrations support
- Easy to extend with new endpoints and models
- Async route support
- Clean and professional code structure

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install: 
    fastapi
    uvicorn
    python-jose[cryptography]
    python-dotenv
    python-multipart
    sqlalchemy alembic sqlalchemy-utils
```
4. Set up the database and run migrations:
```
alembic revision --autogenerate -m "Initial Migration"
alembic upgrade head

```

5. Running the Application:
```
uvicorn main:app --reload
```
5. Project Structure:
```
project/
├── main.py             # App initialization and router inclusion
├── auth_routes.py      # Authentication endpoints
├── order_routes.py     # Order endpoints
├── models.py           # SQLAlchemy models
├── alembic.ini         # Alembic configuration
├── alembic/            # Alembic migrations folder
├── banco.db            # SQLite database file
├── README.md
└── requirements.txt    # Optional: to list dependencies


```
