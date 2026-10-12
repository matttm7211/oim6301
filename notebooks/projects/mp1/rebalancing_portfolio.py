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
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings, target_weights):
    ### ----------------- Creating Functions ----------------- ###
    ## sanity check functions to double check at the end

    def portfolio_value(portfolio): 
        """
        This function takes a portfolio as an input and returns the total value of that portfolio including cash
        portfolio_value(holdings) -> will give you the total value of all the stocks in the portfolio including cash
        """
        total = 0
        for stock in portfolio:
            symbol, quantity, price = stock
            total += quantity * price
        total += cash
        return f'The porfolio is worth ${total:,.2f}.'


    def stock_value(name):
        """ 
        This function takes an stock as an input and returns its value
        stock_value('stock name') -> will give you the value of what all the stock is worth
        """
        for stock in holdings:
            symbol, quantity, price = stock
            if symbol == name:
                return f'{symbol} is currently worth ${quantity*price:,.2f}.'
        return f'{name} not found in portfolio.'


    def current_weights(portfolio):
        """
        This function checks the portfolio you input to see what the current weights are of each stock not including cash
        """
        total = 0
        for stock in portfolio:
            symbol, quantity, price = stock
            total += quantity * price

        for stock in portfolio:
            symbol, quantity, price = stock
            weight = (quantity * price) / total
            print(f'{symbol} current weight: {weight:.2%}')


    def target_allocation(portfolio):
        """
        this function creates a dictionary of the porfolio you input and returns 1. the dollar amount of the target allocation and 2. the amount of shares to reach that allocation
        """
        total = cash
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


    #portfolio_value(holdings)
    current_weights(holdings)
    target_allocation(holdings)
    #stock_value('AAPL')
    return current_weights, target_allocation


@app.cell
def _(cash, holdings, target_weights):
    """
    Calculating the total value of the portfolio including the starting cash
    """
    total_value = 0
    for symbol, shares, price in holdings:
        total_value += shares * price
    total_value += cash
    #print(total_value) #total value of the initial holdings
    #sanity check ^^






    """
    Determining the target amount of shares to have based on the target_weights provided
    """
    targets = {}
    for symbol, shares, price in holdings:
        targets[symbol] = (total_value * target_weights[symbol]) // price #assigning a target amount of shares to the dictionary key
    #print(targets) #returns the number of SHARES needed for each ticker
    #sanity check ^^






    """
    Creating a table based on holdings```
    with target shares, trade needed, resulting value, and resulting weight
    """
    table = []
    for symbol, shares, price in holdings:
        target_shares = targets[symbol]
        trade = target_shares - shares
        value_after = target_shares * price
        weight_after = value_after / total_value
        table.append((symbol, shares, target_shares, trade, value_after, weight_after))
    #print(table)
    #sanity check ^^






    """
    Determining the amound of cash left after weve made the correcting trades, pulling out trade from the table and the origional price from holdings
    """
    cash_used = sum(trade*price for (_, _, _, trade, _, _), (_, _, price) in zip(table, holdings))
    cash_left = cash - cash_used
    assert cash_left >= 0, "Not enough cash" #assert lets us make sure that cash left is still in the positive, if not it stops the program
    #print(cash, cash_used)
    #sanity check ^^






    """
    Checking deviation after the trades and if its close enough to the target_weights initially defined
    """
    for symbol, shares, target_shares, trade, value_after, weight_after in table: 
        deviation_percentage = (weight_after - target_weights[symbol]) * 100
        #print(abs(deviation_percentage)) # sanity check
        status = "Bellow" if deviation_percentage < 0 else "Above" if deviation_percentage > 0 else "On Target"
        result = "Close Enough" if abs(deviation_percentage) <= 0.5 else "Not Close Enough"
        print(f"{symbol}: {abs(deviation_percentage):.2f}pp {status} target - {result}.")


    return cash_left, table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(cash_left, table):
    ### ----------------- Creating The Table ----------------- ###

    """
    Printint the headers for the table
    """
    print(f"{'Ticker':<7}{'Now':>9}{'Target':>11}{'Trade':>7}{'ValueAfter':>12}{'WeightAfter':>14}")

    """
    Iteraring through table, defining one row of the table and then printing a line for each ticker
    """
    for row in table:
        a, b, c, d, e, f = row
        print(f'{a:<7} | {b:>6} | {c:>8} | {d:+.0f} | ${e:,.2f} | {f:.2%}')

    after_total_value = cash_left
    for row in table:
        after_total_value += row[4]

    """
    Printing the total portfolio value after the trades and the remaining cash left
    """
    print(f"\nTotal portfolio value: ${after_total_value:,.2f}, Cash left after trades: ${cash_left:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To asnswer the questions in #1, this project helps people keep track of how far their holdings have strayed from the target allocations. From the table above we can see that the portfolio has drifted quite a bit from the targets and we can now see the amount of trades needed of each stock to rebalance the portfolio, or the amount of trades needed to get them all back to around target weights. As for how close, I felt like a tolerance that was within 0.5 percentage points away from the target was acceptable. and as we see from the deviation percentages, the bigest difference we have is 0.24pp. Seeing as prices of stocks are constantly changing everyday, I like being in this range.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(current_weights, holdings, target_allocation):
    current_weights(holdings)
    target_allocation(holdings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The way I know that these numbers are correct and that they work is that if we look at the current_weights function i created at the beginning, we can see that the weights are not close to the target weights. This confirms that the portfolio is currently out of balance and needs rebalancing. Once I rebalance the portfolio and we take a look at the new weights, we can see that they all fall in accordance to the target allocations defined at the beginning of this notebook. Aditionally, if we look at the target_allocation function that i created at the beginning, we can see that the number of shares needed for each stock to be balanced, matched up with the number of shares traded (in the table) in order to balance the portfolio. E.G, AAPL was at 100, the target function said 139, and in the table the target also said 139 and shows a trade of +39.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell
def _():
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
