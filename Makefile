VENV := .venv
PY   := $(VENV)/bin/python

WS1 := worksheets/worksheet1_boolean_algebra
WS2 := worksheets/worksheet2_flowcharts
WS3 := worksheets/worksheet3_binary
WS4 := worksheets/worksheet4_hexadecimal
WS5 := worksheets/worksheet5_sevensegment
WS6 := worksheets/worksheet6_decisions

.PHONY: all boolean flowchart binary hex sevenseg decisions setup clean

# Build every worksheet  ->  make
all: boolean flowchart binary hex sevenseg decisions

boolean:
	$(PY) -m gens.boolgen.build $(WS1)/boolean_worksheet.py --out $(WS1)/build

flowchart:
	$(PY) -m gens.flowgen.build $(WS2)/flowchart_worksheet.py --out $(WS2)/build

binary:
	$(PY) -m gens.bingen.build $(WS3)/binary_worksheet.py --out $(WS3)/build

hex:
	$(PY) -m gens.bingen.build $(WS4)/hex_worksheet.py --out $(WS4)/build

sevenseg:
	$(PY) -m gens.segen.build $(WS5)/sevenseg_worksheet.py --out $(WS5)/build

decisions:
	$(PY) -m gens.flowgen.build $(WS6)/decisions_worksheet.py --out $(WS6)/build

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf worksheets/*/build
