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
    **1. Getting started - The question**
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
    **2. My plan**
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
    **3. Inputs**
    """)
    return


@app.cell
def _():
    from datetime import date, timedelta
    import requests

    days = 7

    def get_date_range(days):
        today = date.today()
        from_date = today - timedelta(days=days - 1)
        return from_date.isoformat(), today.isoformat()


    def get_orders(from_date_str, to_date_str):
        response = requests.get(
            "https://oim.zhili.dev/shop/orders",
            params={"from_date": from_date_str, "to_date": to_date_str},
        )
        return response.json()

    def get_all_orders(from_date_str, to_date_str):
        orders = []
        page = 1
        more_pages = True

        while more_pages:
            page_response = requests.get(
                "https://oim.zhili.dev/shop/orders",
                params={"from_date": from_date_str, "to_date": to_date_str, "page": page},
            )
            page_data = page_response.json()

            for order in page_data["items"]:
                orders.append(order)

            more_pages = page_data["pagination"]["has_next"]
            page += 1

        return orders


    def get_order_lines(orders):
        lines = []
        for order in orders:
            line_response = requests.get(f"https://oim.zhili.dev/shop/orders/{order['order_id']}")
            line_data = line_response.json()
            for line in line_data["lines"]:
                lines.append(line)
        return lines


    def total_revenue(orders):
        total = 0
        for order in orders:
            total += order["order_total_dollars"]
        return total


    def revenue_by_country(orders):
        by_country = {}
        for order in orders:
            country = order["ship_country"]
            by_country[country] = by_country.get(country, 0) + order["order_total_dollars"]
        return by_country


    def get_unshipped(orders):
        unshipped = []
        for order in orders:
            if order["shipped_date"] is None:
                unshipped.append(order)
        return unshipped


    def get_top_country(by_country):
        top_country = None
        top_amount = None
        for country, amount in by_country.items():
            if top_amount is None or amount > top_amount:
                top_country = country
                top_amount = amount
        return top_country

    return (
        get_all_orders,
        get_date_range,
        get_order_lines,
        get_orders,
        get_top_country,
        get_unshipped,
        revenue_by_country,
        total_revenue,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4. The Work**
    """)
    return


@app.cell
def _(
    get_all_orders,
    get_date_range,
    get_order_lines,
    get_orders,
    get_top_country,
    get_unshipped,
    revenue_by_country,
    total_revenue,
):
    from_date_str, to_date_str = get_date_range(7)
    data = get_orders(from_date_str, to_date_str)
    data
    all_orders = get_all_orders(from_date_str, to_date_str)
    all_lines = get_order_lines(all_orders)
    number_of_orders = len(all_orders)
    revenue = total_revenue(all_orders)
    country_totals = revenue_by_country(all_orders)
    unshipped_orders = get_unshipped(all_orders)
    top_country = get_top_country(country_totals)
    return (
        all_orders,
        country_totals,
        data,
        number_of_orders,
        revenue,
        top_country,
        unshipped_orders,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5. The Answer**
    """)
    return


@app.cell
def _(
    country_totals,
    number_of_orders,
    revenue,
    top_country,
    unshipped_orders,
):
    print(f"{'Country':<15}{'Revenue':>12}")
    for x, y in country_totals.items():
        print(f"{x:<15}${y:>10,.2f}")

    print()
    print(f"This week there were {number_of_orders} orders worth ${revenue:,.2f}, with {len(unshipped_orders)} not yet shipped. {top_country} led all countries with ${country_totals[top_country]:,.2f} in revenue.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6. How do I know these numbers are right.**
    """)
    return


@app.cell
def _(all_orders, data):
    reported_total = data["pagination"]["total"]
    collected_total = len(all_orders)

    print(f"The API reports {reported_total} orders; this notebook collected {collected_total}.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7. Working with the agent**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One of the errors I noticed is that the get_top_country function that AI helped me write start with None, so if the every country's revenue is 0 or negative becuase of refunds, the function could raise an error when called. I fixed it by also using a top amount of None, instead of 0, so that if the function gets called and all countries have non-positive revenue, it will still correctly return the country with the highest (least negative) value instead of skipping it due to a default of 0.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **8. Reading it back**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Function 1. get_all_orders:** What goes in is a starting date and an ending date. What comes out is a list of every order placed in that date range, pulled from the API until there are no more pages left. One change I'd like to see is if i change in the input cell days=7 to days=30 so that i can get orders for a full month instead of a week. What I expect to change is the date range used to fetch orders will expand from 7 days to 30 days, resulting in more orders being returned in the output list, since `get_all_orders` will now query the API for a full month's worth of data instead of just one week.

    **Function 2. filter_orders_by_status:** What goes in is the list of orders returned by `get_all_orders` along with a target status ("shipped", "cancelled", "pending"). What comes out is a filtered list containing only the orders that match the specified status. One change I'd like to see is if I change the status filter from "shipped" to "cancelled" so that I can review which orders were cancelled instead of which were shipped. What I expect to change is the output list will now contain only orders with a "cancelled" status, filtering out all others, since `filter_orders_by_status` will compare each order's status field against the new target value instead of the old one.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
