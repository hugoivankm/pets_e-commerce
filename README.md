# Pets e-commerce

Set `DATABASE_URL` in `.env` to your PostgreSQL development database URL,
using the `postgresql+psycopg://` driver.

## Initialize the development database with pgAdmin

The app uses `DATABASE_URL`; integration tests use the separate
`TEST_DATABASE_URL`. Tables created in the test database are not available
in the development database.

1. In pgAdmin, connect to the PostgreSQL server specified by `DATABASE_URL`.
2. Select the development database named in that URL. If it does not exist,
   right-click **Databases → Create → Database**, create it, and make sure
   `DATABASE_URL` uses the same name. Use the application database user as
   the owner, or run the script as that user so the app can access the tables.
3. Right-click that database and open **Query Tool**.
4. Open [scripts/init_db.sql](scripts/init_db.sql) using the Query Tool's file button,
   or paste its contents into the editor.
5. Execute the complete script. It creates all 15 model tables, their indexes,
   and constraints in the `public` schema, inside one transaction. The app's
   database user must have `public` in its schema search path (the PostgreSQL
   default includes it).
6. Refresh **Schemas → public → Tables** and confirm `products` and
   `categories` appear.

Run this script once against an empty development database. It does not drop
tables or insert data, and it is not a migration for an existing schema. If
execution fails, run `ROLLBACK;`, resolve the reported error, and retry the
complete script.

After setup, `GET /products/1` returns a JSON 404 until a product with ID 1
exists. Creating a product also requires an existing category.

## Run the app

Start the development server:

```bash
uv run flask --app src.main:create_app run --debug
```

Alternatively, run `uv run python run.py` without debug mode.

Check startup with `GET http://127.0.0.1:5000/liveness`.
It returns `{"status": "ok"}`; this checks the app, not database connectivity.

Each request receives a SQLAlchemy session at `g.db_session`, which is closed
after the request. Services own commits and rollbacks. Construct the product
repository and service with that same session.

The product blueprint is registered at `/products`. `GET /products/<id>`
returns product JSON or a JSON 404 when the product does not exist. The POST
endpoint is still to be implemented. Startup does not create tables or seed data.
