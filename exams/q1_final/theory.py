"""CS17 Q1 Final Examination — Computer Science (Theory).

50 marks, five parts:

    Part A   multiple choice                 8 x 1  =  8
    Part B   circuit, spreadsheet, shortcut, bits,
             // and %, software, Calc formulas 6 + 2 =  8
    Part C   Boolean algebra                 2 x 3  =  6
    Part D   number systems                  2 + 3  =  5
    Part E   flowcharts and algorithms   5 + 4 + 2 + 2 + 7 + 3  = 23

Questions still to be written are TBD(...) placeholders that reserve their
marks, so the paper always totals 50 while it is being filled in. The last two
1-mark questions in Part B are the spare that brings the rest (48 marks) up to
50 -- move them to whichever part should carry them.

Everything derived is derived: each flowchart question carries a real flowgen
Algorithm (the chart, the trace table's columns, and the should-print /
actually-prints table are all produced by running it) and each Boolean
question carries a real boolgen expression.
"""

from gens import flowgen
from gens.boolgen import parse
from gens.boolgen.latex import expr_latex
from gens.examgen import (PART, MCQ, GATEMCQ, SHORT, SHEET, CALC, TBD, BOOL,
                          TRACE, DRAW, DEBUG)

TITLE = "Q1 Final Examination"
SUBJECT = "Computer Science Theory"
DURATION = "2 hours"
DATE = "7th August 2026"
MAX_MARKS = 50

INSTRUCTIONS = (
    "All questions are compulsory.",
    "The marks for each question are shown in brackets on the right.",
    "Write all your answers in the answer sheet provided, not on this paper.",
    "Show your working for conversions, truth tables and traces --- "
    "the working carries marks.",
)

# --- Part E algorithms --------------------------------------------------------
# Authored once each; the flowchart, the trace table and (for the debug
# question) the symptom table are all derived from these.

# Q16: the merge step of merge sort -- two ordered lists walked at the same
# time, always taking the smaller front item next. Never named on the paper:
# the student just traces it (and gets a sorted list out, which is the point).
merge = flowgen.Algorithm("Combine two ordered lists into one", [
    flowgen.assign("i", "0"),
    flowgen.assign("j", "0"),
    flowgen.While("i < 3 and j < 3", [
        flowgen.If("A[i] < B[j]",
                   [flowgen.out("A[i]"), flowgen.assign("i", "i + 1")],
                   [flowgen.out("B[j]"), flowgen.assign("j", "j + 1")]),
    ]),
    flowgen.While("i < 3", [
        flowgen.out("A[i]"),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.While("j < 3", [
        flowgen.out("B[j]"),
        flowgen.assign("j", "j + 1"),
    ]),
])

# Q16: square root the Babylonian (Heron / Newton) way -- start at n // 2 and
# replace the guess by the average of the guess and n // guess, six times. It
# closes in fast: n = 1000 gives 500 -> 251 -> 127 -> 67 -> 40 -> 32 -> 31,
# against the true 31.6228, so every one of the six rows is a different number.
#
# Everything is WHOLE-NUMBER division. An earlier decimal version (round(...,1))
# was dropped: past the first step the guess is a 1-dp number like 4.7, so every
# division after it recurs (20 / 4.7 = 4.2553...), which is unusable in a trace
# table -- and no n avoids it (searched n = 2..6000, none gives four
# non-recurring divisions). With // the divisions are exact by construction.
babylonian = flowgen.Algorithm("Square root by repeated averaging", [
    flowgen.read("n"),
    flowgen.assign("x", "n // 2"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= 6", [
        flowgen.assign("x", "(x + n // x) // 2"),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("x"),
])

# No note explaining //: it has been taught, and Part A already asks for the
# value of 23 // 4 - 23 % 4. Knowing it is part of what this question tests.

# Q17: the SMALLEST of n numbers (largest was done in class, so the debug
# question is the other way round -- they cannot pattern-match it). The guess
# starts at 9999 rather than 0, since every number is smaller than nothing.
#
# TWO bugs are planted in it below -- the loop stops one number early, and the
# print box sits inside the loop instead of after it. The input list ends with
# its smallest value, so BOTH bugs show up in the output (with the smallest
# anywhere else, the short loop would be invisible).
smallest = flowgen.Algorithm("Smallest of n numbers", [
    flowgen.read("n"),
    flowgen.assign("i", "1"),
    flowgen.assign("smallest", "9999"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.If("x < smallest", [flowgen.assign("smallest", "x")]),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("smallest"),
])

# The second debug question, carrying ONE bug -- but not a visible one. The
# planted mistake is the divide box after the loop: avg = total // i instead of
# total // n. Nothing about that box LOOKS wrong; finding it means knowing that
# i does not stop at n, it stops at n + 1 (the loop only ends once the test
# fails), so the total is shared out among one person too many. A student who
# only skims the chart cannot spot it, and a student who traces it will.
#
# // rather than / so the answers are whole numbers, and the inputs divide
# exactly either way, so the whole-number division changes nothing the student
# has to reason about.
average = flowgen.Algorithm("Average of n numbers", [
    flowgen.read("n"),
    flowgen.assign("total", "0"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.assign("total", "total + x"),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.assign("avg", "total // n"),
    flowgen.out("avg"),
])

# Q19: factorial -- drawn by the student, traced for 5 and 6 (the answers, 120
# and 720, are run from this algorithm, so their trace has something to check).
factorial = flowgen.Algorithm("Factorial of n", [
    flowgen.read("n"),
    flowgen.assign("f", "1"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.assign("f", "f * i"),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("f"),
])

# Q20: read a few values -> one formula in a process box -> a single decision
# that changes the answer -> print. (Simple interest has been set often enough;
# this one adds the if/else without adding a loop.)
shop_bill = flowgen.Algorithm("Bill with a discount over Rs 1000", [
    flowgen.read("price"),
    flowgen.read("quantity"),
    flowgen.assign("total", "price * quantity"),
    flowgen.If("total > 1000",
               [flowgen.assign("total", "total - total * 10 / 100")]),
    flowgen.out("total"),
])

# --- the paper ----------------------------------------------------------------

PARTS = [
    PART("Part A", "Multiple Choice Questions",
         lead=r"Tick (\checkmark) the correct option for each question.",
         questions=[
             MCQ("What is the full form of DHCP?", [
                 "Domain Host Control Protocol",
                 "Dynamic Host Configuration Protocol",
                 "Data Host Communication Protocol",
                 "Dynamic Hypertext Connection Protocol",
             ], answer="b"),
             MCQ("Which pair of keyboard shortcuts is used to copy and then "
                 "paste?", [
                     r"Ctrl + X, then Ctrl + V",
                     r"Ctrl + C, then Ctrl + V",
                     r"Ctrl + C, then Ctrl + P",
                     r"Ctrl + S, then Ctrl + V",
                 ], answer="b"),
             # only one octet is out of range (300 > 255); the other three
             # addresses are ordinary ones, including a .255 host part, which
             # is legal and catches anyone who thinks 255 is the invalid bit
             MCQ("Which of the following is \\textbf{not} a valid IP address?", [
                 r"\texttt{192.168.1.1}",
                 r"\texttt{10.0.0.255}",
                 r"\texttt{172.16.300.5}",
                 r"\texttt{8.8.8.8}",
             ], answer="c"),
             # The direction taught in class: the circuit is one bar over
             # the whole thing (OR into a NOT), and the answer breaks it into
             # two separate bars. The straight reading, A+B under one bar, is
             # not on offer, so the mark needs the expansion -- but every wrong
             # option has a different truth table, so only one answer is right.
             GATEMCQ(parse("~(A | B)"),
                     [parse("~A | ~B"),          # (a) 1,1,1,0
                      parse("~A & ~B"),          # (b) 1,0,0,0  <- the circuit
                      parse("A | B"),            # (c) 0,1,1,1
                      parse("A & B")],           # (d) 0,0,0,1
                     marks=1, answer="b",
                     text=("Which of the following is the Boolean expression "
                           "for the output $Y$ of the circuit below?")),
             # 2^7 = 128. The distractors are the three near misses: the bit
             # count itself, 2^6, and 2^8 (thinking a character is a whole byte)
             MCQ("ASCII uses 7 bits for each character. \\textbf{How many "
                 "different} characters can ASCII represent?", [
                     "7",
                     "64",
                     "128",
                     "256",
                 ], answer="c"),
             # Calc. The stem does NOT point out that the equals sign is
             # missing -- noticing that is the whole question. Nothing here can
             # be answered from memory of a menu or a shortcut.
             MCQ(r"You type \texttt{A1+A2} into a cell in LibreOffice Calc and "
                 r"press Enter. What appears in the cell?", [
                     "The sum of the values in A1 and A2",
                     r"The text \texttt{A1+A2}",
                     "An error message",
                     "0",
                 ], answer="b"),
             # file extensions, asked as a choice of tool rather than a list to
             # recall: the image formats are the distractors, and picking .zip
             # means knowing it is the one that holds many files as one
             MCQ("You need to send 50 files to your teacher as a single email "
                 "attachment. Which format should you use?", [
                     r"\texttt{.png}",
                     r"\texttt{.jpg}",
                     r"\texttt{.zip}",
                     r"\texttt{.txt}",
                 ], answer="c"),
             # the complement law: a variable AND its own inverse can never both
             # be 1, so the answer is 0 whatever A is. Written through
             # expr_latex so the notation matches every other expression on the
             # paper. (a) and (b) catch anyone treating the bar as a no-op.
             MCQ("What is the value of $%s$?" % expr_latex(parse("A & ~A")), [
                 "$A$",
                 "$%s$" % expr_latex(parse("~A")),
                 "0",
                 "1",
             ], answer="c"),
         ]),

    PART("Part B", "Short Answer Questions",
         questions=[
             # one gate of each kind (AND, OR, NOT) -- circuit only, no table
             BOOL(parse("(a & b) | ~c"), 1, ask="circuit", with_table=False),
             # Calc: read a selection off the grid and name the range
             SHEET("B2:C3", marks=1),
             SHORT(r"What is the keyboard shortcut for undoing an action in "
                   r"LibreOffice Writer?", marks=1),
             # extends Worksheet 4 (a black-and-white picture is 1 bit per
             # pixel) to colour: a byte per channel. "RGB" already says there
             # are three, so the count is not handed over -- answering means
             # going byte -> 8 bits -> x3, testing the binary work too. As a
             # short answer there is no 24 to recognise on the page: the three
             # multiplication has to be done. "byte" and "bits" are bold: the
             # whole question turns on noticing they are different units, and
             # these are beginners
             SHORT("One pixel of an RGB image uses one \\textbf{byte} for each "
                   "of the colours. How many \\textbf{bits} is that per pixel?",
                   marks=1),
             # // and % together, and SUBTRACTED rather than added: with a plus
             # the expression is symmetric, so a student who swaps the two
             # operators still gets the right total. As a short answer there is
             # nothing to eliminate against -- both operators have to be worked
             # out (5 - 3 = 2), which is also what the Part E trace needs.
             SHORT(r"What is the value of \texttt{23 // 4 - 23 \% 4}?", marks=1),
             # application vs system software, asked about the one program every
             # student has used. (d) is the trap: an operating system IS system
             # software, so a student who half-remembers the pair can pick it
             MCQ("A computer game is an example of which type of software?", [
                 "System software",
                 "Application software",
                 "Utility software",
                 "Operating system",
             ], answer="b"),
             # A price list, and two formulas to work out by hand: the whole
             # column, then only the part of it above 200. SUMIF is the point of
             # the question -- adding six numbers is arithmetic, deciding WHICH
             # six to add is the spreadsheet.
             #
             # The prices are chosen so both answers are round: the six add to
             # 1600, and the three at 200 or under (40 + 150 + 10) come to
             # exactly 200, leaving 1400. A student who mis-copies one price
             # lands on an untidy number and knows to look again. Both answers
             # are evaluated against this same table (gens/examgen/calc.py), so
             # the data and the answers cannot drift apart.
             CALC(("Item", "Price"),
                  [("Pen", 40),
                   ("Notebook", 150),
                   ("Bag", 850),
                   ("Water bottle", 250),
                   ("Eraser", 10),
                   ("Lunch box", 300)],
                  asks=[("B8", "=SUM(B2:B7)"),
                        ("B9", '=SUMIF(B2:B7,">200")')],
                  extra_rows=2,
                  marks=2),
         ]),

    PART("Part C", "Boolean Algebra",
         questions=[
             # one product term over all three variables (AND + NOT), OR-ed
             # with a second: worth the 4 marks, unlike two 2-variable terms
             BOOL(parse("(a & ~b & c) | (~a & b)"), 3, ask="truthtable",
                  cases=[{"A": 1, "B": 0, "C": 1}, {"A": 1, "B": 1, "C": 0}]),
             BOOL(parse("(a | b) & ~c"), 3, ask="circuit"),
         ]),

    PART("Part D", "Number Systems",
         questions=[
             SHORT(r"Convert the binary number $\mathrm{1011010}_2$ to "
                   r"decimal.", marks=2),
             SHORT(r"Convert the hexadecimal number $\mathrm{2AF}_{16}$ to "
                   r"binary.", marks=3),
         ]),

    PART("Part E", "Flowcharts and Algorithms",
         questions=[
             TRACE(flowgen.TRACE(merge, {"A": (2, 5, 9), "B": (3, 6, 8)}),
                   marks=5),
             TRACE(flowgen.TRACE(babylonian, {"n": 1000}), marks=4),
             DEBUG(smallest,
                   [flowgen.wrong_cond("i <= n", "i < n"),
                    flowgen.move_into_loop("print smallest")],
                   cases=[{"n": 5, "x": [30, 25, 15, 20, 10]}],
                   description=("The program should read how many numbers there "
                                "are, then read that many numbers, and finally "
                                "print the smallest of them --- once."),
                   marks=2),
             DEBUG(average,
                   [flowgen.wrong_assign("avg", "total // n", "total // i")],
                   cases=[{"n": 4, "x": [10, 20, 30, 40]},
                          {"n": 5, "x": [20, 30, 10, 40, 20]}],
                   description=("The program should read how many numbers there "
                                "are, then read that many numbers, and print "
                                "their average."),
                   marks=2),
             DRAW(flowgen.DRAW(
                 factorial,
                 description=(r"A program reads a whole number n and prints the "
                              r"factorial of n. The factorial of n is "
                              r"$1 \times 2 \times 3 \times \cdots \times n$, "
                              r"so the factorial of 4 is "
                              r"$1 \times 2 \times 3 \times 4 = 24$."),
                 predict=[{"n": 5}, {"n": 6}]),
                 marks=7),
             DRAW(flowgen.DRAW(
                 shop_bill,
                 description=(r"A shop bills a customer. The program reads the "
                              r"price of one item and the quantity bought, and "
                              r"works out the total as "
                              r"$\text{price} \times \text{quantity}$. If the "
                              r"total is more than 1000, the shop gives the "
                              r"customer a 10% discount on the total. The "
                              r"program then prints the amount the customer has "
                              r"to pay.")),
                 marks=3),
         ]),
]
