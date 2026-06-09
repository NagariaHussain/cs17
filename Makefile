VENV := .venv
PY   := $(VENV)/bin/python

WS1 := worksheets/worksheet1_boolean_algebra
WS2 := worksheets/worksheet2_flowcharts
WS3 := worksheets/worksheet3_binary
WS4 := worksheets/worksheet4_hexadecimal

.PHONY: all boolean flowchart binary hex setup clean

# Build every worksheet  ->  make
all: boolean flowchart binary hex

boolean:
	$(PY) -m gens.boolgen.build $(WS1)/boolean_worksheet.py --out $(WS1)/build

flowchart:
	$(PY) -m gens.flowgen.build $(WS2)/flowchart_worksheet.py --out $(WS2)/build

binary:
	$(PY) -m gens.bingen.build $(WS3)/binary_worksheet.py --out $(WS3)/build

hex:
	$(PY) -m gens.bingen.build $(WS4)/hex_worksheet.py --out $(WS4)/build

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf worksheets/*/build
