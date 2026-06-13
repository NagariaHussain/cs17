"""Flowchart problem bank — extra algorithms not currently on any worksheet.

A holding area for authored-but-unused flowchart algorithms. Nothing here is
built (the Makefile only builds the worksheet modules), so this file has no
TITLE and no PROBLEMS list. To put one of these on a worksheet, copy its
Algorithm into that worksheet module and add a DRAW(...) (a ready-to-use
statement is given in the comment above each one).

These are written for the same flowgen DSL as the worksheets:
    from gens.flowgen import Algorithm, read, assign, out, If, While, DRAW
"""

from gens.flowgen import Algorithm, read, assign, out, If, While

# DRAW: "Ask the user for a number n. If n is divisible by 3 or by 5, print
# “Divisible”; otherwise print “Not divisible”."
divisible = Algorithm("Divisible by 3 or 5", [
    read("n"),
    If("n % 3 == 0 or n % 5 == 0",
       [out('"Divisible"')],
       [out('"Not divisible"')]),
])

# DRAW: "A shopkeeper enters the cost price and the selling price of an item.
# If it was sold for more than it cost, print “Profit” and the profit amount.
# If it was sold for less, print “Loss” and the loss amount. If the two prices
# are equal, print “No profit, no loss”."
profit_loss = Algorithm("Profit or loss", [
    read("cp"),
    read("sp"),
    If("sp > cp",
       [out('"Profit"'), out("sp - cp")],
       [If("sp < cp",
           [out('"Loss"'), out("cp - sp")],
           [out('"No profit, no loss"')])]),
])

# DRAW: "Ask the user for three numbers and print the largest of the three."
largest = Algorithm("Largest of three numbers", [
    read("a"),
    read("b"),
    read("c"),
    If("a >= b and a >= c",
       [out("a")],
       [If("b >= c", [out("b")], [out("c")])]),
])

# DRAW: "Ask the user for a year and print whether it is a leap year. A year is
# a leap year if it is divisible by 4 — except that years divisible by 100 are
# not leap years, unless they are also divisible by 400. (So 2000 is a leap
# year, but 1900 is not.)"
leap_year = Algorithm("Leap year check", [
    read("year"),
    If("year % 400 == 0",
       [out('"Leap Year"')],
       [If("year % 100 == 0",
           [out('"Not a Leap Year"')],
           [If("year % 4 == 0",
               [out('"Leap Year"')],
               [out('"Not a Leap Year"')])])]),
])

# DRAW: "Ask the user for a number n and print its factorial — the product
# 1 × 2 × 3 × … × n. (For example, the factorial of 4 is 1 × 2 × 3 × 4 = 24.)"
factorial = Algorithm("Factorial of n", [
    read("n"),
    assign("fact", "1"),
    assign("i", "1"),
    While("i <= n", [
        assign("fact", "fact * i"),
        assign("i", "i + 1"),
    ]),
    out("fact"),
])
