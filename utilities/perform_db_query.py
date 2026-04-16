from sqlalchemy.engine import make_url
from sqlalchemy import create_engine, text
import os


def perform_step_db(config_db, var_manager):

    query_final = config_db.get("db_query")
    expected = config_db.get("db_expected_result")
    db_url_key = config_db.get("db_url_key")
    save_as = config_db.get("db_result_variable")

    db_url_env = os.environ.get(db_url_key)
    if not db_url_env:
        return False, f"Error: Environment variable not found: '{db_url_key}'"

    try:
        db_url = make_url(db_url_env)
        engine = create_engine(db_url)
    except Exception as e:
        return False, f"Error creating DB connection: {str(e)}"

    try:
        with engine.begin() as connection:
            result = connection.execute(text(query_final))

            if result.returns_rows:
                row = result.mappings().first()

                if not row:
                    return False, "Query did not generate any rows."

                row_str = str(dict(row))

                if expected is not None and expected not in row_str:
                    return False, f"Expected '{expected}', but obtained '{row_str}'"

                if save_as:
                    var_manager.set_variable(save_as, dict(row))

                return True, dict(row)

            else:
                affected_rows = result.rowcount
                result_message = f"Success. {affected_rows} affected rows."

                if expected is not None and expected not in str(affected_rows):
                    return False, f"Expected '{expected}' affected rows but there were '{affected_rows}'"

                if save_as:
                    var_manager.set_variable(save_as, affected_rows)

                return True, result_message

    except Exception as e:
        return False, f"Errors in query execution: {str(e)}"
