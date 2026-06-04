VENV := .venv
PY   := $(VENV)/bin/python

.PHONY: all boolean flowchart setup clean

# Build every worksheet  ->  make
all: boolean flowchart

boolean:
	$(PY) -m boolgen.build worksheet.py

flowchart:
	$(PY) -m flowgen.build flowchart_worksheet.py

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt

clean:
	rm -rf build
