# dagster_project/definitions.py
from dagster import Definitions, EnvVar
from dagster_project.pipelines.assets import (
    raw_passengers,
    cleaned_passengers,
    survival_by_class,
)
from dagster_project.pipelines.resources import SupabasePostgresResource

defs = Definitions(
    assets=[raw_passengers, cleaned_passengers, survival_by_class],
    resources={
        "supabase": SupabasePostgresResource(
            host=EnvVar("SUPABASE_DB_HOST"),
            port=EnvVar("SUPABASE_DB_PORT").int_value(),
            user=EnvVar("SUPABASE_DB_USER"),
            password=EnvVar("SUPABASE_DB_PASSWORD"),
            database=EnvVar("SUPABASE_DB_NAME"),
        )
    },
)