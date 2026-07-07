TARGET ?= .
OUTPUT ?= graph.html
EXCLUDE ?= venv,__pycache__

.PHONY: install run run-out run-exclude clean

install:
	@pip install -e .

run:
	@pydescope $(TARGET)

run-out:
	@pydescope $(TARGET) --output $(OUTPUT)

run-exclude:
	@pydescope $(TARGET) --exclude $(EXCLUDE)

clean:
	@powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
	@powershell -Command "Remove-Item -Force *.html -ErrorAction SilentlyContinue"


.PHONY: test test-cov

test:
	@pytest tests/

test-cov:
	@pytest --cov=pydescope tests/ --cov-report=term-missing


