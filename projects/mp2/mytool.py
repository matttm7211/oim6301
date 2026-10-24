import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Getting started - The question**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The question I will be working with is question B - The Shop's Week. Here I will be returning one report: the number of orders, the revenue, revenue by country, the five products that sold the most units, and the orders not shipped yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **My plan**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My plan, or my thought process, before writing any code would be to first check the api and the doc and look at how it is structured. I would try and aquire the first page of orders and then add them to a list for all the other pages so that I can collect every order. I would then try and pull every line item from each depending on what I'm looking for and then compute the total for each line like product, product quantity, and the prices. Once I've aquired all the information in a organized manner I would then return one report that gives the number of orders, the revenue, revenue by country, the five products that sold the most units, and the orders not shipped yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The Main Task**
    """)
    return


if __name__ == "__main__":
    app.run()
