# Copyright (C) 2016  Hans Yu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DOT = dot
LATEX = pdflatex -synctex=1 -interaction=nonstopmode -shell-escape
MAKE = make
PANDOC = pandoc
PYTHON = python

.PHONY: default
default: juniper

%:
	$(MAKE) $@.gv
	$(MAKE) $@.eps
	$(MAKE) $@.png
	$(MAKE) $@.pdf

%.pdf: %.eps %.tex
	$(LATEX) $(basename $<).tex

%.eps: %.gv
	$(DOT) -Teps $< > $@

%.png: %.gv
	$(DOT) -Tpng $< > $@

%.gv: %.py
	$(PYTHON) $< $(basename $<).gv

README.pdf: README.md
	$(PANDOC) -o README.pdf README.md

.PHONY: clean
clean:
	-rm README.pdf
	-rm *.eps
	-rm *.gv
	-rm *.png
	-rm *.aux
	-rm *.log
	-rm *.out
	-rm *.pdf
	-rm *.pyc
	-rm *.synctex.gz

.PHONY: test
test:
	python3 -m pytest

.PHONY: cover
cover:
	coverage run -m pytest
	coverage report
