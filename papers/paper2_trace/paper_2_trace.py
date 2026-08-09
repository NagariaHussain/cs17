"""Quick test: trace a small Scratch script and predict its output.

One short script with a loop, an if/else and two variables — small enough to
hand out on its own, but with enough logic that a student who only skims the
blocks gets it wrong.

The loop's numbers are authored once as constants and used by BOTH the Scratch
script and the Python run below, so the blocks the student sees and the trace
table on the answer key are driven by the same values. `_run()` produces the
trace by actually executing the loop, so the key's table and final answer are
computed, never typed.
"""

from gens.papergen import Paper, Section, Question, Part
from gens.scratchgen import (
    script, when_flag, repeat, ifelse, say,
    set_var, change_var, var, gt,
)

# ---- the one source of truth for the loop -------------------------------------

START = 1          # N starts here
TIMES = 5          # the repeat count
THRESHOLD = 2      # the if test: N > THRESHOLD
ELSE_ADD = 1       # what the else branch adds instead


def _run() -> tuple:
    """Execute the same loop the blocks describe. Returns (rows, total, n),
    where each row is one pass: (pass number, N at the start of the pass,
    whether the test held, Total after the pass)."""
    total, n, rows = 0, START, []
    for i in range(1, TIMES + 1):
        hit = n > THRESHOLD
        total += n if hit else ELSE_ADD
        rows.append((i, n, hit, total))
        n += 1
    return rows, total, n


ROWS, FINAL_TOTAL, FINAL_N = _run()
ELSE_RUNS = sum(1 for _, _, hit, _ in ROWS if not hit)

# ---- the script the student is given ------------------------------------------

trace_script = script(
    when_flag(),
    set_var("Total", 0),
    set_var("N", START),
    repeat(
        TIMES,
        ifelse(
            gt(var("N"), THRESHOLD),
            [change_var("Total", var("N"))],
            [change_var("Total", ELSE_ADD)],
        ),
        change_var("N", 1),
    ),
    say(var("Total")),
)


def _trace_table() -> str:
    """The pass-by-pass trace, derived from `_run()`."""
    body = "\n".join(
        r"%d & %d & %s & %d \\" % (i, n, "Yes" if hit else "No", total)
        for i, n, hit, total in ROWS)
    return (r"\par\vspace{4pt}\begin{center}"
            r"\begin{tabular}{@{}c c c c@{}}\hline"
            r"\textbf{Pass} & \textbf{N at start} & "
            r"\textbf{Is N $>$ %d ?} & \textbf{Total after} \\ \hline "
            % THRESHOLD
            + body +
            r"\hline\end{tabular}\end{center}"
            r"\par\vspace{4pt}After the last pass \blk{change N by 1} runs once "
            r"more, so N finishes at \textbf{%d}, not %d." % (FINAL_N, TIMES))


PAPER = Paper(
    title="Scratch Quick Test - Trace the Script",
    duration="10 minutes",
    max_marks=4,
    # No instructions box: on a 4-mark hand-out it costs more page than it earns,
    # and the one thing worth saying fits in the question's own intro.
    instructions=(),
    # one unnamed section: a single-question hand-out needs no section band
    sections=(Section(
        name="",
        questions=(Question(
            number=1,
            title="Predict the output",
            intro=r"The \blk{Total} and \blk{N} variables have already been created. "
                  r"Work through the script below \textbf{one block at a time} and "
                  r"answer the questions under it. Do not run it in Scratch - the "
                  r"point is to predict what it will do. Keeping a rough trace table "
                  r"in the margin is the easiest way to track the variables.",
            given=(trace_script,),
            parts=(
                Part(
                    label="(a)", title="The output", marks=2,
                    text=r"What number does the script \textbf{say} when it "
                         r"finishes?",
                    answer=r"It says \textbf{%d}." % FINAL_TOTAL,
                    answer_note=r"\textbf{2 marks} for %d. Award \textbf{1 mark} for "
                                r"a correct method with one arithmetic slip. The "
                                r"common wrong answer is %d - that is what you get by "
                                r"adding every N and ignoring the else branch."
                                % (FINAL_TOTAL, sum(n for _, n, _, _ in ROWS)),
                ),
                Part(
                    label="(b)", title="The counter", marks=1,
                    text=r"What is the value of \blk{N} when the script finishes?",
                    answer=r"\textbf{%d}." % FINAL_N,
                    answer_note=r"The usual wrong answer is %d. \blk{change N by 1} "
                                r"is the last block inside the loop, so it also runs "
                                r"on the final pass - N is left one past the last "
                                r"value it was tested with." % TIMES,
                ),
                Part(
                    label="(c)", title="The else branch", marks=1,
                    text=r"How many times does the \textbf{else} branch run?",
                    answer=r"\textbf{%d} times (on the passes where N is %s)."
                           % (ELSE_RUNS,
                              " and ".join(str(n) for _, n, hit, _ in ROWS if not hit)),
                    answer_note=r"The full trace:" + _trace_table(),
                ),
            ),
        ),),
    ),),
).check()
