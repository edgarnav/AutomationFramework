from sqlalchemy.engine import make_url
from sqlalchemy import create_engine, text
import os


def perform_step_db(config_db, var_manager):

    query_final = config_db.get("db_query")
    expected = config_db.get("db_expected_result")
    db_url_key = config_db.get("db_url_key")
    save_as = config_db.get("db_result_variable")

    db_url_env = os.environ.get(db_url_key)
    db_url = make_url(db_url_env)
    engine = create_engine(db_url)

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query_final))
            row = result.mappings().first()

            if not row:
                return False, "The query did not generate any records"

            if expected is not None and expected not in str(row):
                return False, f"Expected value '{expected}', but real '{str(row)}'"

            else:
                for column, value in row.items():
                    real_value = row.get(column)
                    var_manager.set_variable(save_as, real_value)

            return True, row

    except Exception as e:
        return False, f"Connectivity errors BD: {str(e)}"
