import os
from typing import Any

from dotenv import load_dotenv
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modules.products.routes.product_routes import product_bp


def create_app(config: dict[str, Any] | None = None) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(DATABASE_URL=os.environ.get("DATABASE_URL"))
    if config is not None:
        app.config.update(config)

    database_url = app.config["DATABASE_URL"]
    if not database_url:
        raise RuntimeError("Set DATABASE_URL before starting the application")

    engine = create_engine(database_url, pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app.extensions["db_engine"] = engine
    app.extensions["db_session_factory"] = session_factory

    app.register_blueprint(product_bp, url_prefix="/products")

    @app.get("/liveness")
    def liveness():
        return {"status": "ok"}

    @app.before_request
    def create_db_session() -> None:
        g.db_session = session_factory()

    @app.teardown_request
    def close_db_session(exception: BaseException | None = None) -> None:
        session = g.pop("db_session", None)
        if session is not None:
            session.close()

    return app
