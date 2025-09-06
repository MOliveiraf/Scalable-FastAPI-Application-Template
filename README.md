# Scalable FastAPI Application Template

A clean, modular, and production-ready **FastAPI** project template designed for scalability.  
This project provides authentication, order management, and database integration, following best practices for maintainability and growth.

---

## 🚀 Features

- ✅ Modular route organization (`auth`, `orders`, etc.)
- ✅ Secure user authentication with **bcrypt** password hashing
- ✅ Database integration with **SQLAlchemy** and **Alembic**
- ✅ Automatic database migrations
- ✅ Easy to extend with new endpoints and models
- ✅ Async route support for performance
- ✅ Clean and professional code structure

---

## 🔧 Installation

1. **Clone the repository**:
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
    fastapi → The main web framework. Lets you build high-performance APIs quickly with Python type hints and automatic docs (Swagger UI).

    uvicorn → An ASGI server. Runs your FastAPI app and handles HTTP requests/responses efficiently.

    python-jose[cryptography] → Handles JSON Web Tokens (JWT). Used for securely encoding/decoding authentication tokens.

    python-dotenv → Loads environment variables from a .env file into your project (e.g., database URL, secret keys).

    python-multipart → Enables form data and file upload handling in FastAPI (e.g., sending images or forms in requests).

    sqlalchemy → The ORM (Object-Relational Mapper) for database interactions. Lets you use Python classes instead of writing raw SQL.

    alembic → Migration tool for SQLAlchemy. Helps version and update your database schema safely over time.

    sqlalchemy-utils → Extra tools for SQLAlchemy (like advanced field types, validators, helpers).

    bcrypt → Password hashing library. Ensures user passwords are securely stored by hashing + salting.
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
├── auth_routes.py      # Authentication endpoints (register, login, hashing)
├── order_routes.py     # Order endpoints (create and manage orders)
├── models.py           # SQLAlchemy models (User, Order, OrderItem)
├── schemas.py          # Pydantic schemas for validation
├── dependencies.py     # Dependency injections (DB session, etc.)
├── alembic.ini         # Alembic configuration
├── alembic/            # Alembic migrations folder
├── banco.db            # SQLite database file (development only)
├── README.md           # Project documentation
└── requirements.txt    # Dependencies list
```

6. 🔑 Authentication & Security

* Passwords are never stored in plain text.
* User passwords are hashed using bcrypt with a random salt and configurable cost factor.
* During login, bcrypt re-hashes the provided password and compares it with the stored hash.
* This ensures strong protection against brute-force and rainbow table attacks.

Example workflow:

I-Register → password is hashed before being stored in the database.

II-Login → password is verified against the stored hash.

III-Access token (Bearer) is generated for session handling.

7. 🛠️ Future Improvements
* JWT authentication with refresh tokens
* Role-based access control (admin/user)
* Testing with pytest
* Docker support for containerized deployments
* CI/CD integration