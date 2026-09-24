"""CS17 Q1 Final Examination — MOCK PAPER 2, Computer Science (Theory).

The second practice paper for the Q1 final (theory.py). Same 50 marks and the
same kinds of question in the same quantities as the real paper, but a third
running order and a harder set of questions than mock_theory.py: where the real
paper reads a value off a grid, this one asks what a copied formula becomes;
where it converts a number, this one adds two binary numbers; and every
flowchart carries either a decision inside the loop or a bug that only one of
the two test cases exposes.

    Part A   multiple choice                 8 x 1  =  8
    Part B   Boolean algebra                 2 x 3  =  6
    Part C   circuit, spreadsheet, shortcut, bits,
             // and %, software, Calc formulas 6 + 2 =  8
    Part D   number systems                  2 + 3  =  5
    Part E   flowcharts and algorithms   5 + 4 + 2 + 2 + 7 + 3  = 23

Running orders so far: real paper A-MCQ B-short C-bool D-number E-flow;
mock 1 A-MCQ B-number C-bool D-short E-flow; this one A-MCQ B-bool C-short
D-number E-flow.

Everything derived is derived, as in theory.py: each flowchart question carries
a real flowgen Algorithm (chart, trace columns and the should-print /
actually-prints table are all produced by running it) and each Boolean question
a real boolgen expression.
"""

from gens import flowgen
from gens.boolgen import parse
from gens.boolgen.latex import expr_latex
from gens.examgen import (PART, MCQ, GATEMCQ, SHORT, SHEET, CALC, BOOL,
                          TRACE, DRAW, DEBUG)

TITLE = "Q1 Final Examination --- Mock Paper 2"
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

# Q17 (5 marks): decimal -> binary by repeated division, printing the remainder
# each time round -- so the bits come out BACKWARDS. The chart is never named,
# and the `reveal` line tells the student what they have just traced only after
# the trace table, so the question is a genuine trace and not a conversion they
# can shortcut with the method from Part D.
#
# n = 45 gives six passes and the bit pattern 101101, whose reverse (101101) is
# NOT a palindrome-free accident to worry about -- 45 = 101101 reads the same
# either way, so a student who forgets that the printout is reversed still gets
# a defensible answer, while the trace table itself still has to be right.
# (Deliberate: the trap is in the trace, not in a gotcha at the end.)
to_binary = flowgen.Algorithm("Print the remainders of repeated division by 2", [
    flowgen.read("n"),
    flowgen.While("n > 0", [
        flowgen.assign("b", "n % 2"),
        flowgen.out("b"),
        flowgen.assign("n", "n // 2"),
    ]),
])

# Q18 (4 marks): Russian-peasant multiplication -- double one number, halve the
# other, and add up the rows where the halved number is odd. Four passes for
# 13 x 11, three variables changing on every one of them, and a decision INSIDE
# the loop (the real paper's 4-marker had none), so the trace has to record a
# branch that is sometimes taken and sometimes not.
peasant = flowgen.Algorithm("Multiply two numbers by doubling and halving", [
    flowgen.read("a"),
    flowgen.read("b"),
    flowgen.assign("p", "0"),
    flowgen.While("b > 0", [
        flowgen.If("b % 2 == 1", [flowgen.assign("p", "p + a")]),
        flowgen.assign("a", "a * 2"),
        flowgen.assign("b", "b // 2"),
    ]),
    flowgen.out("p"),
])

# Q19 (2 marks): count the even numbers and the odd numbers. TWO bugs:
#   - the Yes and No arms of the decision are the wrong way round, so the two
#     counts are swapped
#   - "print even" was drawn inside the loop instead of after it
# The test case has a different number of evens and odds (3 and 2), so the swap
# actually shows -- with an equal split both bugs would hide one another.
odd_even = flowgen.Algorithm("Count the even and the odd numbers", [
    flowgen.read("n"),
    flowgen.assign("even", "0"),
    flowgen.assign("odd", "0"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.If("x % 2 == 0",
                   [flowgen.assign("even", "even + 1")],
                   [flowgen.assign("odd", "odd + 1")]),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("even"),
    flowgen.out("odd"),
])

# Q20 (2 marks): the largest of n numbers, with ONE bug that is invisible on
# the first test case and fatal on the second: the first guess is 0 instead of
# a number lower than any input. With four positive numbers the program is
# right; with four negative ones it prints 0, which is not even one of the
# numbers that was read. Harder than the real paper's subtle bug -- there the
# symptom showed on every case, here the student has to explain why ONE case
# works, which is the whole skill of reading a test result.
largest = flowgen.Algorithm("Largest of n numbers", [
    flowgen.read("n"),
    flowgen.assign("largest", "-9999"),
    flowgen.assign("i", "1"),
    flowgen.While("i <= n", [
        flowgen.read("x"),
        flowgen.If("x > largest", [flowgen.assign("largest", "x")]),
        flowgen.assign("i", "i + 1"),
    ]),
    flowgen.out("largest"),
])

# Q21 (7 marks): the sum of a number's digits -- a loop whose counter is the
# number itself, shrinking by a factor of ten each pass. Nothing counts from 1
# to n, so the shape of the loop has to be worked out rather than copied from
# the factorial done in class. Predicted for 4728 (21) and 999 (27): the second
# never carries the same digit twice, so a wrong answer cannot be luck.
digit_sum = flowgen.Algorithm("Sum of the digits of n", [
    flowgen.read("n"),
    flowgen.assign("s", "0"),
    flowgen.While("n > 0", [
        flowgen.assign("d", "n % 10"),
        flowgen.assign("s", "s + d"),
        flowgen.assign("n", "n // 10"),
    ]),
    flowgen.out("s"),
])

# Q22 (3 marks): read, a formula, one decision, print -- the same small shape
# as the real paper's shop bill, but the decision does not adjust the whole
# answer by a percentage: it pays extra on the HOURS ABOVE 40 only, so the
# formula inside the branch has a subtraction in it.
wages = flowgen.Algorithm("Weekly pay with overtime", [
    flowgen.read("hours"),
    flowgen.assign("pay", "hours * 50"),
    flowgen.If("hours > 40",
               [flowgen.assign("pay", "pay + (hours - 40) * 50")]),
    flowgen.out("pay"),
])

# --- the paper ----------------------------------------------------------------

PARTS = [
    PART("Part A", "Multiple Choice Questions",
         lead=r"Tick (\checkmark) the correct option for each question.",
         questions=[
             # binary addition in a one-mark box: 1011 + 110 = 10001 (11 + 6 =
             # 17). The carry runs the whole way along, so every wrong option is
             # a carry dropped somewhere different.
             MCQ(r"What is $1011_2 + 110_2$?", [
                 r"$1101_2$",
                 r"$10001_2$",
                 r"$10101_2$",
                 r"$1111_2$",
             ], answer="b"),
             # a THREE-variable circuit (the real paper's was two): a NOR into
             # an AND. The straight reading is the answer only after the bar is
             # pushed onto each variable, and every option has a different
             # truth table.
             GATEMCQ(parse("~(A | B) & C"),
                     [parse("~A & ~B & C"),      # (a) true on 001 only <- circuit
                      parse("~A | ~B | C"),      # (b) true almost everywhere
                      parse("~(A & B) & C"),     # (c) true on 001, 011, 101
                      parse("~(A | B | C)")],    # (d) true on 000 only
                     marks=1, answer="a",
                     text=("Which of the following is the Boolean expression "
                           "for the output $Y$ of the circuit below?")),
             MCQ("How many bits are there in an IPv4 address such as "
                 r"\texttt{192.168.1.1}?", [
                     "8",
                     "16",
                     "32",
                     "64",
                 ], answer="c"),
             # relative references: copying a formula DOWN moves its row. This
             # is the one spreadsheet idea a student cannot get from a menu,
             # and (a) is what everybody who has not met it will pick.
             MCQ(r"Cell C2 of a Calc sheet contains \texttt{=A2*B2}. You copy "
                 r"C2 and paste it into C3. What does C3 now contain?", [
                     r"\texttt{=A2*B2}",
                     r"\texttt{=A3*B3}",
                     r"\texttt{=A2*B3}",
                     r"\texttt{=C2*C2}",
                 ], answer="b"),
             # // and % with a multiplication in the middle, so precedence
             # decides it: 7 % 2 + 7 // 2 * 2 = 1 + (3 * 2) = 7. (b) is what a
             # strict left-to-right reading gives.
             MCQ(r"What is the value of \texttt{7 \% 2 + 7 // 2 * 2}?", [
                 "7",
                 "8",
                 "6",
                 "4",
             ], answer="a"),
             # the absorption law -- the first Boolean identity that cannot be
             # seen by staring at it. Every option is a term that appears in the
             # expression, so guessing gains nothing.
             MCQ("What does $%s$ simplify to?" % expr_latex(parse("A | (A & B)")), [
                 "$A$",
                 "$B$",
                 "$%s$" % expr_latex(parse("A & B")),
                 "$%s$" % expr_latex(parse("A | B")),
             ], answer="a"),
             # a real file-size sum: 100 x 100 = 10000 pixels, one byte each,
             # so about 10 KB. Two steps (area, then bytes -> KB) for one mark.
             MCQ("A picture is 100 pixels wide and 100 pixels tall, and stores "
                 "one byte for each pixel. About how big is the file?", [
                     "100 bytes",
                     "1 KB",
                     "10 KB",
                     "100 KB",
                 ], answer="c"),
             # redo, not undo: the shortcut students have to reach for after
             # they have already learnt Ctrl + Z
             MCQ("You press Ctrl + Z once too often. Which shortcut brings "
                 "back the change you have just undone?", [
                     r"Ctrl + Y",
                     r"Ctrl + Z",
                     r"Ctrl + R",
                     r"Ctrl + B",
                 ], answer="a"),
         ]),

    PART("Part B", "Boolean Algebra",
         questions=[
             # two THREE-variable product terms (the real paper pairs a
             # three-variable term with a two-variable one), so the output
             # column is 1 in exactly two of the eight rows -- a student who
             # loses a bar gets a table that is wrong everywhere
             BOOL(parse("(a & ~b & ~c) | (~a & b & c)"), 3, ask="truthtable",
                  cases=[{"A": 1, "B": 0, "C": 0}, {"A": 0, "B": 1, "C": 1}]),
             # the bar sits over a whole bracket that itself contains a
             # bracket, so the circuit is built from the inside out: OR, then
             # AND, then the inverter last
             BOOL(parse("~((a | b) & c)"), 3, ask="circuit"),
         ]),

    PART("Part C", "Short Answer Questions",
         questions=[
             # one gate of each kind again (OR, NOT, AND) -- circuit only, but
             # with the inversion over the bracket rather than a variable
             BOOL(parse("~(a | b) & c"), 1, ask="circuit", with_table=False),
             # eight cells spanning four columns and two rows: wider than the
             # square blocks asked for before, so the address cannot be read
             # off by counting one step in each direction
             SHEET("B3:E4", marks=1),
             SHORT(r"What is the keyboard shortcut for printing a document in "
                   r"LibreOffice Writer?", marks=1),
             # bytes -> bits with a count in front of it: 1000 samples x 2
             # bytes x 8 = 16000 bits. Two multiplications, and the units have
             # to be kept straight, so the bold words mark the trap.
             SHORT("A sound recording stores 1000 samples, and each sample "
                   "uses 2 \\textbf{bytes}. How many \\textbf{bits} is the "
                   "whole recording?", marks=1),
             # // and % multiplied together, so both operators must be right
             # AND both must be worked out: (23 % 5) x (23 // 5) = 3 x 4 = 12.
             # Swapping the operators gives 20, which is on nobody's list of
             # suspicious answers -- the student has to know the difference.
             SHORT(r"What is the value of \texttt{(23 \% 5) * (23 // 5)}?",
                   marks=1),
             # software, asked about the piece of it students never see running
             MCQ("Which of the following turns a program written by a "
                 "programmer into the machine code a computer can run?", [
                     "A compiler",
                     "An operating system",
                     "A spreadsheet program",
                     "A web browser",
                 ], answer="a"),
             # A sales sheet with the SAME item appearing on three rows, and
             # two formulas: the biggest single sale, and the total for one
             # named item. The second is SUMIF's three-argument form -- test one
             # column, add another -- which is a step past the real paper's
             # ">200" on a single column.
             #
             # The numbers are chosen so the two answers differ and both are
             # round: the three Pen rows come to 400 and the largest single
             # sale is Bag at 450, so an answer of 400 for both means the
             # criterion was ignored.
             CALC(("Item", "Sales"),
                  [("Pen", 120),
                   ("Book", 300),
                   ("Pen", 180),
                   ("Bag", 450),
                   ("Book", 250),
                   ("Pen", 100)],
                  asks=[("B8", "=MAX(B2:B7)"),
                        ("B9", '=SUMIF(A2:A7,"Pen",B2:B7)')],
                  extra_rows=2,
                  marks=2),
         ]),

    PART("Part D", "Number Systems",
         questions=[
             # hex -> decimal, with a letter digit in the middle:
             # 3C7 = 3x256 + 12x16 + 7 = 967. Two marks, and the place values
             # have to be written down rather than counted on fingers.
             SHORT(r"Convert the hexadecimal number $\mathrm{3C7}_{16}$ to "
                   r"decimal.", marks=2),
             # binary ARITHMETIC rather than a conversion: 101101 + 11011
             # (45 + 27 = 72 = 1001000). The carries run through four columns
             # in a row, and the answer is one bit longer than either input.
             SHORT(r"Add the binary numbers $\mathrm{101101}_2$ and "
                   r"$\mathrm{11011}_2$. Give your answer in binary.", marks=3),
         ]),

    PART("Part E", "Flowcharts and Algorithms",
         questions=[
             TRACE(flowgen.TRACE(
                 to_binary, {"n": 45},
                 reveal=("The numbers this program prints are the binary digits "
                         "of $45_{10}$ --- but printed in reverse order, least "
                         "significant bit first.")),
                 marks=5),
             TRACE(flowgen.TRACE(peasant, {"a": 13, "b": 11}), marks=4),
             DEBUG(odd_even,
                   [flowgen.swap_branches("x % 2 == 0"),
                    flowgen.move_into_loop("print even")],
                   cases=[{"n": 5, "x": [4, 7, 2, 9, 6]}],
                   description=("The program should read how many numbers "
                                "there are, then read that many numbers, and "
                                "finally print how many of them are even and "
                                "then how many are odd --- one number each."),
                   marks=2),
             DEBUG(largest,
                   [flowgen.wrong_assign("largest", "-9999", "0")],
                   cases=[{"n": 4, "x": [3, 7, 2, 5]},
                          {"n": 4, "x": [-5, -2, -9, -1]}],
                   description=("The program should read how many numbers "
                                "there are, then read that many numbers, and "
                                "print the largest of them. The numbers may be "
                                "negative."),
                   note=("The program gives the right answer on one of these "
                         "test runs and the wrong answer on the other. Say "
                         "which box is wrong, what it should say, and why the "
                         "mistake does not show on both runs."),
                   marks=2),
             DRAW(flowgen.DRAW(
                 digit_sum,
                 description=(r"A program reads a whole number n and prints "
                              r"the sum of its digits. For example, if n is "
                              r"302 the program prints 5, because "
                              r"$3 + 0 + 2 = 5$. "
                              r"(Hint: \texttt{n \% 10} is the last digit of n, "
                              r"and \texttt{n // 10} is n with that digit "
                              r"removed.)"),
                 predict=[{"n": 4728}, {"n": 999}]),
                 marks=7),
             DRAW(flowgen.DRAW(
                 wages,
                 description=(r"A factory works out a worker's weekly pay. The "
                              r"program reads the number of hours worked. Every "
                              r"hour is paid at Rs 50. If more than 40 hours "
                              r"were worked, each hour \emph{above} 40 is paid "
                              r"a second time over, at another Rs 50 an hour. "
                              r"The program then prints the total pay.")),
                 marks=3),
         ]),
]
