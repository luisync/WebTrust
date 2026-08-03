from app.db.session import get_db

def test_get_db():
    # Databse generator.
    db = get_db()
    session = next(db)

    assert session is not None

    # Close the connection.
    db.close()