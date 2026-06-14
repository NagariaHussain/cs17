VENV := .venv
PY   := $(VENV)/bin/python

WS1 := worksheets/worksheet1_boolean_algebra
WS2 := worksheets/worksheet2_flowcharts
WS3 := worksheets/worksheet3_binary
WS4 := worksheets/worksheet4_hexadecimal
WS5 := worksheets/worksheet5_sevensegment
WS6 := worksheets/worksheet6_decisions
WS7 := worksheets/worksheet7_loops

.PHONY: all boolean flowchart binary hex sevenseg decisions loops pdfs setup clean

# Build every worksheet, then collect all PDFs into pdfs/  ->  make
all: boolean flowchart binary hex sevenseg decisions loops pdfs

boolean:
	$(PY) -m gens.boolgen.build $(WS1)/worksheet_one_boolean_algebra.py --out $(WS1)/build

flowchart:
	$(PY) -m gens.flowgen.build $(WS2)/worksheet_two_flowcharts.py --out $(WS2)/build

binary:
	$(PY) -m gens.bingen.build $(WS3)/worksheet_three_binary.py --out $(WS3)/build

hex:
	$(PY) -m gens.bingen.build $(WS4)/worksheet_four_hexadecimal.py --out $(WS4)/build

sevenseg:
	$(PY) -m gens.segen.build $(WS5)/worksheet_five_seven_segment_display.py --out $(WS5)/build

decisions:
	$(PY) -m gens.flowgen.build $(WS6)/worksheet_six_decisions_and_calculations.py --out $(WS6)/build

loops:
	$(PY) -m gens.flowgen.build $(WS7)/worksheet_seven_simple_loops.py --out $(WS7)/build

# Gather every worksheet + answer-key PDF into a single pdfs/ folder as symlinks,
# so all worksheets can be browsed from one place (build/ holds figures + .tex).
pdfs:
	@mkdir -p pdfs
	@rm -f pdfs/*.pdf
	@for f in worksheets/worksheet*/build/*/*.pdf; do \
	  [ -e "$$f" ] || continue; \
	  ln -sf "../$$f" "pdfs/$$(basename "$$f")"; \
	done
	@echo "pdfs/ updated:"; ls -1 pdfs

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf worksheets/*/build pdfs
