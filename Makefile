VENV := .venv
PY   := $(VENV)/bin/python

.PHONY: all boolean flowchart binary hex setup clean

# Build every worksheet  ->  make
all: boolean flowchart binary hex

boolean:
	$(PY) -m boolgen.build boolean_worksheet.py

flowchart:
	$(PY) -m flowgen.build flowchart_worksheet.py

binary:
	$(PY) -m bingen.build binary_worksheet.py

hex:
	$(PY) -m bingen.build hex_worksheet.py

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf build
