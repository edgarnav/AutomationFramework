from sqlalchemy import create_engine, text


def perform_step_db(config_db, var_manager):

    conn_data = config_db.get("connection", {})

    for key in conn_data:
        conn_data[key] = var_manager.resolve_instruction(str(conn_data[key]))

    db_url = build_url(conn_data)
    if not db_url:
        return False, "DB not compatible "

    engine = create_engine(db_url)
    query_final = var_manager.resolver_instruccion(config_db["query"])
    expected = config_db.get("expected", {})

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query_final))
            row = result.mappings().first()

            if not row:
                return False, "Record not found in the database"

            errors = []
            for col, val_esp in expected.items():
                if str(row.get(col)) != str(val_esp):
                    errors.append(f"[{col}] expected {val_esp}, obtained {row.get(col)}")

            if errors:
                return False, f"Validation failed: {', '.join(errors)}"

            return True, dict(row)

    except Exception as e:
        return False, f"Connection error: {str(e)}"


def build_url(conn_data):

    db_type = conn_data.get("type", "sqlserver").lower()
    user = conn_data.get("user")
    password = conn_data.get("pass")
    host = conn_data.get("host")
    db_name = conn_data.get("db")

    if db_type == "sqlserver":
        return f"mssql+pyodbc://{user}:{password}@{host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"

    elif db_type == "postgresql":
        return f"postgresql://{user}:{password}@{host}/{db_name}"

    elif db_type == "oracle":
        return f"oracle+cx_oracle://{user}:{password}@{host}/?service_name={db_name}"

    return False
