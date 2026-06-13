"""Decisions & Calculations Worksheet — write an algorithm, draw a flowchart.

Every problem here is a DRAW problem: the student is given a plain-English
statement and must write the algorithm and draw its flowchart. As with the
other flowchart worksheets, each algorithm is authored once and the flowchart
(shown on the answer key) is derived from the same source, so the answer can
never disagree with the trace.

  DRAW(algo, description="...")  given the statement -> draw the flowchart
"""

from gens.flowgen import Algorithm, read, assign, out, If, DRAW

TITLE = "Flowcharts II — Decisions and Calculations"

income_tax = Algorithm("Income tax", [
    read("income"),
    If("income <= 250000",
       [assign("tax", "0")],
       [If("income <= 500000",
           [assign("tax", "(income - 250000) * 0.05")],
           [If("income <= 1000000",
               [assign("tax", "250000 * 0.05 + (income - 500000) * 0.20")],
               [assign("tax", "250000 * 0.05 + 500000 * 0.20 "
                              "+ (income - 1000000) * 0.30")])])]),
    out("tax"),
])

shop_discount = Algorithm("Shop discount", [
    read("amount"),
    If("amount < 1000",
       [assign("payable", "amount")],
       [If("amount < 5000",
           [assign("payable", "amount * 0.95")],
           [If("amount < 10000",
               [assign("payable", "amount * 0.90")],
               [assign("payable", "amount * 0.85")])])]),
    out("payable"),
])

electricity = Algorithm("Electricity bill", [
    read("units"),
    If("units <= 100",
       [assign("bill", "0")],
       [If("units <= 200",
           [assign("bill", "(units - 100) * 2")],
           [assign("bill", "100 * 2 + (units - 200) * 5")])]),
    out("bill"),
])

PROBLEMS = [
    DRAW(electricity,
         description="Ask the user for the number of electricity units consumed "
                     "in a month and print the bill. The first 100 units are "
                     "free. The next 100 units (from 101 to 200) cost Rs. 2 per "
                     "unit. Every unit above 200 costs Rs. 5 per unit."),
    DRAW(income_tax,
         description="Ask the user for a person's annual income and print the "
                     "income tax. There is no tax on the first Rs. 2,50,000. "
                     "Income from 2,50,001 to 5,00,000 is taxed at 5%. Income "
                     "from 5,00,001 to 10,00,000 is taxed at 20%. Any income "
                     "above 10,00,000 is taxed at 30%. (Only the part of the "
                     "income that falls in each band is taxed at that band's "
                     "rate.)"),
    DRAW(shop_discount,
         description="Ask the user for the total bill amount and print the "
                     "amount payable after discount. There is no discount below "
                     "Rs. 1,000. From 1,000 to 4,999 a 5% discount applies; from "
                     "5,000 to 9,999 a 10% discount; and 10,000 or above a 15% "
                     "discount. (The discount applies to the whole amount.)"),
]
