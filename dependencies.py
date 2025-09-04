from models import db
from sqlalchemy.orm import sessionmaker

def get_section():
    """
    Dependency that provides a database session for request handling.
    - Ensures each request gets its own session.
    - Closes the session automatically after the request is completed.
    """
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        # Guarantee the session is closed, even if an exception occurs
        session.close()
