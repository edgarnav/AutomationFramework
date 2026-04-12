from sqlalchemy.engine import make_url
from sqlalchemy import create_engine, text
import os


def perform_step_db(config_db, var_manager):

    query_final = config_db.get("query")
    expected = config_db.get("expected", {})
    db_url_key = config_db.get("db_url_env")
    save_as = config_db.get("save_as", {})

    db_url_env = os.environ.get(db_url_key)
    db_url = make_url(db_url_env)
    engine = create_engine(db_url)

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query_final))
            row = result.mappings().first()

            if not row:
                return False, "The query did not generate any records"

            errors = []
            for column, expected_value in expected.items():
                real_value = row.get(column)
                if str(real_value) != str(expected_value):
                    errors.append(f"Column '{column}' expected '{expected_value}', but real '{real_value}'")

            for name_variable, value in save_as.items():
                var_manager.set_variable(name_variable, value)

            if errors:
                return False, f"Errors in BD: {'; '.join(errors)}"

            return True, dict(row)

    except Exception as e:
        return False, f"Connectivity errors BD: {str(e)}"
