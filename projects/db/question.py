import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    from datetime import date

    return date, duckdb, mo


@app.cell
def _(date, duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()


    AS_OF = date(2026, 11, 14)
    return (ask,)


@app.cell
def _(ask):
    task_counts = ask("SELECT project_id, count(*) AS n_tasks FROM task GROUP BY project_id")
    task_counts
    return (task_counts,)


@app.cell
def _(ask):
    expense_counts = ask("SELECT project_id, count(*) AS n_expenses FROM expenses GROUP BY project_id")
    expense_counts
    return (expense_counts,)


@app.cell
def _(expense_counts, task_counts):
    merged = task_counts.join(expense_counts, on="project_id", how="full").fill_null(0)
    predicted_rows = (merged["n_tasks"] * merged["n_expenses"]).sum()
    predicted_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question:** One row per project with its number of tasks and its total expenses.

    **Prediction:** I expect the joins (project joined to task, joined to expenses, both on project_id, before any GROUP BY) to produce {predicted_rows} rows. This is because joining a project to both its tasks and its expenses independently pairs every task with every expense for that project — so each project contributes (its task count × its expense count) rows, not their sum. Project 14, which has zero expenses, contributes zero rows since a plain JOIN drops it when either side has no match.
    """)
    return


if __name__ == "__main__":
    app.run()
