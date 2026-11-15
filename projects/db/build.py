import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (database,)


@app.cell
def _(database, duckdb):
    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE people (
                person_id   INTEGER PRIMARY KEY,
                first_name  VARCHAR NOT NULL,
                last_name   VARCHAR NOT NULL,
                work_email  VARCHAR NOT NULL,
                title       VARCHAR NOT NULL,
                start_date  DATE NOT NULL,
                manager_id  INTEGER REFERENCES people(person_id)
            )
        """)

        _con.execute("""
            CREATE TABLE project (
                project_id   INTEGER PRIMARY KEY,
                name         VARCHAR NOT NULL,
                client_name  VARCHAR,
                category     VARCHAR NOT NULL
                             CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
                budget       DOUBLE NOT NULL 
                             CHECK (budget> 0),
                start_date   DATE NOT NULL,
                status       VARCHAR NOT NULL
                             CHECK (status IN ('planned', 'active', 'paused', 'done'))
            )
        """)

        _con.execute("""
            CREATE TABLE task (
                task_id             INTEGER PRIMARY KEY,
                project_id          INTEGER NOT NULL REFERENCES project(project_id),
                description         VARCHAR NOT NULL,
                date_created        DATE NOT NULL,
                assigned_person_id  INTEGER REFERENCES people(person_id),
                due_date            DATE NOT NULL,
                date_completed      DATE,
                CHECK (date_completed IS NULL OR date_completed >= date_created)
            )
        """)

        _con.execute("""
            CREATE TABLE expenses (
                expense_id    INTEGER PRIMARY KEY,
                project_id    INTEGER NOT NULL REFERENCES project(project_id),
                expense_date  DATE NOT NULL,
                amount        DOUBLE NOT NULL 
                              CHECK (amount > 0),
                category      VARCHAR NOT NULL
                             CHECK (category IN ('GPU cloud', 'data labeling', 'Software', 'travel')),
                note          VARCHAR
            )
        """)

        _con.execute("""
            CREATE TABLE assignment (
                person_id       INTEGER NOT NULL REFERENCES people(person_id),
                project_id      INTEGER NOT NULL REFERENCES project(project_id),
                role            VARCHAR NOT NULL,
                hours_per_week  INTEGER NOT NULL 
                                CHECK (hours_per_week >= 1 AND hours_per_week <= 40),
                date_joined     DATE NOT NULL,
                PRIMARY KEY (person_id, project_id)
            )
        """)
    return


if __name__ == "__main__":
    app.run()
