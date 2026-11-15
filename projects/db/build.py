import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo, pl


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database


@app.cell
def _(database, duckdb, mo, pl):
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
                             CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
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

        data_dir = mo.notebook_dir() / "data"

        # project has no dependency on anything else, load it first
        _con.execute(f"""
            COPY project FROM '{data_dir / "project.csv"}' (HEADER, AUTO_DETECT TRUE)
        """)

        # people self-references manager_id, so load one row at a time,
        # managers before the people who report to them
        people_df = pl.read_csv(data_dir / "people.csv")
        loaded_ids: set[int] = set()
        remaining = people_df
        while remaining.height > 0:
            ready = remaining.filter(
                pl.col("manager_id").is_null() | pl.col("manager_id").is_in(list(loaded_ids))
            )
            if ready.height == 0:
                raise ValueError("people.csv has a manager cycle or a manager_id with no matching person")
            for row in ready.iter_rows(named=True):
                _con.execute(
                    """INSERT INTO people (person_id, first_name, last_name, work_email, title, start_date, manager_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [row["person_id"], row["first_name"], row["last_name"],
                     row["work_email"], row["title"], row["start_date"], row["manager_id"]],
                )
                loaded_ids.add(row["person_id"])
            remaining = remaining.filter(~pl.col("person_id").is_in(list(loaded_ids)))

        # assignment and task depend on both people and project, expenses depends on project
        _con.execute(f"""
            COPY assignment FROM '{data_dir / "assignment.csv"}' (HEADER, AUTO_DETECT TRUE)
        """)
        _con.execute(f"""
            COPY task FROM '{data_dir / "task.csv"}' (HEADER, AUTO_DETECT TRUE)
        """)
        _con.execute(f"""
            COPY expenses FROM '{data_dir / "expenses.csv"}' (HEADER, AUTO_DETECT TRUE)
        """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'people' AS tbl, count(*) AS n FROM people
        UNION ALL SELECT 'project', count(*) FROM project
        UNION ALL SELECT 'assignment', count(*) FROM assignment
        UNION ALL SELECT 'task', count(*) FROM task
        UNION ALL SELECT 'expenses', count(*) FROM expenses
    """)
    return


@app.cell
def _(mo, pl):
    import matplotlib.pyplot as plt

    task_df = pl.read_csv(mo.notebook_dir() / "data" / "task.csv", try_parse_dates=True)

    by_weekday = (
        task_df
        .with_columns(pl.col("date_created").dt.weekday().alias("weekday"))
        .group_by("weekday")
        .len()
        .sort("weekday")
    )

    fig, ax = plt.subplots()
    ax.bar(by_weekday["weekday"], by_weekday["len"])
    ax.set_xticks(range(1, 8))
    ax.set_xlabel("Day of week (1 = Monday ... 7 = Sunday)")
    ax.set_ylabel("Tasks created")
    ax.set_title("Tasks created by day of week")
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Task creation was originally flat across all seven days, including weekends, which isn’t realistic for a company doing project work. I ended up changing make_data.py so date_created is strongly biased toward weekdays, and the chart now shows the distribution of tasks created strongly favored during the week instead of on the weekends.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5. A row it refuses**
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO expenses (expense_id, project_id, expense_date, amount, category, note)
                VALUES (9999, 1, '2026-01-15', -500, 'software', 'testing a refused row')
            """)
        print("Row was accepted (this shouldn't happen)")
    except Exception as e:
        print("Database refused the row:")
        print(e)
    return


if __name__ == "__main__":
    app.run()
