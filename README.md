# Scalable FastAPI Application Template

A clean and modular FastAPI project template designed to grow with multiple endpoints, including authentication and order management. This project is structured to make adding new routes and features simple and maintainable.

## Features

- Modular route organization (`auth`, `orders`, etc.)
- Ready-to-use FastAPI application setup
- Easy to extend with new endpoints
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
fastapi
uvicorn
python-jose[cryptography]
python-dotenv
python-multipart


```
4. Running the Application:
```
uvicorn main:app --reload
```
5. Project Structure:
```
project/
├── main.py             # App initialization and router inclusion
├── auth_routes.py      # Authentication endpoints
├── order_routes.py     # Order endpoints
├── README.md
└── requirements.txt    # Optional: to list dependencies

```
