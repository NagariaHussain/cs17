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

sign = Algorithm("Sign of a number", [
    read("n"),
    If("n > 0",
       [out('"Positive"')],
       [If("n < 0",
           [out('"Negative"')],
           [out('"Zero"')])]),
])

loan = Algorithm("Loan eligibility", [
    read("age"),
    read("salary"),
    If("age >= 21 and age <= 60 and salary >= 25000",
       [out('"Eligible"')],
       [out('"Not eligible"')]),
])

triangle_type = Algorithm("Triangle type by sides", [
    read("a"),
    read("b"),
    read("c"),
    If("a == b and b == c",
       [out('"Equilateral"')],
       [If("a == b or b == c or a == c",
           [out('"Isosceles"')],
           [out('"Scalene"')])]),
])

bmi = Algorithm("BMI category", [
    read("weight"),
    read("height"),
    assign("bmi", "weight / (height * height)"),
    If("bmi < 18.5",
       [out('"Underweight"')],
       [If("bmi < 25",
           [out('"Normal"')],
           [out('"Overweight"')])]),
])

PROBLEMS = [
    DRAW(electricity,
         description="Ask the user for the number of electricity units consumed "
                     "in a month and print the bill. The first 100 units are "
                     "free. The next 100 units (from 101 to 200) cost Rs. 2 per "
                     "unit. Every unit above 200 costs Rs. 5 per unit.",
         example="if units = 250, the first 100 units are free, the next 100 "
                 "cost 100 × 2 = Rs. 200, and the remaining 50 cost 50 × 5 = "
                 "Rs. 250, so the bill is Rs. 450.",
         predict=[{"units": 90}, {"units": 150}, {"units": 320}]),
    DRAW(income_tax,
         description="Ask the user for a person's annual income and print the "
                     "income tax. There is no tax on the first Rs. 2,50,000. "
                     "Income from 2,50,001 to 5,00,000 is taxed at 5%. Income "
                     "from 5,00,001 to 10,00,000 is taxed at 20%. Any income "
                     "above 10,00,000 is taxed at 30%. (Only the part of the "
                     "income that falls in each band is taxed at that band's "
                     "rate.)",
         example="if income = 6,00,000, the first 2,50,000 is tax-free, the "
                 "next 2,50,000 is taxed at 5% = Rs. 12,500, and the remaining "
                 "1,00,000 is taxed at 20% = Rs. 20,000, so the tax is Rs. 32,500.",
         predict=[{"income": 200000}, {"income": 400000}, {"income": 1200000}]),
    DRAW(shop_discount,
         description="Ask the user for the total bill amount and print the "
                     "amount payable after discount. There is no discount below "
                     "Rs. 1,000. From 1,000 to 4,999 a 5% discount applies; from "
                     "5,000 to 9,999 a 10% discount; and 10,000 or above a 15% "
                     "discount. (The discount applies to the whole amount.)",
         example="if amount = 6,000, it falls in the 5,000–9,999 band, so a 10% "
                 "discount applies and the amount payable is 6,000 × 0.90 = "
                 "Rs. 5,400.",
         predict=[{"amount": 800}, {"amount": 3000}, {"amount": 15000}]),
    DRAW(sign,
         description="Ask the user for a number n and print whether it is "
                     "“Positive”, “Negative”, or “Zero”."),
    DRAW(loan,
         description="A bank checks loan applications. Ask the user for the "
                     "applicant's age and monthly salary. The applicant is "
                     "“Eligible” only if their age is between 21 and 60 (both "
                     "included) and their salary is at least Rs. 25,000; "
                     "otherwise print “Not eligible”."),
    DRAW(triangle_type,
         description="Ask the user for the lengths of the three sides of a "
                     "triangle and print its type. If all three sides are equal "
                     "it is “Equilateral”; if exactly two sides are equal it is "
                     "“Isosceles”; if all sides are different it is “Scalene”."),
    DRAW(bmi,
         description="Ask the user for a person's weight (in kg) and height (in "
                     "metres) and print their BMI category. First compute BMI = "
                     "weight ÷ (height × height). A BMI below 18.5 is "
                     "“Underweight”, from 18.5 up to (but not including) 25 is "
                     "“Normal”, and 25 or above is “Overweight”."),
]
