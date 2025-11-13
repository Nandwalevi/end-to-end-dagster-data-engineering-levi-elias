# dagster_project/tests/test_assets.py
# dagster_project/tests/test_assets.py
import os
import pandas as pd
import pytest
from dotenv import load_dotenv
from sqlalchemy.sql import text

from dagster_project.pipelines.resources import SupabasePostgresResource
from dagster_project.pipelines.assets import raw_passengers, cleaned_passengers


# load .env once for the test session
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../..", ".env"))


@pytest.fixture(scope="session")
def supabase():
    return SupabasePostgresResource()


def test_can_connect(supabase):
    """Smoke-test connection."""
    engine = supabase.get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as val")).scalar()
    assert result == 1


def test_assets_end_to_end(supabase):
    """Materialise and verify tables exist and are non-empty."""
    raw_passengers(supabase)
    cleaned_passengers(supabase)

    engine = supabase.get_engine()
    raw_cnt = pd.read_sql("SELECT COUNT(*) as c FROM public.raw_passengers", engine).iloc[0]["c"]
    clean_cnt = pd.read_sql("SELECT COUNT(*) as c FROM public.cleaned_passengers", engine).iloc[0]["c"]
    age_nulls = pd.read_sql(
    'SELECT COUNT(*) as c FROM public.cleaned_passengers WHERE "Age" IS NULL',
    engine
).iloc[0]["c"]


    assert raw_cnt > 0
    assert clean_cnt > 0
    assert age_nulls == 0