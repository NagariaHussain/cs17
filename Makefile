VENV := .venv
PY   := $(VENV)/bin/python

WS1 := worksheets/worksheet1_boolean_algebra
WS2 := worksheets/worksheet2_flowcharts
WS3 := worksheets/worksheet3_binary
WS4 := worksheets/worksheet4_hexadecimal
WS5 := worksheets/worksheet5_sevensegment
WS6 := worksheets/worksheet6_decisions
WS7 := worksheets/worksheet7_loops
WS8 := worksheets/worksheet8_flowcharts_intermediate
WS9 := worksheets/worksheet9_logic_and_flowcharts
WS10 := worksheets/worksheet10_drawing_flowcharts
WS11 := worksheets/worksheet11_coordinate_system
WS12 := worksheets/worksheet12_scratch_projects
WS13 := worksheets/worksheet13_scratch_sensing
WS14 := worksheets/worksheet14_scratch_variables
WS15 := worksheets/worksheet15_scratch_game
WS16 := worksheets/worksheet16_anchor_points
WS17 := worksheets/worksheet17_scratch_coins
WS18 := worksheets/worksheet18_scratch_dodge
WS19 := worksheets/worksheet19_scratch_invaders
WS20 := worksheets/worksheet20_debugging_flowcharts

Q1EXAM := exams/q1_final

.PHONY: all boolean flowchart binary hex sevenseg decisions loops intermediate mixed drawing coords scratch anchors debugging exams pdfs setup clean

# Build every worksheet, then collect all PDFs into pdfs/  ->  make
all: boolean flowchart binary hex sevenseg decisions loops intermediate mixed drawing coords scratch anchors debugging exams pdfs

boolean:
	$(PY) -m gens.boolgen.build $(WS1)/worksheet_1_boolean_algebra.py --out $(WS1)/build

flowchart:
	$(PY) -m gens.flowgen.build $(WS2)/worksheet_2_flowcharts.py --out $(WS2)/build

binary:
	$(PY) -m gens.bingen.build $(WS3)/worksheet_3_binary.py --out $(WS3)/build

hex:
	$(PY) -m gens.bingen.build $(WS4)/worksheet_4_hexadecimal.py --out $(WS4)/build

sevenseg:
	$(PY) -m gens.segen.build $(WS5)/worksheet_5_seven_segment_display.py --out $(WS5)/build

decisions:
	$(PY) -m gens.flowgen.build $(WS6)/worksheet_6_decisions_and_calculations.py --out $(WS6)/build

loops:
	$(PY) -m gens.flowgen.build $(WS7)/worksheet_7_simple_loops.py --out $(WS7)/build

intermediate:
	$(PY) -m gens.flowgen.build $(WS8)/worksheet_8_flowcharts_intermediate.py --out $(WS8)/build

# Worksheet 9 is a mixed review: boolgen hosts it (Boolean is the lead topic)
# and also dispatches its flowchart-tracing problems via flowgen.
mixed:
	$(PY) -m gens.boolgen.build $(WS9)/worksheet_9_logic_and_flowcharts.py --out $(WS9)/build

# Worksheet 10 is DRAW-only: every problem is a plain-English statement and the
# student draws the flowchart (the answer key derives the flowchart from source).
drawing:
	$(PY) -m gens.flowgen.build $(WS10)/worksheet_10_drawing_flowcharts.py --out $(WS10)/build

# Worksheet 11 primes the Scratch stage coordinate system: read/plot points on a
# grid centred at (0,0), then write turtle instructions (go to / change x / change
# y / move / turn) to hit a target. Built by the turtlegen generator (inline TikZ).
coords:
	$(PY) -m gens.turtlegen.build $(WS11)/worksheet_11_coordinate_system.py --out $(WS11)/build

# Worksheets 12-19 are the follow-along Scratch build sheets. A-D (12-15) teach
# the blocks, ramping from basics (A/12) through sensing & choices (B/13) and
# variables & score (C/14) to a complete multi-sprite game (D/15). E-F (17-18)
# are capstones: one game each, mostly given to drag together but with grey
# "your turn" gaps the student fills in - Coin Dash (E/17) and Rock Dodge (F/18).
# G (19) is the big capstone: a full Space Invaders shown as a finished reference
# build, whose headline concept is clone coordination (a 55-strong fleet of
# clones sharing one brain) plus custom blocks. Each finished script is authored
# once in scratchgen and rendered via the scratch3 package, so the blocks shown
# match the prose build steps. All share the generator, so they rebuild together.
scratch:
	$(PY) -m gens.scratchgen.build $(WS12)/worksheet_12_scratch_projects.py --out $(WS12)/build
	$(PY) -m gens.scratchgen.build $(WS13)/worksheet_13_scratch_sensing.py --out $(WS13)/build
	$(PY) -m gens.scratchgen.build $(WS14)/worksheet_14_scratch_variables.py --out $(WS14)/build
	$(PY) -m gens.scratchgen.build $(WS15)/worksheet_15_scratch_game.py --out $(WS15)/build
	$(PY) -m gens.scratchgen.build $(WS17)/worksheet_17_scratch_coins.py --out $(WS17)/build
	$(PY) -m gens.scratchgen.build $(WS18)/worksheet_18_scratch_dodge.py --out $(WS18)/build
	$(PY) -m gens.scratchgen.build $(WS19)/worksheet_19_scratch_invaders.py --out $(WS19)/build

# Worksheet 16 bridges Worksheet 11 (points) and the Scratch build sheets: a
# sprite is not a point but a box, and Scratch pins it to the grid by its centre.
# The student reads/places/computes the box's corners and edges, then writes the
# real grounded-check block (feet = y position minus height/2). Built by boxgen,
# which reuses turtlegen's grid frame (gens/gridframe) and scratchgen's block
# renderer for the capstone, all inline (TikZ + scratch3).
anchors:
	$(PY) -m gens.boxgen.build $(WS16)/worksheet_16_anchor_points.py --out $(WS16)/build

# Worksheet 20 turns tracing round: every flowchart has exactly ONE wrong box
# (a boundary comparison, an off-by-one loop test, a missing counter update, a
# print inside the loop, ...) and the student works backwards from the wrong
# output to the box. Each problem is authored as the CORRECT algorithm plus a
# one-line bug (gens/flowgen/bug.py), so the buggy chart, the should-print vs
# actually-prints table, and the answer key's fix are all derived from one source.
debugging:
	$(PY) -m gens.flowgen.build $(WS20)/worksheet_20_debugging_flowcharts.py --out $(WS20)/build

# Exam question papers (examgen). Each paper module holds the header fields
# (subject, paper, time allowed) and a QUESTIONS list; an empty list renders the
# title block alone, which is the boilerplate to fill in. No answer key.
exams:
	$(PY) -m gens.examgen.build $(Q1EXAM)/theory.py    --out $(Q1EXAM)/build
	$(PY) -m gens.examgen.build $(Q1EXAM)/practical.py --out $(Q1EXAM)/build

# Gather every PDF into pdfs/ as real copies (build/ holds figures + .tex), split
# into pdfs/sheets/ (the worksheets) and pdfs/answer_keys/ (the -answers PDFs) so
# all worksheets can be browsed from one place. We copy rather than symlink so the
# files are standalone (symlinks break when shared, e.g. uploaded to Telegram).
pdfs:
	@mkdir -p pdfs/sheets pdfs/answer_keys
	@rm -f pdfs/sheets/*.pdf pdfs/answer_keys/*.pdf
	@for f in worksheets/worksheet*/build/*/*.pdf; do \
	  [ -e "$$f" ] || continue; \
	  case "$$f" in \
	    *-answers.pdf) cp "$$f" "pdfs/answer_keys/$$(basename "$$f")" ;; \
	    *)             cp "$$f" "pdfs/sheets/$$(basename "$$f")" ;; \
	  esac; \
	done
	@echo "pdfs/sheets:";      ls -1 pdfs/sheets
	@echo "pdfs/answer_keys:"; ls -1 pdfs/answer_keys

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf worksheets/*/build exams/*/build pdfs
