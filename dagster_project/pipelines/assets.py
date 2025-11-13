# dagster_project/pipelines/assets.py
import pandas as pd
from dagster import asset
from dagster_project.pipelines.resources import SupabasePostgresResource

RAW_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"


@asset(group_name="etl")
def raw_passengers(supabase: SupabasePostgresResource) -> None:
    """Download CSV and write to public.raw_passengers."""
    df = pd.read_csv(RAW_URL)
    engine = supabase.get_engine()
    df.to_sql("raw_passengers", engine, schema="public", if_exists="replace", index=False)


@asset(group_name="etl", deps=["raw_passengers"])
def cleaned_passengers(supabase: SupabasePostgresResource) -> None:
    """Drop Age/Fare nulls → public.cleaned_passengers."""
    engine = supabase.get_engine()
    raw_df = pd.read_sql("SELECT * FROM public.raw_passengers", engine)
    cleaned_df = raw_df.dropna(subset=["Age", "Fare"])
    cleaned_df.to_sql("cleaned_passengers", engine, schema="public", if_exists="replace", index=False)


@asset(group_name="analytics", deps=["cleaned_passengers"])
def survival_by_class(supabase: SupabasePostgresResource) -> None:
    """Aggregate survival by Pclass → public.survival_by_class."""
    engine = supabase.get_engine()
    df = pd.read_sql("SELECT * FROM public.cleaned_passengers", engine)
    result = df.groupby("Pclass")["Survived"].mean().reset_index()
    result.to_sql("survival_by_class", engine, schema="public", if_exists="replace", index=False)