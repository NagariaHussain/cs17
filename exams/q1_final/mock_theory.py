"""CS17 Q1 Final Examination — MOCK paper, Computer Science (Theory).

Practice paper for the real Q1 final (theory.py). Same 50 marks and the same
shape of question in the same quantities, but every question is different and
the parts are in a different order, so nothing can be answered from having seen
the real paper:

    Part A   multiple choice                 8 x 1  =  8
    Part B   number systems                  2 + 3  =  5
    Part C   Boolean algebra                 2 x 3  =  6
    Part D   circuit, spreadsheet, shortcut, bits,
             // and %, software, Calc formulas 6 + 2 =  8
    Part E   flowcharts and algorithms   5 + 4 + 2 + 2 + 7 + 3  = 23

(The real paper runs A = MCQ, B = short answers, C = Boolean, D = number
systems, E = flowcharts. Here the two middle blocks are swapped.)

Everything derived is derived, exactly as in theory.py: each flowchart question
carries a real flowgen Algorithm and each Boolean question a real boolgen
expression, so the chart, the trace and the symptom tables are produced by
running them.
"""

from gens import flowgen
from gens.boolgen import parse
from gens.boolgen.latex import expr_latex
from gens.examgen import (PART, MCQ, GATEMCQ, SHORT, SHEET, CALC, BOOL,
                          TRACE, DRAW, DEBUG)

TITLE = "Q1 Final Examination --- Mock Paper"
SUBJECT = "Computer Science Theory"
DURATION = "2 hours"
DATE = "Practice paper"
MAX_MARKS = 50

INSTRUCTIONS = (
    "All questions are compulsory.",
    "The marks for each question are shown in brackets on the right.",
    "Write all your answers in the answer sheet provided, not on this paper.",
    "Show your working for conversions, truth tables and traces --- "
    "the working carries marks.",
)

# --- Part E algorithms --------------------------------------------------------

# Q17 (5 marks): reverse the digits of a whole number -- pull the last digit off
# with % 10, push it onto the answer with * 10, drop it with // 10. Four times
# round for 5309, three variables changing every pass, so the trace table is a
# real piece of work; and it is the same // and % that Part D asks about.
#
# 5309 rather than 1234: the 0 in the middle means a student who is pattern-
# matching ("the digits just come out backwards") still has to do the
# arithmetic, and the answer 9035 cannot be guessed from the input's shape.
reverse_digits = flowgen.Algorithm("Reverse the digits of a number", [
    flowgen.read("n"),
    flowgen.assign("rev", "0"),
    flowgen.While("n > 0", [
        flowgen.assign("d", "n % 10"),
        flowgen.assign("rev", "rev * 10 + d"),
        flowgen.assign("n", "n // 10"),
    ]),
    flowgen.out("rev"),
])

# Q18 (4 marks): Euclid's algorithm for the HCF, never named on the paper (the
# student just traces it and gets 15 out of 120 and 45, which is the point --
# the reveal is that the machine found the HCF without trying every number).
#
# 120 and 45 give three passes with a different pair every time
# (120,45 -> 45,30 -> 30,15 -> 15,0) and no pass repeats a remainder, so the
# trace table cannot be filled in by copying the row above.
euclid = flowgen.Algorithm("Highest common factor of two numbers", [
    flowgen.read("a"),
    flowgen.read("b"),
    flowgen.While("b > 0", [
        flowgen.assign("r", "a % b"),
        flowgen.assign("a", "b"),
        flowgen.assign("b", "r"),
    ]),
    flowgen.out("a"),
])

# Q19 (2 marks): count how many of n numbers are above a pass mark. TWO bugs,
# both of which show in the output:
#   - the counter starts at 1, not 0 (every answer is one too many)
#   - the test is >= 50 where the question says more than 50
# The input list contains a 50 exactly, so the second bug is visible rather
# than theoretical; without it the wrong comparison would never show.
count_above = flowgen.Algorithm("Count the marks above 50", [
    flowgen.read("n"),
    flowgen.assign("count", "0"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.If("x > 50", [flowgen.assign("count", "count + 1")]),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("count"),
])

# Q20 (2 marks): the second debug question, carrying ONE bug that does not look
# like one -- the loop tests i < n instead of i <= n, so the last number is
# never added. Nothing in the chart is misspelt or out of place; the only way
# to find it is to trace it and notice the total is short by exactly the last
# input. (The real paper's subtle bug is a divide by i instead of n; this is
# the other classic off-by-one, so a student who has seen both has met the two
# ways a counted loop goes wrong.)
sum_n = flowgen.Algorithm("Total of n numbers", [
    flowgen.read("n"),
    flowgen.assign("total", "0"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.assign("total", "total + x"),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("total"),
])

# Q21 (7 marks): every factor of n -- a loop and a decision inside it, which is
# one step past the factorial on the real paper (that one only had a loop).
# Predicted for 12 (six factors) and 7 (two, because it is prime), so the
# student's own trace tells them something: the second answer is the definition
# of a prime number falling out of a flowchart.
factors = flowgen.Algorithm("Print all the factors of n", [
    flowgen.read("n"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.If("n % i == 0", [flowgen.out("i")]),
        flowgen.assign("i", "i + 1"),
    ]),
])

# Q22 (3 marks): read, one formula, one decision that changes the answer,
# print -- the same small shape as the shop bill on the real paper, with a
# surcharge added rather than a discount taken off, so the arithmetic goes the
# other way.
electricity = flowgen.Algorithm("Electricity bill with a surcharge", [
    flowgen.read("units"),
    flowgen.assign("bill", "units * 8"),
    flowgen.If("units > 100", [flowgen.assign("bill", "bill + 500")]),
    flowgen.out("bill"),
])

# --- the paper ----------------------------------------------------------------

PARTS = [
    PART("Part A", "Multiple Choice Questions",
         lead=r"Tick (\checkmark) the correct option for each question.",
         questions=[
             MCQ("What is the full form of URL?", [
                 "Uniform Resource Locator",
                 "Universal Reference Link",
                 "Uniform Retrieval Language",
                 "User Resource Locator",
             ], answer="a"),
             # asked as the VALID one this time, so the three wrong options can
             # each be a different kind of wrong: an octet over 255, only three
             # octets, and five octets
             MCQ("Which of the following \\textbf{is} a valid IP address?", [
                 r"\texttt{256.100.50.1}",
                 r"\texttt{192.168.10.7}",
                 r"\texttt{10.0.0}",
                 r"\texttt{1.2.3.4.5}",
             ], answer="b"),
             # NAND rather than the NOR on the real paper, so De Morgan has to
             # be applied in the other direction. Every option has a different
             # truth table, so only one answer works.
             GATEMCQ(parse("~(A & B)"),
                     [parse("~A & ~B"),          # (a) 1,0,0,0
                      parse("~A | ~B"),          # (b) 1,1,1,0  <- the circuit
                      parse("A & B"),            # (c) 0,0,0,1
                      parse("A | B")],           # (d) 0,1,1,1
                     marks=1, answer="b",
                     text=("Which of the following is the Boolean expression "
                           "for the output $Y$ of the circuit below?")),
             MCQ("Which keyboard shortcut selects everything in the document?", [
                 r"Ctrl + A",
                 r"Ctrl + E",
                 r"Ctrl + S",
                 r"Ctrl + Z",
             ], answer="a"),
             # 2^4 = 16. The distractors are the bit count itself, 2 x 4, and
             # 2^5 (one bit too many)
             MCQ("A picture stores 4 bits for each pixel. \\textbf{How many "
                 "different} colours can one pixel have?", [
                     "4",
                     "8",
                     "16",
                     "32",
                 ], answer="c"),
             # Calc, and nothing here can be recalled off a menu: the cell
             # multiplies before it adds. (a) is what a left-to-right reader
             # gets, and it is the option most students will want.
             MCQ(r"You type \texttt{=5+3*2} into a cell in LibreOffice Calc "
                 r"and press Enter. What appears in the cell?", [
                     "16",
                     "11",
                     "13",
                     r"\texttt{=5+3*2}",
                 ], answer="b"),
             # file formats again, but chosen for a different property: the one
             # that keeps the page looking the same everywhere. .zip is the trap
             # for anyone who memorised the answer to the "many files" question.
             MCQ("You want to email a report so that it looks exactly the same "
                 "on every computer that opens it. Which format should you "
                 "use?", [
                     r"\texttt{.txt}",
                     r"\texttt{.pdf}",
                     r"\texttt{.zip}",
                     r"\texttt{.bmp}",
                 ], answer="b"),
             # the OTHER complement law: a variable OR its own inverse covers
             # every case, so the answer is 1 whatever A is. Written through
             # expr_latex so the notation matches the rest of the paper.
             MCQ("What is the value of $%s$?" % expr_latex(parse("A | ~A")), [
                 "$A$",
                 "$%s$" % expr_latex(parse("~A")),
                 "0",
                 "1",
             ], answer="d"),
         ]),

    PART("Part B", "Number Systems",
         questions=[
             # the reverse direction of the real paper's binary -> decimal:
             # 89 = 1011001, seven bits, and the repeated division leaves a
             # remainder of 1 at both ends so a dropped digit is obvious
             SHORT(r"Convert the decimal number $89_{10}$ to binary.", marks=2),
             # binary -> hex: 110110111 groups from the RIGHT into
             # 1 1011 0111 = 1B7, so the leading group has to be padded --
             # which is the mistake this question is looking for
             SHORT(r"Convert the binary number $\mathrm{110110111}_2$ to "
                   r"hexadecimal.", marks=3),
         ]),

    PART("Part C", "Boolean Algebra",
         questions=[
             # one three-variable product term OR-ed with a two-variable one,
             # as on the real paper, but with the bars in different places so
             # the table comes out differently
             BOOL(parse("(~a & b & ~c) | (a & c)"), 3, ask="truthtable",
                  cases=[{"A": 1, "B": 1, "C": 1}, {"A": 0, "B": 1, "C": 0}]),
             # a NAND feeding an OR: the bar sits over a whole bracket, so the
             # circuit is drawn inside-out (gate first, then the inverter)
             BOOL(parse("~(a & b) | c"), 3, ask="circuit"),
         ]),

    PART("Part D", "Short Answer Questions",
         questions=[
             # one gate of each kind again (NOT, AND, OR) -- circuit only
             BOOL(parse("~a | (b & c)"), 1, ask="circuit", with_table=False),
             # Calc: read a selection off the grid and name the range. Four
             # cells as on the real paper, but in a different place on the
             # sheet so the answer is not the remembered one
             SHEET("C2:D5", marks=1),
             SHORT(r"What is the keyboard shortcut for saving a document in "
                   r"LibreOffice Writer?", marks=1),
             # Worksheet 4 again (1 bit per pixel for black and white), but the
             # multiplication is the picture's size rather than its colour
             # depth: 8 x 8 = 64 pixels, one bit each. "bit" and "pixels" are
             # bold because the question turns on keeping the two apart.
             SHORT("A black-and-white picture uses one \\textbf{bit} for each "
                   "pixel. How many bits are needed for a picture that is "
                   "\\textbf{8 pixels by 8 pixels}?", marks=1),
             # // and % together and SUBTRACTED, so swapping the two operators
             # does not give the same answer: 31 // 7 = 4 and 31 % 7 = 3, so
             # the value is 1 -- and swapping them gives -1
             SHORT(r"What is the value of \texttt{31 // 7 - 31 \% 7}?", marks=1),
             # system vs application software, asked the other way round from
             # the real paper. (b) is the trap: a browser is the program
             # students use most, and it is not system software.
             MCQ("Which of the following is an example of system software?", [
                 "A photo editor",
                 "A web browser",
                 "An operating system",
                 "A spreadsheet program",
             ], answer="c"),
             # A marks table, and two formulas: the whole column, then only the
             # part of it that passed. COUNTIF is not in the paper's little
             # spreadsheet engine, so the second ask is a SUMIF again -- but of
             # a different column from the one being tested, which is the
             # three-argument form and a genuinely different question.
             #
             # The marks are chosen so both answers are round: the six add to
             # 396, and the four at 60 or more (72 + 60 + 88 + 96) come to 316.
             CALC(("Student", "Marks"),
                  [("Asha", 72),
                   ("Bilal", 45),
                   ("Chen", 60),
                   ("Dia", 88),
                   ("Ekta", 35),
                   ("Farid", 96)],
                  asks=[("B8", "=SUM(B2:B7)"),
                        ("B9", '=SUMIF(B2:B7,">=60")')],
                  extra_rows=2,
                  marks=2),
         ]),

    PART("Part E", "Flowcharts and Algorithms",
         questions=[
             TRACE(flowgen.TRACE(reverse_digits, {"n": 5309}), marks=5),
             TRACE(flowgen.TRACE(euclid, {"a": 120, "b": 45}), marks=4),
             DEBUG(count_above,
                   [flowgen.wrong_assign("count", "0", "1"),
                    flowgen.wrong_cond("x > 50", "x >= 50")],
                   cases=[{"n": 5, "x": [72, 50, 45, 90, 60]}],
                   description=("The program should read how many marks there "
                                "are, then read that many marks, and finally "
                                "print how many of them are more than 50."),
                   marks=2),
             DEBUG(sum_n,
                   [flowgen.wrong_cond("i <= n", "i < n")],
                   cases=[{"n": 4, "x": [10, 20, 30, 40]},
                          {"n": 5, "x": [5, 15, 25, 35, 45]}],
                   description=("The program should read how many numbers "
                                "there are, then read that many numbers, and "
                                "print their total."),
                   marks=2),
             DRAW(flowgen.DRAW(
                 factors,
                 description=(r"A program reads a whole number n and prints "
                              r"every factor of n --- that is, every whole "
                              r"number from 1 up to n that divides into n "
                              r"leaving no remainder. For example, the factors "
                              r"of 6 are 1, 2, 3 and 6."),
                 predict=[{"n": 12}, {"n": 7}]),
                 marks=7),
             DRAW(flowgen.DRAW(
                 electricity,
                 description=(r"An electricity board bills a house. The "
                              r"program reads the number of units of "
                              r"electricity used, and works out the bill as "
                              r"$\text{units} \times 8$ rupees. If more than "
                              r"100 units were used, a fixed surcharge of "
                              r"Rs 500 is added to the bill. The program then "
                              r"prints the amount the house has to pay.")),
                 marks=3),
         ]),
]
