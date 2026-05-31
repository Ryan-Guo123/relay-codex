PYTHON ?= python3
RELAY_RUNTIME := plugins/relay-codex/scripts/relay_runtime.py
ROOT ?= .

.PHONY: test test-runtime review-readiness validation-bundle

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

test-runtime:
	$(PYTHON) -m unittest tests.test_relay_runtime

review-readiness:
	$(PYTHON) $(RELAY_RUNTIME) review-readiness --root $(ROOT) --json

validation-bundle:
	$(PYTHON) $(RELAY_RUNTIME) review-readiness --root $(ROOT) --json
	$(PYTHON) $(RELAY_RUNTIME) handoff --root $(ROOT) --json
	$(PYTHON) $(RELAY_RUNTIME) pr-comment --root $(ROOT) --json
	$(PYTHON) $(RELAY_RUNTIME) reviewer-pack --root $(ROOT) --json
	$(PYTHON) $(RELAY_RUNTIME) validation-brief --root $(ROOT) --json
