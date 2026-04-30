from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables and apply any missing column migrations. Call on startup."""
    from models.user import User          # noqa
    from models.scan import Scan          # noqa
    from models.post_result import PostResult  # noqa
    Base.metadata.create_all(bind=engine)
    _migrate_schema()


def _migrate_schema():
    """
    Lightweight forward-only migration: adds any columns that exist in the ORM
    models but are missing from the live database tables.

    This is safe to run on every startup — it uses ADD COLUMN IF NOT EXISTS so
    it's a no-op when columns already exist. It does NOT drop or alter existing
    columns, preserving data safety.
    """
    from sqlalchemy import text, inspect

    inspector = inspect(engine)

    # Map each table to its expected columns (name → SQLAlchemy type string)
    # Add entries here whenever a new column is added to a model.
    migrations = {
        "scans": {
            "report_hash": "VARCHAR(64)",
            "pdf_hash":    "VARCHAR(64)",
        },
    }

    with engine.connect() as conn:
        for table, columns in migrations.items():
            existing = {col["name"] for col in inspector.get_columns(table)}
            for col_name, col_type in columns.items():
                if col_name not in existing:
                    conn.execute(
                        text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col_name} {col_type}")
                    )
            conn.commit()
