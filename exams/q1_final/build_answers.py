"""Step-by-step answer key for the Q1 Final Theory paper.

examgen deliberately emits no answer key, so this builds one beside it.

Two rules keep the key honest:

1. **Numbering and marks come from the paper**, not from here — this walks
   `theory.PARTS` in order, so a question inserted into the paper renumbers the
   key too, and a question with no worked solution here fails the build instead
   of quietly going missing.
2. **Every computed value is computed.** Traces, outputs and the buggy-vs-correct
   tables are produced by running the paper's own `flowgen` algorithms; truth
   tables come from its `boolgen` expressions. The prose reasoning is authored;
   the numbers are not.

    python exams/q1_final/build_answers.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from gens import flowgen, wsbase                                    # noqa: E402
from gens.boolgen import parse                                      # noqa: E402
from gens.boolgen.expr import truth_table                           # noqa: E402
from gens.flowgen.bug import apply_bug                              # noqa: E402


def _load(path):
    spec = importlib.util.spec_from_file_location("theory", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"not an importable paper module: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = _load(HERE / "theory.py")


def outputs(algo, inputs):
    """What the algorithm prints, run for real."""
    return flowgen.run(algo, inputs)[2]


# ---- derived tables -----------------------------------------------------------

def _tab(colspec, header, rows, note=""):
    body = "\n".join(" & ".join(str(c) for c in r) + r" \\" for r in rows)
    out = (r"\par\vspace{4pt}\begin{center}\small"
           r"\begin{tabular}{%s}\hline " % colspec
           + " & ".join(r"\textbf{%s}" % h for h in header) + r" \\ \hline "
           + body + r"\hline\end{tabular}\end{center}")
    return out + (r"\par\vspace{2pt}%s" % note if note else "")


def merge_trace():
    """Q20: walk the two lists exactly as the flowchart does, then check the
    printed sequence against a real run of the algorithm."""
    A, B = (2, 5, 9), (3, 6, 8)
    i = j = 0
    rows, printed = [], []
    while i < 3 and j < 3:
        if A[i] < B[j]:
            rows.append((i, j, f"{A[i]} < {B[j]} ? Yes", f"print {A[i]}", "i"))
            printed.append(A[i]); i += 1
        else:
            rows.append((i, j, f"{A[i]} < {B[j]} ? No", f"print {B[j]}", "j"))
            printed.append(B[j]); j += 1
    while i < 3:
        rows.append((i, j, "second loop", f"print {A[i]}", "i"))
        printed.append(A[i]); i += 1
    while j < 3:
        rows.append((i, j, "third loop", f"print {B[j]}", "j"))
        printed.append(B[j]); j += 1
    assert printed == outputs(T.merge, {"A": A, "B": B}), "trace disagrees with run"
    return printed, _tab("c c l l c", ("i", "j", "Test", "Output", "then add 1 to"),
                         rows)


def babylonian_trace():
    """Q21: each pass of x = (x + n // x) // 2, with the division shown."""
    n = 1000
    x = n // 2
    rows = [("start", r"$x = 1000 \div 2$", x)]
    for p in range(1, 7):
        q = n // x
        nx = (x + q) // 2
        rows.append((p, r"$(%d + %d) \div 2 = %d \div 2$" % (x, q, x + q), nx))
        x = nx
    assert [x] == outputs(T.babylonian, {"n": n}), "trace disagrees with run"
    return x, _tab("c l c", ("Pass", "New x = (x + 1000 // x) // 2", "x"), rows)


def smallest_tables():
    """Q22: what the correct chart prints vs what the two-bug chart prints."""
    case = {"n": 5, "x": [30, 25, 15, 20, 10]}
    good = outputs(T.smallest, case)
    buggy = T.smallest
    for bug in (flowgen.wrong_cond("i <= n", "i < n"),
                flowgen.move_into_loop("print smallest")):
        buggy, _ = apply_bug(buggy, bug)
    bad = outputs(buggy, case)
    rows = [("30, 25, 15, 20, 10", ", ".join(map(str, good)),
             ", ".join(map(str, bad)))]
    return good, bad, _tab("l c c", ("Numbers read", "Should print",
                                     "Actually prints"), rows)


def average_tables():
    """Q23: the one planted bug, shown on both input sets."""
    buggy, _ = apply_bug(T.average,
                         flowgen.wrong_assign("avg", "total // n", "total // i"))
    rows = []
    for case in ({"n": 4, "x": [10, 20, 30, 40]},
                 {"n": 5, "x": [20, 30, 10, 40, 20]}):
        nums = ", ".join(map(str, case["x"]))
        tot, n = sum(case["x"]), case["n"]
        rows.append((nums, f"{tot} / {n} = {outputs(T.average, case)[0]}",
                     f"{tot} / {n + 1} = {outputs(buggy, case)[0]}"))
    return _tab("l c c", ("Numbers read", "Should print", "Actually prints"), rows)


def factorial_predictions():
    return [(n, outputs(T.factorial, {"n": n})[0]) for n in (5, 6)]


def truthtable(src, varnames):
    """A full truth table for one authored expression."""
    _, rows = truth_table(parse(src))
    return _tab("c c c c", tuple(varnames) + ("Y",),
                [tuple(vals) + (int(y),) for vals, y in rows])


MERGE_OUT, MERGE_TAB = merge_trace()
BABY_OUT, BABY_TAB = babylonian_trace()
SMALL_GOOD, SMALL_BAD, SMALL_TAB = smallest_tables()
AVG_TAB = average_tables()
FACT = factorial_predictions()

# ---- the worked solutions, keyed by question number ---------------------------
# `a` is the answer itself; `w` is the working that earns it.

S = {
 1: dict(a=r"\textbf{(b)} Dynamic Host Configuration Protocol",
         w=r"DHCP is the protocol that hands out IP addresses automatically when "
           r"a device joins a network, instead of someone typing one in by hand. "
           r"The other three options are invented names."),
 2: dict(a=r"\textbf{(b)} \texttt{Ctrl + C}, then \texttt{Ctrl + V}",
         w=r"\texttt{Ctrl + C} copies (the original stays), \texttt{Ctrl + V} "
           r"pastes. Option (a) starts with \texttt{Ctrl + X}, which \emph{cuts} "
           r"-- the original is removed, so that is move, not copy. "
           r"\texttt{Ctrl + P} is print and \texttt{Ctrl + S} is save."),
 3: dict(a=r"\textbf{(c)} \texttt{172.16.300.5}",
         w=r"An IPv4 address is four numbers, each stored in one byte, so each "
           r"one must be in the range \textbf{0 to 255}. In (c) the third number "
           r"is \textbf{300}, which is bigger than 255, so it cannot be stored. "
           r"\par\vspace{2pt}Note (b) \texttt{10.0.0.255} \emph{is} valid -- 255 "
           r"is a legal value for a byte. Rejecting it is the common mistake."),
 4: dict(a=r"\textbf{(b)} $\overline{A} \cdot \overline{B}$",
         w=r"Read the circuit: A and B go into an \textbf{OR} gate, and the "
           r"result goes into a \textbf{NOT} gate. So "
           r"$Y = \overline{A + B}$ (a NOR gate)."
           r"\par\vspace{3pt}Now apply \textbf{De Morgan's law} -- the bar over a "
           r"sum becomes a product of bars:"
           r"\par\vspace{2pt}\qquad $\overline{A + B} = \overline{A} \cdot \overline{B}$"
           r"\par\vspace{3pt}Checking with a truth table, $Y$ is 1 only when both "
           r"inputs are 0:"
           # side-by-side comparison of the two columns, so this one is written
           # out rather than taken from truthtable() (which prints a single Y)
           r"\par\vspace{2pt}\begin{center}\small\begin{tabular}{c c c c}\hline"
           r"\textbf{A} & \textbf{B} & $\overline{A+B}$ & $\overline{A}\cdot\overline{B}$ \\ \hline "
           r"0 & 0 & 1 & 1 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\"
           r"\hline\end{tabular}\end{center}"
           r"The two columns match. Option (a) $\overline{A}+\overline{B}$ is "
           r"the \emph{NAND} (1,1,1,0) -- the classic De Morgan slip of moving "
           r"the bar in without changing the operator."),
 5: dict(a=r"\textbf{(c)} 128",
         w=r"Each bit has 2 possible values, and there are 7 independent bits, "
           r"so the number of different patterns is"
           r"\par\vspace{2pt}\qquad $2^7 = 2\times2\times2\times2\times2\times2\times2 = \textbf{128}$"
           r"\par\vspace{3pt}(a) 7 is the bit \emph{count}, not the number of "
           r"patterns; (b) 64 is $2^6$; (d) 256 is $2^8$ -- that is a whole byte, "
           r"but ASCII uses only 7 of those 8 bits."),
 6: dict(a=r"\textbf{(b)} The text \texttt{A1+A2}",
         w=r"A spreadsheet only treats what you type as a \textbf{formula} if it "
           r"begins with an \textbf{equals sign}. \texttt{A1+A2} has no "
           r"\texttt{=}, so Calc has nothing to calculate and stores it as "
           r"ordinary text. Typing \texttt{=A1+A2} would give the sum."),
 7: dict(a=r"\textbf{(c)} \texttt{.zip}",
         w=r"A \texttt{.zip} file is an \emph{archive}: it holds many files "
           r"inside one file, so all 50 travel as a single attachment (and "
           r"compressed, so it is smaller too). \texttt{.png} and \texttt{.jpg} "
           r"are single images and \texttt{.txt} is a single text file -- none of "
           r"them can contain other files."),
 8: dict(a=r"\textbf{(c)} 0",
         w=r"$\overline{A}$ is always the opposite of $A$, so the two can never "
           r"be 1 at the same time, and AND needs \emph{both} inputs to be 1:"
           r"\par\vspace{2pt}\qquad if $A = 0$: $0 \cdot \overline{0} = 0 \cdot 1 = 0$"
           r"\par\qquad if $A = 1$: $1 \cdot \overline{1} = 1 \cdot 0 = 0$"
           r"\par\vspace{3pt}Either way the answer is \textbf{0}. This is the "
           r"\textbf{complement law}, $A \cdot \overline{A} = 0$."),

 9: dict(a=r"See the circuit below.",
         w=r"Work outwards from the brackets in $Y = (a \cdot b) + \overline{c}$:"
           r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item An \textbf{AND} gate with inputs $a$ and $b$ (gives $a \cdot b$)."
           r"\item A \textbf{NOT} gate on $c$ (gives $\overline{c}$)."
           r"\item An \textbf{OR} gate taking those two outputs, giving $Y$."
           r"\end{enumerate}"
           r"Three gates in total. \textbf{1 mark} for a correct circuit; the "
           r"NOT must sit on $c$ alone, not on the whole expression."),
10: dict(a=r"\texttt{B2:C3}",
         w=r"Read the shaded block off the grid: it starts at the top-left "
           r"shaded cell and ends at the bottom-right one. Top-left is column "
           r"\textbf{B}, row \textbf{2}; bottom-right is column \textbf{C}, row "
           r"\textbf{3}. A range is written \texttt{first:last}, so "
           r"\texttt{B2:C3} (4 cells). Accept lower case."),
11: dict(a=r"\texttt{Ctrl + Z}",
         w=r"\texttt{Ctrl + Z} undoes the last action. (\texttt{Ctrl + Y} redoes "
           r"it.) Accept \texttt{Cmd + Z} on a Mac."),
12: dict(a=r"\textbf{24 bits}",
         w=r"The trap is that the question gives \emph{bytes} and asks for "
           r"\emph{bits}, so two steps are needed:"
           r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item RGB means three colours -- Red, Green, Blue -- so one pixel "
           r"uses \textbf{3 bytes}."
           r"\item 1 byte $=$ 8 bits, so $3 \times 8 = \textbf{24 bits}$."
           r"\end{enumerate}"
           r"Answering ``3'' means missing the unit change."),
13: dict(a=r"\textbf{2}",
         w=r"Two different operators, worked out separately:"
           r"\begin{itemize}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item \texttt{23 // 4} is \emph{whole-number division} -- how many "
           r"whole 4s fit into 23. $4 \times 5 = 20$ and $4 \times 6 = 24$, so it "
           r"is \textbf{5} (the remainder is thrown away)."
           r"\item \texttt{23 \% 4} is the \emph{remainder} after that division: "
           r"$23 - 20 = \textbf{3}$."
           r"\end{itemize}"
           r"Then $5 - 3 = \textbf{2}$."
           r"\par\vspace{2pt}Note the subtraction: swapping the two operators "
           r"gives $3 - 5 = -2$, so a student who mixes them up cannot land on "
           r"the right answer by accident."),
14: dict(a=r"\textbf{(b)} Application software",
         w=r"\textbf{Application} software is written for the \emph{user} to do "
           r"something with -- play, write, draw, calculate. \textbf{System} "
           r"software runs the machine itself. A game is something you use the "
           r"computer \emph{for}, so it is an application."
           r"\par\vspace{2pt}(d) is the trap: an operating system is a kind of "
           r"\emph{system} software, so anyone half-remembering the pair "
           r"``application / system'' can be pulled towards it."),
15: dict(a=r"\texttt{B8} $\rightarrow$ \textbf{1600} \qquad "
           r"\texttt{B9} $\rightarrow$ \textbf{1400}",
         w=r"\texttt{=SUM(B2:B7)} adds every price in the range:"
           r"\par\vspace{2pt}\qquad $40 + 150 + 850 + 250 + 10 + 300 = \textbf{1600}$"
           r"\par\vspace{4pt}\texttt{=SUMIF(B2:B7,\textquotedbl>200\textquotedbl)} "
           r"adds only the prices that are \emph{greater than} 200. Check each "
           r"one: 40 no, 150 no, 850 \textbf{yes}, 250 \textbf{yes}, 10 no, "
           r"300 \textbf{yes}."
           r"\par\vspace{2pt}\qquad $850 + 250 + 300 = \textbf{1400}$"
           r"\par\vspace{3pt}\textbf{1 mark} each. The skill being tested is "
           r"deciding \emph{which} numbers to add, not the adding."),

16: dict(a=r"Truth table below. For the two cases asked: "
           r"$A{=}1, B{=}0, C{=}1 \Rightarrow Y = \textbf{1}$; \quad "
           r"$A{=}1, B{=}1, C{=}0 \Rightarrow Y = \textbf{0}$.",
         w=r"$Y = (A \cdot \overline{B} \cdot C) + (\overline{A} \cdot B)$ is an "
           r"OR of two terms, so $Y = 1$ when \emph{either} term is 1."
           r"\begin{itemize}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item First term $A \cdot \overline{B} \cdot C$ needs $A{=}1$, "
           r"$B{=}0$ and $C{=}1$ all at once -- true on one row only."
           r"\item Second term $\overline{A} \cdot B$ needs $A{=}0$ and $B{=}1$, "
           r"whatever $C$ is -- true on two rows."
           r"\end{itemize}"
           r"So exactly 3 of the 8 rows give 1. Build the table with A, B, C "
           r"counting up in binary 000 to 111 so no row is missed:"
           + truthtable("(a & ~b & c) | (~a & b)", ("A", "B", "C"))
           + r"Checking the two asked cases against it: row $A{=}1, B{=}0, C{=}1$ "
             r"is the first term satisfied, so $Y = 1$; row $A{=}1, B{=}1, C{=}0$ "
             r"fails both terms ($B$ is 1 so the first dies, $A$ is 1 so the "
             r"second dies), so $Y = 0$."
             r"\par\vspace{3pt}\textbf{3 marks:} 1 for the 8 input rows in order, "
             r"2 for the output column (or 1 if only one or two rows are wrong)."),
17: dict(a=r"See the circuit below.",
         w=r"$Y = (a + b) \cdot \overline{c}$. Brackets first, so the OR happens "
           r"before the AND:"
           r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item An \textbf{OR} gate with inputs $a$ and $b$ $\rightarrow a + b$."
           r"\item A \textbf{NOT} gate on $c$ $\rightarrow \overline{c}$."
           r"\item An \textbf{AND} gate taking those two $\rightarrow Y$."
           r"\end{enumerate}"
           r"\textbf{3 marks:} 1 per gate, correctly connected. The commonest "
           r"error is feeding $c$ straight into the AND and putting the NOT at "
           r"the end, which draws $\overline{(a+b) \cdot c}$ instead."
           + truthtable("(a | b) & ~c", ("a", "b", "c"))
           + r"(Truth table given for checking -- it was not asked for.)"),

18: dict(a=r"$1011010_2 = \textbf{90}_{10}$",
         w=r"Write the place values above the bits, doubling from the right, then "
           r"add the ones with a 1 under them:"
           r"\par\vspace{3pt}\begin{center}\small"
           r"\begin{tabular}{c c c c c c c}\hline"
           r"\textbf{64} & \textbf{32} & \textbf{16} & \textbf{8} & \textbf{4} & "
           r"\textbf{2} & \textbf{1} \\ \hline "
           r"1 & 0 & 1 & 1 & 0 & 1 & 0 \\ \hline\end{tabular}\end{center}"
           r"\par\vspace{2pt}\qquad $64 + 16 + 8 + 2 = \textbf{90}$"
           r"\par\vspace{3pt}\textbf{2 marks:} 1 for correct place values, 1 for "
           r"the total. A 7-bit number, so the leftmost place is $2^6 = 64$."),
19: dict(a=r"$2AF_{16} = \textbf{1010101111}_2$",
         w=r"Hexadecimal is base 16 and $16 = 2^4$, so \textbf{each hex digit is "
           r"exactly 4 bits}. Convert them one at a time -- there is no need to go "
           r"through decimal:"
           r"\par\vspace{3pt}\begin{center}\small"
           r"\begin{tabular}{c c c}\hline"
           r"\textbf{Hex digit} & \textbf{Decimal} & \textbf{4 bits} \\ \hline "
           r"2 & 2 & 0010 \\ A & 10 & 1010 \\ F & 15 & 1111 \\"
           r"\hline\end{tabular}\end{center}"
           r"Join them in the same order:"
           r"\par\vspace{2pt}\qquad $0010\ 1010\ 1111$"
           r"\par\vspace{2pt}Leading zeros may be dropped, giving "
           r"$\textbf{1010101111}_2$ (both forms accepted)."
           r"\par\vspace{3pt}\emph{Check:} $2 \times 256 + 10 \times 16 + 15 = "
           r"512 + 160 + 15 = 687$, and $1010101111_2 = 512+128+32+8+4+2+1 = 687$. "
           r"\checkmark"
           r"\par\vspace{3pt}\textbf{3 marks:} 1 per digit converted correctly, "
           r"provided they are joined in order."),

20: dict(a=r"The program prints \textbf{%s}." % ", ".join(map(str, MERGE_OUT)),
         w=r"Both lists are already in order. The first loop compares the front "
           r"item of each list and prints the smaller one, then steps only "
           r"\emph{that} list forward. $A = (2, 5, 9)$ and $B = (3, 6, 8)$, "
           r"counting from $i = 0$ and $j = 0$:"
           + MERGE_TAB
           + r"After the first loop $j$ has reached 3 (list B is used up), so the "
             r"second loop prints what is left of A -- just the 9. The third loop "
             r"runs zero times."
             r"\par\vspace{3pt}\emph{What it does:} it merges two sorted lists "
             r"into one sorted list -- the output %s is in order. This is the "
             r"merge step of merge sort."
             r"\par\vspace{3pt}\textbf{5 marks:} 3 for the i/j columns tracked "
             r"correctly, 2 for the output in the right order."
             % ", ".join(map(str, MERGE_OUT))),
21: dict(a=r"The program prints \textbf{%d}." % BABY_OUT,
         w=r"$x$ starts at $n \div 2$ and is then replaced six times by the "
           r"average of $x$ and $n \div x$. \textbf{Every division here is "
           r"whole-number division} -- throw the remainder away each time:"
           + BABY_TAB
           + r"After 6 passes the loop test $i \le 6$ fails and $x = %d$ is "
             r"printed."
             r"\par\vspace{3pt}\emph{What it does:} it closes in on the square "
             r"root of $n$. $\sqrt{1000} = 31.6\ldots$, and the whole-number "
             r"answer is 31 -- reached by pass 6 and stable after that."
             r"\par\vspace{3pt}\textbf{4 marks:} 3 for the six values of $x$ in "
             r"order, 1 for the printed answer. Losing the remainder at any step "
             r"derails everything after it, so mark the first wrong row and "
             r"follow through." % BABY_OUT),
22: dict(a=r"\textbf{Two} boxes are wrong: the loop test, and the position of "
           r"the print box.",
         w=r"Run the chart on the given numbers and compare:"
           + SMALL_TAB
           + r"Two separate symptoms, so two separate faults."
             r"\par\vspace{4pt}\textbf{Bug 1 -- the loop stops one number early.}"
             r"\par The test reads \texttt{i < n}, so with $n = 5$ the loop body "
             r"runs for $i = 1, 2, 3, 4$ only: the fifth number (10) is never "
             r"read. That is why the smallest found is 15 and not 10. "
             r"\textbf{Fix:} change the test to \texttt{i <= n}."
             r"\par\vspace{4pt}\textbf{Bug 2 -- the print box is inside the loop.}"
             r"\par ``Print smallest'' sits within the loop, so it runs on every "
             r"pass and the program prints four times (30, 25, 15, 15) instead of "
             r"once. \textbf{Fix:} move the print box \emph{after} the loop."
             r"\par\vspace{4pt}With both fixed the program prints \textbf{%s}, "
             r"once."
             r"\par\vspace{3pt}\textbf{2 marks:} 1 per bug -- the mark needs both "
             r"the box named \emph{and} the correction. Naming only the symptom "
             r"(``it prints too many times'') scores 0."
             % ", ".join(map(str, SMALL_GOOD))),
23: dict(a=r"One box is wrong: \texttt{avg = total // i} should be "
           r"\texttt{avg = total // n}.",
         w=r"Nothing in this chart \emph{looks} wrong, so trace it:"
           + AVG_TAB
           + r"Both sets print 20, and both are too low -- so the totals are "
             r"right and the division is not."
             r"\par\vspace{4pt}\textbf{Why.} The loop ends when the test "
             r"\texttt{i <= n} \emph{fails}, which means $i$ has already passed "
             r"$n$: after reading 4 numbers, $i$ is \textbf{5}, not 4. The divide "
             r"box uses $i$, so the total is shared among one person too many:"
             r"\par\vspace{2pt}\qquad $100 \div 5 = 20$ \quad instead of \quad "
             r"$100 \div 4 = 25$"
             r"\par\vspace{4pt}\textbf{Fix:} divide by \texttt{n} -- the count "
             r"that was read in -- not by the loop counter \texttt{i}."
             r"\par\vspace{3pt}\textbf{2 marks:} 1 for identifying the divide "
             r"box, 1 for the correction. This is the off-by-one that a student "
             r"can only find by tracing, so credit a correct trace that reaches "
             r"the box even if the wording of the fix is loose."),
24: dict(a=r"Flowchart below; it prints \textbf{%d} for $n = 5$ and \textbf{%d} "
           r"for $n = 6$." % (FACT[0][1], FACT[1][1]),
         w=r"\textbf{The flowchart} (7 marks: 5 for the chart, 2 for the two "
           r"predictions). A correct chart needs, in order:"
           r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item \textbf{Start} (oval)."
           r"\item \textbf{Read} $n$ (parallelogram)."
           r"\item Set $f = 1$ and $i = 1$ (process). \emph{$f$ must start at 1, "
           r"not 0 -- anything times 0 stays 0.}"
           r"\item A \textbf{decision} $i \le n$ (diamond)."
           r"\item On \textbf{Yes}: $f = f \times i$, then $i = i + 1$, then an "
           r"arrow \emph{back} to the decision."
           r"\item On \textbf{No}: \textbf{print} $f$ (parallelogram), then "
           r"\textbf{Stop} (oval)."
           r"\end{enumerate}"
           r"Marks are for the loop-back arrow and the counter update as much as "
           r"the boxes -- without $i = i + 1$ the loop never ends."
           r"\par\vspace{4pt}\textbf{The predictions.} Trace the multiplication:"
           r"\par\vspace{2pt}\qquad $n = 5$: $1 \times 1 \times 2 \times 3 \times "
           r"4 \times 5 = \textbf{%d}$"
           r"\par\qquad $n = 6$: $\textbf{%d} \times 6 = \textbf{%d}$"
           r"\par\vspace{2pt}The second follows from the first -- a student who "
           r"multiplies out again from scratch is not wrong, just slower."
           % (FACT[0][1], FACT[0][1], FACT[1][1])),
25: dict(a=r"Flowchart below.",
         w=r"Read the wording one sentence at a time; each becomes a box."
           r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
           r"\item \textbf{Start} (oval)."
           r"\item \textbf{Read} price, \textbf{read} quantity (parallelograms, "
           r"or one box reading both)."
           r"\item $total = price \times quantity$ (process)."
           r"\item A \textbf{decision}: $total > 1000$? (diamond)."
           r"\item On \textbf{Yes}: $total = total - (total \times 10 \div 100)$ "
           r"-- a 10\% discount. Equivalent forms such as $total = total \times "
           r"0.9$ are fully correct."
           r"\item On \textbf{No}: nothing -- the arrow joins straight back."
           r"\item \textbf{Print} total, then \textbf{Stop}."
           r"\end{enumerate}"
           r"\textbf{3 marks:} 1 for reading the inputs and computing the total, "
           r"1 for a correctly shaped decision with both branches rejoining, "
           r"1 for the discount arithmetic and the print."
           r"\par\vspace{3pt}\textbf{Note:} there is \emph{no loop} in this one. "
           r"The commonest error is discounting on the No branch as well, which "
           r"gives every customer 10\% off."),
}


# ---- assembly -----------------------------------------------------------------

_PRE = wsbase.preamble(r"""\usepackage{enumitem}
\usepackage{amssymb}
\setlist[enumerate]{leftmargin=*,topsep=3pt,itemsep=3pt}
\setlist[itemize]{leftmargin=*,topsep=3pt,itemsep=3pt}
\newcommand{\qhead}[2]{\par\vspace{11pt}\noindent\textbf{#1}%
  \hfill\textnormal{\bfseries[#2]}\par\vspace{3pt}}
\newcommand{\partband}[1]{\par\vspace{8pt}\noindent\colorbox{gray!15}{%
  \begin{minipage}{\dimexpr\linewidth-2\fboxsep}\vspace{2pt}\centering\bfseries #1%
  \vspace{2pt}\end{minipage}}\par\vspace{10pt}}
\setlength{\emergencystretch}{5em}
""")


def build():
    body = [_PRE, r"\begin{document}",
            r"\wstitle{%s --- Answer Key}" % T.SUBJECT,
            r"\textit{%s, %s. %d marks, %s. Teacher's copy --- worked solutions "
            r"and marking notes.}\par\vspace{4pt}"
            % (T.TITLE, T.DATE, T.MAX_MARKS, T.DURATION),
            r"{\color{gray!60}\hrule height 0.4pt}\par\vspace{10pt}"]

    n = 0
    missing, total = [], 0
    for part in T.PARTS:
        marks = sum(q.marks or 0 for q in part.questions)
        total += marks
        body.append(r"\partband{%s --- %s\hfill %d marks}"
                    % (part.name, part.title, marks))
        for q in part.questions:
            n += 1
            if n not in S:
                missing.append(n)
                continue
            body.append(r"\qhead{Q%d}{%d}" % (n, q.marks or 0))
            body.append(r"\noindent\textbf{Answer.}\quad %s\par\vspace{4pt}" % S[n]["a"])
            body.append(r"\noindent\textbf{Working.}\quad %s\par" % S[n]["w"])

    assert not missing, f"no worked solution for question(s): {missing}"
    assert total == T.MAX_MARKS, f"parts total {total}, paper claims {T.MAX_MARKS}"

    body.append(r"\par\vspace{12pt}\begin{center}\textit{\textcolor{gray}"
                r"{- End of Answer Key -}}\end{center}")
    body.append(r"\end{document}")

    out = HERE / "build" / "theory_answers"
    out.mkdir(parents=True, exist_ok=True)
    tex = out / "theory_answers.tex"
    # explicit encoding: the worked solutions carry non-ASCII, which a non-UTF-8
    # locale would refuse to write
    tex.write_text("\n".join(body), encoding="utf-8")
    print(f"{n} questions, {total} marks -> {tex}")
    wsbase.compile_tex(tex)
    print(f"compiled {tex.with_suffix('.pdf')}")


if __name__ == "__main__":
    build()
