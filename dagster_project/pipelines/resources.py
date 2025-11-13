# dagster_project/pipelines/resources.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # ensures .env is loaded if not already


class SupabasePostgresResource:
    """Dagster resource for connecting to Supabase PostgreSQL."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ):
        # Pull from .env if not provided directly
        self.host = host or os.getenv("SUPABASE_DB_HOST")
        self.port = port or int(os.getenv("SUPABASE_DB_PORT", 5432))
        self.user = user or os.getenv("SUPABASE_DB_USER")
        self.password = password or os.getenv("SUPABASE_DB_PASSWORD")
        self.database = database or os.getenv("SUPABASE_DB_NAME")

    def get_engine(self):
        if not all([self.host, self.user, self.password, self.database]):
            raise ValueError(
                "Missing one or more required Supabase connection parameters."
            )
        uri = (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        # 👇 Add SSL requirement for Supabase
        return create_engine(
            uri,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10, "sslmode": "require"},
        )
