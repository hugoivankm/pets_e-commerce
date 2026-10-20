from sqlalchemy.engine import make_url


def test_database_config(test_database_url: str) -> None:
    parsed_url = make_url(test_database_url)
    assert parsed_url.drivername == "postgresql+psycopg"
    assert parsed_url.database == "pets-e-commerce-test"
