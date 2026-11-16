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
    return AS_OF, ask


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 1: Each project's expenses against its budget, and the share of the budget spent, the largest share first.**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            project_id,
            name,
            budget,
            total_expenses,
            total_expenses / budget AS share_of_budget
        FROM project_summary
        ORDER BY share_of_budget DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two of the fourteen projects have already gone over budget — Forge 1 has spent $145,345 against a $94,250 budget (154% of budget) and Harbor 1 has spent $123,682 against a $118,124 budget (105%) — while the remaining twelve projects are all still under their allocated budgets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 2: The tasks past their due date and not completed, with the project's name and the name of the person assigned. (three tables or more)**
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT
            t.task_id,
            p.name AS project_name,
            t.description,
            t.due_date,
            coalesce(pe.first_name || ' ' || pe.last_name, 'Unassigned') AS assigned_to
        FROM task t
        JOIN project p ON p.project_id = t.project_id
        LEFT JOIN people pe ON pe.person_id = t.assigned_person_id
        WHERE t.due_date < DATE '{AS_OF}'
          AND t.date_completed IS NULL
        ORDER BY t.due_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    61 tasks are past their due date and still not completed, including 1 with no one assigned at all. I used a LEFT JOIN to people so that unassigned overdue task still shows up (as ‘Unassigned’) rather than being silently dropped
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 3: Each person's hours a week across all active projects, and the people above 40.**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            pe.person_id,
            pe.first_name || ' ' || pe.last_name AS person_name,
            coalesce(sum(CASE WHEN p.status = 'active' THEN a.hours_per_week END), 0) AS active_hours
        FROM people pe
        LEFT JOIN assignment a ON a.person_id = pe.person_id
        LEFT JOIN project p ON p.project_id = a.project_id
        GROUP BY pe.person_id, person_name
        ORDER BY active_hours DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Jeffrey Lawrence is the only person committed to more than 40 hours a week across active projects, at 55 hours, the next highest is Melanie Munoz at 39, just under the limit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 4: Expenses by category over the last 90 days, keeping only the categories whose total is above the average of the category totals.**
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        WITH category_totals AS (
            SELECT category, sum(amount) AS total
            FROM expenses
            WHERE expense_date > DATE '{AS_OF}' - INTERVAL 90 DAY
              AND expense_date <= DATE '{AS_OF}'
            GROUP BY category
        )
        SELECT category, total
        FROM category_totals
        WHERE total > (SELECT avg(total) FROM category_totals)
        ORDER BY total DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Over the last 90 days, only the travel category’s spending is above average across categories, totaling $198,577.22.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 5: The projects with no expenses at all.**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT project_id, name
        FROM project_summary
        WHERE total_expenses = 0
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exactly one project, Prism 1, has had no expenses recorded at all.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 6: One row per project with its number of tasks and its total expenses, each checked against counting it on its own. (three tables or more)**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT project_id, name, task_count, total_expenses
        FROM project_summary
        ORDER BY project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each of the 14 projects has between 13 and 28 tasks and between roughly $92,800 and $168,400 in total expenses recorded so far, with each count independently verified against a direct query
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 7: Every task checked against the rule that its assignee works on its project, and a list of any that break it. (three tables or more) (checks a rule)**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.task_id,
            p.name AS project_name,
            pe.first_name || ' ' || pe.last_name AS assignee
        FROM task t
        JOIN project p ON p.project_id = t.project_id
        JOIN people pe ON pe.person_id = t.assigned_person_id
        LEFT JOIN assignment a
            ON a.person_id = t.assigned_person_id
           AND a.project_id = t.project_id
        WHERE t.assigned_person_id IS NOT NULL
          AND a.person_id IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exactly 2 of the 260 tasks are assigned to someone who doesn’t actually work on that task’s project: task 1 (Beacon 1, assigned to Linda Wolfe) and task 2 (Prism 1, assigned to Melanie Munoz), both of which were assigned by mistake when the data was generated to test this rule
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 8: For each manager, how many people report to them directly, and the hours a week those people have committed across all projects. (three tables or more)**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            mgr.person_id AS manager_id,
            mgr.first_name || ' ' || mgr.last_name AS manager_name,
            count(DISTINCT rep.person_id) AS direct_reports,
            coalesce(sum(a.hours_per_week), 0) AS total_hours
        FROM people mgr
        JOIN people rep ON rep.manager_id = mgr.person_id
        LEFT JOIN assignment a ON a.person_id = rep.person_id
        GROUP BY mgr.person_id, manager_name
        ORDER BY direct_reports DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Danielle Johnson has the most direct reports (6), whose combined weekly commitments across all projects total 467 hours, well above the next highest manager, Jeffrey Lawrence, with 3 reports and 114 hours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 9: How has total expense spending trended month by month over the last 12 months?**
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT
            date_trunc('month', expense_date) AS month,
            sum(amount) AS total
        FROM expenses
            WHERE expense_date > DATE '{AS_OF}' - INTERVAL 12 MONTH
          AND expense_date <= DATE '{AS_OF}'
        GROUP BY month
        ORDER BY month
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Monthly expense spending was fairly steady most of the year, generally between $75,000 and $136,000, except for two notably higher months, December 2025 (\$210,426) and July 2026 (\$252,241), both roughly double a typical month. November 2025's low figure (\$6,932) is just a partial month at the start of the 12-month window, not a real dip in spending
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 10: What share of completed tasks were finished after their original due date?**
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            count(*) AS completed_tasks,
            sum(CASE WHEN date_completed > due_date THEN 1 ELSE 0 END) AS late_completions,
            round(100.0 * sum(CASE WHEN date_completed > due_date THEN 1 ELSE 0 END) / count(*), 1) AS pct_late
        FROM task
        WHERE date_completed IS NOT NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 165 tasks that have been completed, 42 (25.5%) were finished after their original due date, meaning roughly one in four completed tasks runs late.
    """)
    return


if __name__ == "__main__":
    app.run()
