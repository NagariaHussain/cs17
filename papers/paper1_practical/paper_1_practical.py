"""Practical paper 1 — GreenLeaf Organics (Calc) + Apple Catcher (Scratch).

Section A is authored as a `Workbook`: the two tables the student is given and
every figure on the answer key come from the same 8 products and 15 orders, so
changing a price or a quantity re-derives the lot. Section B's model solution is
authored as scratchgen scripts, rendered as real Scratch blocks on the key only.
"""

from gens.papergen import (
    Paper, Section, Question, Part, SheetTable,
    Product, Sale, Workbook, rupees, plain, fx,
)
from gens.scratchgen import (
    script, when_flag, when_receive, goto_xy, setx, sety, changex, changey,
    show, hide, say, wait, forever, if_, repeat_until, stop_all, broadcast,
    play_sound, set_var, change_var, show_var, var,
    x_position, y_position, touching, key_pressed,
    pick_random, join, gt, lt, eq,
)

# ---- Section A: the data, authored once ---------------------------------------

PRODUCTS = [
    Product("P001", "Green Tea Pack",     "Beverages",     250),
    Product("P002", "Cold Pressed Juice", "Beverages",     180),
    Product("P003", "Organic Honey",      "Grocery",       450),
    Product("P004", "Almond Butter",      "Grocery",       620),
    Product("P005", "Herbal Shampoo",     "Personal Care", 320),
    Product("P006", "Aloe Face Wash",     "Personal Care", 210),
    Product("P007", "Quinoa 1 kg",        "Grocery",       540),
    Product("P008", "Ginger Ale",         "Beverages",     150),
]

SALES = [
    Sale("S01", "05-01-2026", "P001", "North", 12),
    Sale("S02", "07-01-2026", "P003", "South",  8),
    Sale("S03", "09-01-2026", "P002", "North", 20),
    Sale("S04", "11-01-2026", "P005", "East",  15),
    Sale("S05", "14-01-2026", "P004", "West",   6),
    Sale("S06", "16-01-2026", "P001", "South", 10),
    Sale("S07", "18-01-2026", "P006", "North", 25),
    Sale("S08", "21-01-2026", "P007", "East",   9),
    Sale("S09", "23-01-2026", "P008", "North", 30),
    Sale("S10", "25-01-2026", "P003", "West",  14),
    Sale("S11", "28-01-2026", "P002", "South", 18),
    Sale("S12", "30-01-2026", "P005", "North", 11),
    Sale("S13", "02-02-2026", "P007", "South",  7),
    Sale("S14", "04-02-2026", "P004", "East",   5),
    Sale("S15", "06-02-2026", "P006", "West",  22),
]

WB = Workbook(PRODUCTS, SALES,
              regions=["North", "South", "East", "West"],
              categories=["Beverages", "Grocery", "Personal Care"])

FIRST, LAST = WB.first_data_row, WB.last_data_row      # 2 and 16
PLAST = WB.last_product_row                            # 9
TOTAL_ROW, AVG_ROW, MAX_ROW = LAST + 2, LAST + 3, LAST + 4   # I18 / I19 / I20

# ---- Section A: the two sheets, derived from the data -------------------------

MASTER_TABLE = SheetTable(
    sheet="Product_Master",
    columns=(("A", ("Product Code", "2.1cm")), ("B", ("Product Name", "3.4cm")),
             ("C", ("Category", "2.6cm")), ("D", ("Unit Price", "2.0cm"))),
    rows=tuple((p.code, p.name, p.category, plain(p.price)) for p in PRODUCTS),
)

SALES_TABLE = SheetTable(
    sheet="Sales_Data",
    columns=(("A", ("Order ID", "1.15cm")), ("B", ("Order Date", "1.75cm")),
             ("C", ("Product Code", "1.5cm")), ("D", ("Region", "1.25cm")),
             ("E", ("Qty", "0.75cm")), ("F", ("Product Name", "1.9cm")),
             ("G", ("Category", "1.6cm")), ("H", ("Unit Price", "1.2cm")),
             ("I", ("Total Amount", "1.5cm"))),
    rows=tuple((r.sale.order, r.sale.date, r.sale.code, r.sale.region,
                r.sale.qty, "", "", "", "") for r in WB.rows),
    blank_from="F",
    new_page=True,      # keep the 15-row register whole, under its own heading
    note=r"Columns \textbf{F}, \textbf{G}, \textbf{H} and \textbf{I} are shaded "
         r"because they are to be left \textbf{blank} when you enter the data - "
         r"you will fill them using formulas.",
)

# ---- Section A: the answers, computed -----------------------------------------

_MASTER = f"Product_Master.$A${FIRST}:$A${PLAST}"
_REGION = f"$D${FIRST}:$D${LAST}"
_CATEG = f"$G${FIRST}:$G${LAST}"
_NAME = f"$F${FIRST}:$F${LAST}"
_AMOUNT = f"$I${FIRST}:$I${LAST}"

# Each SUMIFS answer authored once: what the question asks, where it goes, the
# formula, and the value — the value computed with the same criteria as the text.
_SUMIFS = [
    dict(ask=r"Total sales amount of the \textbf{Beverages} category in the "
             r"\textbf{North} region",
         label="Beverages sales in North", kcell="K3", lcell="L3",
         formula=f'=SUMIFS({_AMOUNT},{_CATEG},"Beverages",{_REGION},"North")',
         value=WB.sumifs(category="Beverages", region="North")),
    dict(ask=r"Total sales amount of the \textbf{Grocery} category in the "
             r"\textbf{West} region",
         label="Grocery sales in West", kcell="K4", lcell="L4",
         formula=f'=SUMIFS({_AMOUNT},{_CATEG},"Grocery",{_REGION},"West")',
         value=WB.sumifs(category="Grocery", region="West")),
    dict(ask=r"Total sales amount of orders in the \textbf{East} region where "
             r"Product Name is \textbf{Herbal Shampoo}",
         label="Herbal Shampoo sales in East", kcell="K5", lcell="L5",
         formula=f'=SUMIFS({_AMOUNT},{_REGION},"East",{_NAME},"Herbal Shampoo")',
         value=WB.sumifs(region="East", name="Herbal Shampoo")),
]

TOP_REGION, TOP_AMOUNT = WB.top_region()
PV = WB.pivot()


def _region_rows() -> str:
    """The Region-wise Sales summary as it should end up in K8:L12."""
    rows = "\n".join(r"%s & %s \\" % (reg, rupees(amt))
                     for reg, amt in WB.by_region().items())
    return (r"\par\vspace{4pt}\begin{center}\begin{tabular}{@{}p{3.2cm}r@{}}"
            r"\hline \textbf{Region} & \textbf{Total Sales} \\ \hline "
            + rows + r"\hline\end{tabular}\end{center}")


def _pivot_table() -> str:
    """The expected Pivot_Summary layout, both margins included. Cells with no
    orders are shown blank, which is what a pivot table actually displays."""
    head = " & ".join(r"\textbf{%s}" % c for c in PV.categories)
    body = []
    for reg in PV.regions:
        cells = [rupees(PV.cell(reg, c)) if PV.cell(reg, c) else "-"
                 for c in PV.categories]
        body.append(r"\textbf{%s} & %s & %s \\"
                    % (reg, " & ".join(cells), rupees(PV.row_totals[reg])))
    totals = " & ".join(rupees(PV.col_totals[c]) for c in PV.categories)
    return (r"\par\vspace{4pt}\begin{center}\footnotesize"
            r"\begin{tabular}{@{}l r r r r@{}}\hline"
            r"\textbf{Sum of Total Amount} & " + head + r" & \textbf{Total} \\ \hline "
            + "\n".join(body) +
            r"\hline \textbf{Total} & " + totals + r" & \textbf{%s} \\ \hline"
            % rupees(PV.grand_total) +
            r"\end{tabular}\end{center}")


SECTION_A = Section(
    name="Section A",
    title="Spreadsheet (Calc)",
    scenario=(
        r"\textbf{GreenLeaf Organics Pvt. Ltd.} is a retail chain selling organic "
        r"products across four regions of the country - North, South, East and "
        r"West. The company maintains a product master list (product code, name, "
        r"category and unit price) on one sheet, and a sales register of every "
        r"order received during January--February 2026 on another sheet. However, "
        r"the sales register records \textbf{only the product code} - it does not "
        r"repeat the product name, category or price."
        r"\par\vspace{5pt}"
        r"The Sales Manager has asked you, the data assistant, to complete the "
        r"sales register, calculate the revenue figures, and prepare a summary of "
        r"regional and category-wise performance for the monthly review meeting."
        r"\par\vspace{6pt}"
        r"Create a new spreadsheet with two sheets named exactly "
        r"\sheetname{Product\_Master} and \sheetname{Sales\_Data}, and enter the "
        r"two tables below."),
    tables=(MASTER_TABLE, SALES_TABLE),
    questions=(Question(
        number=1,
        title="Completing and summarising the sales register",
        parts=(
            Part(
                label="(a)", marks=2, title="Looking up the product details",
                text=(r"The sales register stores only the product code. On the sheet "
                      r"\sheetname{Sales\_Data}, use the \textbf{XLOOKUP} function to "
                      r"bring in the missing details from the sheet "
                      r"\sheetname{Product\_Master} for every order in rows %d to %d:"
                      % (FIRST, LAST)),
                items=(r"In column \textbf{F} - the \textbf{Product Name} "
                       r"corresponding to the product code in column C.",
                       r"In column \textbf{G} - the \textbf{Category} of that product.",
                       r"In column \textbf{H} - the \textbf{Unit Price} of that product."),
                note=r"\textbf{Condition:} the formula must be written once in row %d "
                     r"and copied down to row %d." % (FIRST, LAST),
                answer=r"In row %d, then select F%d:H%d and copy down to row %d:" % (
                    FIRST, FIRST, FIRST, LAST),
                answer_items=(
                    fx(f"F{FIRST}  =XLOOKUP($C{FIRST},{_MASTER},Product_Master.$B${FIRST}:$B${PLAST})"),
                    fx(f"G{FIRST}  =XLOOKUP($C{FIRST},{_MASTER},Product_Master.$C${FIRST}:$C${PLAST})"),
                    fx(f"H{FIRST}  =XLOOKUP($C{FIRST},{_MASTER},Product_Master.$D${FIRST}:$D${PLAST})"),
                ),
                answer_note=r"Accept \blk{VLOOKUP} equivalents. The lookup ranges must "
                            r"be absolute (\$) or the formula breaks as it is copied "
                            r"down - \textbf{1 mark} for a correct XLOOKUP, "
                            r"\textbf{1 mark} for all three columns filled to row %d."
                            % LAST,
            ),
            Part(
                label="(b)", marks=2, title="Order amounts and totals",
                items=(r"In column \textbf{I} (Total Amount), write a formula to "
                       r"calculate the amount of each order as "
                       r"\textbf{Quantity $\times$ Unit Price}.",
                       r"In cell \textbf{I%d}, calculate the \textbf{grand total} of "
                       r"all %d orders." % (TOTAL_ROW, len(SALES)),
                       r"In cell \textbf{I%d}, calculate the \textbf{average order "
                       r"value}." % AVG_ROW,
                       r"In cell \textbf{I%d}, display the value of the "
                       r"\textbf{highest single order}." % MAX_ROW),
                note=r"Format the values in column I and in cells I%d:I%d as "
                     r"\textbf{Currency (Rs.)} with \textbf{2 decimal places}."
                     % (TOTAL_ROW, MAX_ROW),
                answer_items=(
                    fx(f"I{FIRST}  =E{FIRST}*H{FIRST}") + r"\quad copied down to row %d" % LAST,
                    fx(f"I{TOTAL_ROW}  =SUM(I{FIRST}:I{LAST})") +
                    r"\quad $\rightarrow$ \textbf{%s}" % rupees(WB.grand_total()),
                    fx(f"I{AVG_ROW}  =AVERAGE(I{FIRST}:I{LAST})") +
                    r"\quad $\rightarrow$ \textbf{%s}" % rupees(WB.average_order()),
                    fx(f"I{MAX_ROW}  =MAX(I{FIRST}:I{LAST})") +
                    r"\quad $\rightarrow$ \textbf{%s} (order %s, %s)"
                    % (rupees(WB.highest_order()), WB.highest_row().sale.order,
                       WB.highest_row().name),
                ),
                answer_note=r"\textbf{1 mark} for the four formulas, \textbf{1 mark} "
                            r"for the currency formatting with 2 decimals. Deduct "
                            r"nothing for \blk{=E2*D2} if the student looked the price "
                            r"up into H correctly in (a).",
            ),
            Part(
                label="(c)", marks=2, title="Category and region figures",
                text=r"Prepare the answers in the cells indicated, using the "
                     r"\textbf{SUMIFS} function only:",
                items=tuple(r"%s - cell \textbf{%s}" % (a["ask"], a["lcell"])
                            for a in _SUMIFS),
                note=r"Enter a suitable label for each value in the corresponding "
                     r"cells - \textbf{K3}, \textbf{K4} and \textbf{K5}.",
                answer_items=tuple(
                    r"%s \quad label in %s, e.g. ``%s'' \par\vspace{2pt}%s"
                    r"\quad $\rightarrow$ \textbf{%s}"
                    % (a["lcell"], a["kcell"], a["label"], fx(a["formula"]),
                       rupees(a["value"]))
                    for a in _SUMIFS),
                answer_note=r"\textbf{2 marks} for all three correct; \textbf{1 mark} "
                            r"for one or two. Note (iii) keys on the \emph{product "
                            r"name} in column F, not the category - a SUMIFS on "
                            r"category here scores 0 for that item.",
            ),
            Part(
                label="(d)", marks=2, title="Region summary and chart",
                items=(r"In the range \textbf{K8:L12}, build a small summary table "
                       r"titled ``Region-wise Sales'', listing the four regions in "
                       r"\textbf{K9:K12} and their total sales amounts in "
                       r"\textbf{L9:L12}. The totals must be calculated using the "
                       r"\textbf{SUMIF} function.",
                       r"Using this summary table, insert a \textbf{column (bar) "
                       r"chart} on the same sheet."),
                note=r"The chart must have - chart title: ``Region-wise Sales - "
                     r"Jan--Feb 2026''; X-axis title: ``Region''; Y-axis title: "
                     r"``Total Sales (Rs.)''; and \textbf{data labels} displayed on "
                     r"each column.",
                answer=r"%s copied down K9:K12, giving:%s"
                       % (fx(f"L9  =SUMIF({_REGION},K9,{_AMOUNT})"), _region_rows()),
                answer_note=r"\textbf{1 mark} for the SUMIF summary table, "
                            r"\textbf{1 mark} for the chart carrying all four "
                            r"required elements (title, both axis titles, data "
                            r"labels). A chart built from a hand-typed table rather "
                            r"than SUMIF scores the chart mark only.",
            ),
            Part(
                label="(e)", marks=2, title="Pivot table summary",
                text=r"Insert a \textbf{pivot table} (Insert $\rightarrow$ Pivot Table) "
                     r"using the "
                     r"range \textbf{A1:I%d} of \sheetname{Sales\_Data} as the source "
                     r"data. Place the pivot table on a \textbf{new sheet} named "
                     r"\sheetname{Pivot\_Summary}, with the following layout:" % LAST,
                items=(r"\textbf{Row fields} - Region",
                       r"\textbf{Column fields} - Category",
                       r"\textbf{Data / Values} - Sum of Total Amount"),
                note=r"The pivot table must display \textbf{row totals} and "
                     r"\textbf{column totals}. Finally, sort the pivot table so that "
                     r"the region with the \textbf{highest} total sales appears "
                     r"first, and state that region's name in a cell below the pivot "
                     r"table.",
                answer=r"The completed \sheetname{Pivot\_Summary}:%s" % _pivot_table(),
                answer_note=r"Sorted by total descending, \textbf{%s} appears first "
                            r"(%s) - that is the name to be stated below the table. "
                            r"\textbf{1 mark} for a correct pivot with both margins, "
                            r"\textbf{1 mark} for the sort plus the region named. "
                            r"Empty cells (e.g. North/Grocery) are correct - there "
                            r"are no such orders."
                            % (TOP_REGION, rupees(TOP_AMOUNT)),
            ),
        ),
    ),),
)

# ---- Section B: the Apple Catcher model solution ------------------------------

TOP_Y, FLOOR_Y = 170, -170
EDGE = 220

setup_script = script(
    when_flag(),
    set_var("Score", 0),
    set_var("Lives", 3),
    set_var("Time", 60),
    show_var("Score"), show_var("Lives"), show_var("Time"),
    caption="Any sprite (or the Stage): initialise the three variables",
)

bowl_script = script(
    when_flag(),
    goto_xy(0, -150),
    forever(
        if_(key_pressed("right arrow"), changex(10)),
        if_(key_pressed("left arrow"), changex(-10)),
        if_(gt(x_position(), EDGE), setx(EDGE)),
        if_(lt(x_position(), -EDGE), setx(-EDGE)),
    ),
    caption="Bowl: start at bottom centre, move on the arrow keys, stay on stage",
)

apple_script = script(
    when_flag(),
    show(),
    goto_xy(pick_random(-EDGE, EDGE), TOP_Y),
    forever(
        changey(-8),
        if_(touching("Bowl"),
            change_var("Score", 1),
            play_sound("Pop"),
            goto_xy(pick_random(-EDGE, EDGE), TOP_Y)),
        if_(lt(y_position(), FLOOR_Y),
            goto_xy(pick_random(-EDGE, EDGE), TOP_Y)),
    ),
    caption="Apple: fall from a random x; caught scores a point, missed just resets",
)

ladybug_script = script(
    when_flag(),
    show(),
    goto_xy(pick_random(-EDGE, EDGE), TOP_Y),
    forever(
        changey(-5),
        if_(touching("Bowl"),
            change_var("Lives", -1),
            play_sound("Boing"),
            goto_xy(pick_random(-EDGE, EDGE), TOP_Y),
            if_(eq(var("Lives"), 0), broadcast("Game Over"))),
        if_(lt(y_position(), FLOOR_Y),
            goto_xy(pick_random(-EDGE, EDGE), TOP_Y)),
    ),
    caption="Ladybug2: same fall at a slower speed; a hit costs a life",
)

timer_script = script(
    when_flag(),
    repeat_until(eq(var("Time"), 0),
                 wait(1),
                 change_var("Time", -1)),
    broadcast("Game Over"),
    caption="Timer: one second per tick, then end the game",
)

gameover_hide_script = script(
    when_receive("Game Over"),
    hide(),
    caption="Apple and Ladybug2: leave the stage",
)

gameover_say_script = script(
    when_receive("Game Over"),
    say(join("Game Over! Your score is ", var("Score"))),
    wait(3),
    stop_all(),
    caption="Bowl (or Stage): show the final score, then stop everything",
)

SECTION_B = Section(
    name="Section B",
    title="Scratch Programming",
    scenario=(
        r"Your school is organising a \textbf{Health and Nutrition Week}. The "
        r"organisers want a small computer game for the exhibition stall that "
        r"encourages children to collect healthy fruit and avoid the garden pests."
        r"\par\vspace{5pt}"
        r"You have been asked to build this game in Scratch. It is called "
        r"\textbf{Apple Catcher}. A bowl at the bottom of the stage is moved left "
        r"and right by the player. Apples fall from the top of the stage at random "
        r"positions - catching an apple earns a point. Ladybugs also fall - touching "
        r"a ladybug costs a life. The game runs for a fixed time or until all lives are "
        r"lost, after which the final score is displayed."),
    questions=(Question(
        number=2,
        title="Design a game",
        parts=(
            Part(
                label="(a)", title="Setting up the project", marks=3,
                items=(r"Choose a suitable \textbf{backdrop} for the stage (for "
                       r"example a garden, park or sky).",
                       r"Create \textbf{three sprites} and rename them exactly as "
                       r"\blk{Bowl}, \blk{Apple} and \blk{Ladybug2}. Resize each sprite "
                       r"so that it is clearly visible but not larger than about "
                       r"one-fifth of the stage.",
                       r"Create \textbf{three variables} named \blk{Score}, "
                       r"\blk{Lives} and \blk{Time}, and make all three visible on "
                       r"the stage.",
                       r"When the green flag is clicked, the game must "
                       r"\textbf{initialise} the variables to Score $=$ 0, "
                       r"Lives $=$ 3, Time $=$ 60."),
                scripts=(setup_script,),
                answer_note=r"\textbf{1 mark} backdrop and three correctly named, "
                            r"sensibly sized sprites; \textbf{1 mark} the three "
                            r"variables created and shown on stage; \textbf{1 mark} "
                            r"initialisation under \blk{when green flag clicked}. The "
                            r"initialisation may sit on any sprite or the Stage.",
            ),
            Part(
                label="(b)", title="Controlling the bowl", marks=3,
                text=r"Write the script for the \blk{Bowl} sprite so that:",
                items=(r"It starts at the \textbf{bottom centre} of the stage every "
                       r"time the game begins.",
                       r"Pressing the \textbf{right arrow} key moves it to the right, "
                       r"and the \textbf{left arrow} key moves it to the left. The "
                       r"movement must be \textbf{continuous} while the key is held "
                       r"down.",
                       r"The bowl must \textbf{not disappear off the edge} of the "
                       r"stage."),
                scripts=(bowl_script,),
                answer_note=r"\textbf{1 mark} start position inside a "
                            r"\blk{when green flag clicked} script; \textbf{1 mark} "
                            r"both arrow keys read inside a \blk{forever} loop (a "
                            r"\blk{when key pressed} hat also gives continuous "
                            r"movement - accept it); \textbf{1 mark} an edge guard. "
                            r"Any working guard scores: the \blk{if x position} "
                            r"clamps shown here, or \blk{if on edge, bounce}.",
            ),
            Part(
                label="(c)", title="Falling apples and scoring", marks=4,
                text=r"Write the script for the \blk{Apple} sprite so that:",
                items=(r"It appears at the \textbf{top} of the stage at a "
                       r"\textbf{random horizontal position}, using the "
                       r"\blk{pick random} block.",
                       r"It \textbf{falls downwards} continuously.",
                       r"If it \textbf{touches the Bowl}, the score increases by 1, "
                       r"a \textbf{sound} is played, and the apple returns to the top "
                       r"at a new random position.",
                       r"If it reaches the \textbf{bottom} of the stage without being "
                       r"caught, it simply returns to the top at a new random "
                       r"position."),
                scripts=(apple_script,),
                answer_note=r"\textbf{1 mark} per numbered requirement. The random "
                            r"spawn must use \blk{pick random} with a sensible x "
                            r"range; falling must be a \blk{change y by} (negative) "
                            r"inside \blk{forever}.",
            ),
            Part(
                label="(d)", title="The ladybug and losing lives", marks=3,
                text=r"Write the script for the \blk{Ladybug2} sprite so that:",
                items=(r"It behaves like the apple - falling from a random position "
                       r"at the top - but moves at a \textbf{noticeably different "
                       r"speed}.",
                       r"If it touches the \blk{Bowl}, Lives decreases by 1 and a "
                       r"\textbf{different sound} is played.",
                       r"When Lives reaches 0, the message \blk{Game Over} is "
                       r"\textbf{broadcast}."),
                scripts=(ladybug_script,),
                answer_note=r"\textbf{1 mark} falling ladybug at a different step size "
                            r"from the apple; \textbf{1 mark} life lost with a "
                            r"different sound; \textbf{1 mark} the broadcast when "
                            r"Lives hits 0. Testing \blk{Lives = 0} or "
                            r"\blk{Lives < 1} both score.",
            ),
            Part(
                label="(e)", title="Timer and game over", marks=2,
                items=(r"Write a script that reduces \blk{Time} by 1 every second. "
                       r"When Time reaches 0, the message \blk{Game Over} must be "
                       r"broadcast.",
                       r"On receiving \blk{Game Over}: the Apple and the Ladybug2 must "
                       r"\textbf{hide}, a message showing the \textbf{final score} "
                       r"must be displayed on the stage (for example ``Game Over! "
                       r"Your score is 12''), and the whole program must then "
                       r"\textbf{stop}."),
                scripts=(timer_script, gameover_hide_script, gameover_say_script),
                answer_note=r"\textbf{1 mark} the countdown broadcasting at 0; "
                            r"\textbf{1 mark} the receivers - both sprites hidden, "
                            r"the joined score message shown, \blk{stop all} last. "
                            r"The \blk{when I receive} hide script goes on both the "
                            r"Apple and the Ladybug2. Note the countdown keeps running "
                            r"after a lives-out finish, so \blk{Game Over} can be "
                            r"broadcast twice - harmless here, and not penalised.",
            ),
        ),
    ),),
)


PAPER = Paper(
    title="Practical Examination - Paper 1",
    duration="1 hour 45 minutes",
    max_marks=25,
    instructions=(
        r"\textbf{All questions are compulsory.} Section A is done in "
        r"\textbf{LibreOffice Calc}; Section B is done in \textbf{Scratch}.",
        r"\textbf{Suggested time:} 15 minutes entering the data in Calc, 30 minutes "
        r"writing the formulas, chart and pivot table and emailing the file, and "
        r"60 minutes building the Scratch game.",
        r"Enter the two tables of Section A \textbf{exactly} as printed, on two "
        r"sheets named \sheetname{Product\_Master} and \sheetname{Sales\_Data}. "
        r"Columns F to I of \sheetname{Sales\_Data} must be filled by "
        r"\textbf{formula}, not typed by hand - typed values score no marks.",
        r"Save your spreadsheet as \sheetname{YourName.ods} and email it to "
        r"\sheetname{shivam@cs17.org} and \sheetname{hussain@cs17.org} before "
        r"starting Section B.",
        r"Save your Scratch project as \sheetname{YourName\_AppleCatcher} and leave "
        r"it open on screen at the end of the examination.",
        r"Marks are shown in brackets against each part.",
    ),
    sections=(SECTION_A, SECTION_B),
).check()
