"""Schema-level tests for user domain models; no database connection is used."""

from src.modules.users import PaymentMethod, User


def test_user_model_has_required_identity_and_access_columns() -> None:
    table = User.__table__

    assert table.c.name.nullable is False
    assert table.c.email.nullable is False
    assert table.c.email.unique is True
    assert table.c.role.nullable is False
    assert table.c.is_active.nullable is False


def test_payment_method_belongs_to_a_user() -> None:
    user_id = PaymentMethod.__table__.c.user_id

    assert user_id.nullable is False
    assert {foreign_key.target_fullname for foreign_key in user_id.foreign_keys} == {
        "users.id"
    }


def test_user_instance_can_be_created_without_a_database_session() -> None:
    user = User(name="Ari Example", email="ari@example.test")

    assert user.name == "Ari Example"
    assert user.email == "ari@example.test"
