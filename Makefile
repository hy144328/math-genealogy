COVERAGE = coverage
DOT = dot
MAKE = make
PYTHON = python3

.PHONY: juniper
juniper: examples/juniper.eps examples/juniper.png

examples/%.eps: examples/%.gv
	$(DOT) -Teps $< > $@

examples/%.png: examples/%.gv
	$(DOT) -Tpng $< > $@

examples/%.gv: examples/%.py
	$(PYTHON) $<

.PHONY: clean
clean:
	$(MAKE) -C examples/ clean

.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: cover
cover:
	$(COVERAGE) run -m pytest
	$(COVERAGE) report
