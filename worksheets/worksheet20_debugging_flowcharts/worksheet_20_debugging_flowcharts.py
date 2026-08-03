"""Debugging Flowcharts Worksheet — find the one wrong box and fix it.

Worksheets 6-8 asked the student to trace a correct flowchart or draw one from
scratch. This one turns it round: every flowchart here is *nearly* right, and the
student has to work backwards from a wrong output to the box that caused it. The
bugs are the ones beginners actually write, one of each kind:

  a boundary comparison (>= vs >)        the Yes/No arms the wrong way round
  and where it should be or             a loop that stops one step too early
  a missing counter update (never ends)  the wrong operator in an accumulator
  printing the wrong variable            a box drawn inside the loop, not after

Each problem is authored as the CORRECT algorithm plus a one-line bug (see
`gens/flowgen/bug.py`):

  DEBUG(algo, bug, cases=[...], description="what it is supposed to do")

The buggy flowchart, what the program should print, what it actually prints, and
the answer key's fix are ALL derived from that pair, so the planted mistake, the
symptom, and the correction can never disagree.
"""

from gens.flowgen import (Algorithm, read, assign, out, If, While, DEBUG,
                          wrong_cond, wrong_assign, wrong_print, swap_branches,
                          missing, move_into_loop)

TITLE = "Worksheet 20: Debugging Flowcharts"

LEAD = (r"In every problem below, the flowchart has \textbf{exactly one} wrong "
        r"box. The words in italics say what the program is \textit{supposed} to "
        r"do; the table under the flowchart shows what it \textit{should} print "
        r"and what it \textit{actually} prints. Work backwards from that "
        r"difference: do not redraw the whole flowchart --- find the single box "
        r"that is wrong, write what it should say instead, and explain why that "
        r"one box produces the wrong output.")

INDEX_NOTE = ("Reminder: the items of a list have positions counted from 0, so "
              "the list [3, 9, 2, 12, 7] has 5 items in positions 0 to 4. "
              "arr[i] means the item at position i, so arr[0] is 3.")

# --- decisions ----------------------------------------------------------------

# 1. the classic boundary slip: a mark of exactly 40 must pass
pass_fail = Algorithm("Pass or fail at 40 marks", [
    read("marks"),
    If("marks >= 40",
       [out('"Pass"')],
       [out('"Fail"')]),
])

# 2. right decision, arms swapped
even_odd = Algorithm("Even or odd", [
    read("n"),
    If("n % 2 == 0",
       [out('"Even"')],
       [out('"Odd"')]),
])

# 3. a condition where BOTH parts must hold — and vs or
voting = Algorithm("Eligible to vote", [
    read("age"),
    read("citizen"),
    If("age >= 18 and citizen == 1",
       [out('"Eligible"')],
       [out('"Not eligible"')]),
])

# --- loops --------------------------------------------------------------------

# 4. counting loop: the test decides whether the last number is printed
print_1_to_n = Algorithm("Print 1 to n", [
    read("n"),
    assign("i", "1"),
    While("i <= n", [
        out("i"),
        assign("i", "i + 1"),
    ]),
])

# 5. an accumulator whose starting value must be 0 (nothing added yet)
sum_1_to_n = Algorithm("Sum of the numbers 1 to n", [
    read("n"),
    assign("total", "0"),
    assign("i", "1"),
    While("i <= n", [
        assign("total", "total + i"),
        assign("i", "i + 1"),
    ]),
    out("total"),
])

# 6. a fixed 10-step loop — the counter update is what makes it stop
times_table = Algorithm("Multiplication table of n", [
    read("n"),
    assign("i", "1"),
    While("i <= 10", [
        out("n * i"),
        assign("i", "i + 1"),
    ]),
])

# 7. an accumulator that multiplies, not adds
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

# 8. two things to work out, and only one of them is the answer
average = Algorithm("Average of n numbers", [
    read("n"),
    assign("sum", "0"),
    assign("i", "1"),
    While("i <= n", [
        read("x"),
        assign("sum", "sum + x"),
        assign("i", "i + 1"),
    ]),
    assign("avg", "sum / n"),
    out("avg"),
])

# --- a decision inside a loop -------------------------------------------------

# 9. count how many marks pass — the answer is printed ONCE, at the end
count_passes = Algorithm("How many students passed", [
    read("n"),
    assign("count", "0"),
    assign("i", "1"),
    While("i <= n", [
        read("marks"),
        If("marks >= 40",
           [assign("count", "count + 1")]),
        assign("i", "i + 1"),
    ]),
    out("count"),
])

# 10. "best so far" — the comparison decides whether you get the largest or the
# smallest (arr is a given list the algorithm indexes, never read)
largest_in_list = Algorithm("Largest number in a list", [
    assign("max", "arr[0]"),
    assign("i", "1"),
    While("i < 5", [
        If("arr[i] > max",
           [assign("max", "arr[i]")]),
        assign("i", "i + 1"),
    ]),
    out("max"),
])

PROBLEMS = [
    DEBUG(pass_fail, wrong_cond("marks >= 40", "marks > 40"),
          cases=[{"marks": 72}, {"marks": 40}, {"marks": 12}],
          description="A student passes if they score 40 marks or more. The "
                      "program reads a student's marks and prints “Pass” or "
                      "“Fail”.",
          why="40 marks must pass, so the test has to include 40 itself: "
              "“more than 40” leaves the boundary value out. Only the input 40 "
              "shows the bug — 72 and 12 look fine, which is why boundary values "
              "are always worth testing."),

    DEBUG(even_odd, swap_branches("n % 2 == 0"),
          cases=[{"n": 6}, {"n": 7}],
          description="The program reads a number and prints “Even” if the "
                      "number is even, and “Odd” if it is odd.",
          note="Reminder: n % 2 is the remainder when n is divided by 2, so "
               "n % 2 is 0 exactly when n is even.",
          why="The condition is right but the two arms are the wrong way round: "
              "the Yes arm (remainder 0) is the even case, so it must print "
              "“Even”. Every input comes out wrong — the answers are simply "
              "swapped."),

    DEBUG(voting, wrong_cond("age >= 18 and citizen == 1",
                             "age >= 18 or citizen == 1"),
          cases=[{"age": 20, "citizen": 1}, {"age": 15, "citizen": 1},
                 {"age": 30, "citizen": 0}],
          description="A person may vote only if they are 18 or older AND they "
                      "are a citizen. The program reads the person's age and "
                      "citizen (1 means yes, 0 means no) and prints “Eligible” "
                      "or “Not eligible”.",
          why="Both conditions must hold, so they are joined with “and”. With "
              "“or”, meeting just one of them is enough — a 15-year-old citizen "
              "and a 30-year-old non-citizen both slip through."),

    DEBUG(print_1_to_n, wrong_cond("i <= n", "i < n"),
          cases=[{"n": 5}, {"n": 1}],
          description="The program reads a number n and prints every number from "
                      "1 up to n — so for n = 5 it prints 1, 2, 3, 4, 5.",
          why="The loop must keep going while i is still 1 to n, and that "
              "includes i = n itself. Testing i < n stops one step too early, so "
              "the last number is never printed (and for n = 1 nothing is "
              "printed at all)."),

    DEBUG(sum_1_to_n, wrong_assign("total", "0", "1"),
          cases=[{"n": 5}, {"n": 3}],
          description="The program reads a number n and prints the total of all "
                      "the numbers from 1 to n — so for n = 5 it prints "
                      "1+2+3+4+5 = 15.",
          why="Before the loop, nothing has been added yet, so the running total "
              "must start at 0. Starting it at 1 adds a stray 1 that is not one "
              "of the numbers, so every answer is 1 too big."),

    DEBUG(times_table, missing("i = i + 1"),
          cases=[{"n": 3}],
          description="The program reads a number n and prints its "
                      "multiplication table from n × 1 up to n × 10 — so for "
                      "n = 3 it prints 3, 6, 9, …, 30.",
          why="Nothing inside the loop changes i, so i stays 1 for ever, the "
              "test “i is 10 or less” is always true, and the loop never ends — "
              "it keeps "
              "printing n × 1. A counting loop needs its counter to move on "
              "every time round."),

    DEBUG(factorial, wrong_assign("fact", "fact * i", "fact + i"),
          cases=[{"n": 4}, {"n": 5}],
          description="The program reads a number n and prints its factorial — "
                      "the product 1 × 2 × 3 × … × n. So for n = 4 it prints "
                      "1 × 2 × 3 × 4 = 24.",
          why="A factorial multiplies the numbers together, so the running value "
              "must be multiplied by i each time round. Adding instead gives the "
              "total of the numbers, not their product."),

    DEBUG(average, wrong_print("avg", "sum"),
          cases=[{"n": 4, "x": [10, 20, 30, 40]}, {"n": 2, "x": [7, 9]}],
          description="The program reads how many numbers there are (n), then "
                      "reads that many numbers one by one and prints their "
                      "average — the total divided by how many there were.",
          why="The average is worked out correctly and stored in avg, but the "
              "program prints sum, the running total, instead. The right value "
              "is computed and then thrown away."),

    DEBUG(count_passes, move_into_loop("print count"),
          cases=[{"n": 4, "marks": [55, 32, 80, 40]}],
          description="The program reads how many students there are (n), then "
                      "reads each student's marks and finally prints how many of "
                      "them passed (40 marks or more). For the marks 55, 32, 80, "
                      "40 it should print just one number: 3.",
          why="The count is only finished once every student has been read, so "
              "the print box belongs after the loop, not inside it. Drawn inside "
              "the loop it runs on every turn and prints the count so far each "
              "time."),

    DEBUG(largest_in_list, wrong_cond("arr[i] > max", "arr[i] < max"),
          cases=[{"arr": (3, 9, 2, 12, 7)}, {"arr": (8, 1, 6, 4, 5)}],
          description="The program goes through a list of 5 numbers and prints "
                      "the largest of them. It starts by assuming the first item "
                      "is the biggest, then checks every later item and remembers "
                      "any item that beats the best one so far.",
          note=INDEX_NOTE,
          why="max is meant to hold the biggest value seen so far, so it should "
              "be replaced only by an item that is bigger than it. With the "
              "comparison the other way round the program keeps the smaller item "
              "every time, so it prints the smallest number in the list."),
]
