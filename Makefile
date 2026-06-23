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

.PHONY: all boolean flowchart binary hex sevenseg decisions loops intermediate mixed drawing pdfs setup clean

# Build every worksheet, then collect all PDFs into pdfs/  ->  make
all: boolean flowchart binary hex sevenseg decisions loops intermediate mixed drawing pdfs

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

# Gather every PDF into pdfs/ as symlinks (build/ holds figures + .tex), split
# into pdfs/sheets/ (the worksheets) and pdfs/answer_keys/ (the -answers PDFs)
# so all worksheets can be browsed from one place.
pdfs:
	@mkdir -p pdfs/sheets pdfs/answer_keys
	@rm -f pdfs/sheets/*.pdf pdfs/answer_keys/*.pdf
	@for f in worksheets/worksheet*/build/*/*.pdf; do \
	  [ -e "$$f" ] || continue; \
	  case "$$f" in \
	    *-answers.pdf) ln -sf "../../$$f" "pdfs/answer_keys/$$(basename "$$f")" ;; \
	    *)             ln -sf "../../$$f" "pdfs/sheets/$$(basename "$$f")" ;; \
	  esac; \
	done
	@echo "pdfs/sheets:";      ls -1 pdfs/sheets
	@echo "pdfs/answer_keys:"; ls -1 pdfs/answer_keys

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf worksheets/*/build pdfs
