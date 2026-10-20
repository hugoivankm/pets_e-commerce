from sqlalchemy import text
from sqlalchemy.engine import Engine


def test_database_connection(test_engine: Engine) -> None:
    with test_engine.connect() as connection:
        result = connection.scalar(text("SELECT current_database()"))
        assert result == "pets-e-commerce-test"