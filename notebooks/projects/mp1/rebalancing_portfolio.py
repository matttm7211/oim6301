# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The question I will be working on is question c) Rebalancing a Portfolio. Rebalancing a portfolio is important because it helps someone keep their desired allocation of stocks based off their risk preference. Rebalancing a portfolio is important because market trends change often and based on the risk that someone is willing to make, they made need to rebalance the allocations of each stock percentage in order to stay at the risk level they desire. If rebalancing isn't done, then over time someone might end up with a portfolio that has way more risk then they are willing to take, or not enough risk for them to reach their financial goals. This project will help them make the decision on when to rebalance their portfolio based on how far the current allocation of their portfolio has strayed from their target allocation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first thing I would do would be to add up all the current shares in the portfolio and then divide them by the portion of each stock to see how close they fall to the current allocation. My loop would carry for every stock in the portfolio, add up the current shares of every stock to an empty list, then calculate the percentage of each stock by dividing the current shares by the total shares. By doing so, I can check how close the current allocation falls to the target allocation. I would then take the current allocation and subract it from the target allocation by indexing the target allocation dictionary's keys values. This would then give me the difference in allocation, where I would then determin 1. If it needs to be changed based on a metric I come up with (e.g. If I want each allocation to be within a certain percentage like +/- 2% for example) 2. I would determin if the stock is over or under weight and then change the allocation by either buying or selling the stock and then substracting or adding the cost or profit to the origional cash value. I would then repeat this process for each stock and their allocation untill all the allocations are within target range, but also making sure that we have enough cash left to purchase more stock if need be. Once all the allocation are within range I would probably make a new list of which trades to buy/sell in order to satisfy the allocation to send to a broker to do the trades.

    How I would check if the numbers agree is by comparing the total porfolio value after all the trades are made, to the origional value of the portfolio without the trades because the value should remain the same since the value of the portfolio should not change but rather just the allocation percentages should change. If the values of each porfolio matches, I would know that the reallocation worked.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


app._unparsable_cell(
    """
    ### ----------------- Creating Functions ----------------- ###


    def portfolio_value(portfolio): 
        \"\"\"
        This function takes a portfolio as an input and returns the total value of that portfolio including cash
        portfolio_value(holdings) -> will give you the total value of all the stocks in the portfolio including cash
        \"\"\"
        total = 0
        for stock in portfolio:
            symbol, quantity, price = stock
            total += quantity * price
        total += cash
        return f'The porfolio is worth ${total:,.2f}.'


    def stock_value(name):
        \"\"\" 
        This function takes an stock as an input and returns its value
        stock_value('stock name') -> will give you the value of what all the stock is worth
        \"\"\"
        for stock in holdings:
            symbol, quantity, price = stock
            if symbol == name:
                return f'{symbol} is currently worth ${quantity*price:,.2f}.'
        return f'{name} not found in portfolio.'


    def current_weights(portfolio):
        \"\"\"
        This function checks the portfolio you input to see what the current weights are of each stock not including cash
        \"\"\"
        total = 0
        for stock in portfolio:
            symbol, quantity, price = stock
            total += quantity * price

        for stock in portfolio:
            symbol, quantity, price = stock
            weight = (quantity * price) / total
            print(f'{symbol} current weight: {weight:.2%}')


    def target_allocation(portfolio):
        \"\"\"
        this function creates a dictionary of the porfolio you input and returns 1. the dollar amount of the target allocation and 2. the amount of shares to reach that allocation
        \"\"\"
        total = 0
        for stock in portfolio:
            symbol, quantity, price = stock
            total += quantity * price
        
        target_allocation = {}
        for stock in portfolio:
            symbol, quantity, price = stock
            target_dollars = target_weights[symbol] * total
            target_shares = target_dollars // price
            target_allocation[symbol] = (target_dollars, target_shares)

        return target_allocation


    def trades(portfolio):


    #current_weights(holdings)
    #target_allocation(holdings)
    #stock_value('AAPL')
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
