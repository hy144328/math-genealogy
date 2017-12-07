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

MAKE = make
PYTHON = python
DOT = dot
PANDOC = pandoc

.PHONY: default
default:
	$(MAKE) stammbaum.gv
	$(MAKE) stammbaum.eps
	$(MAKE) stammbaum.png
	pdflatex -synctex=1 -interaction=nonstopmode -shell-escape main.tex

stammbaum.eps: stammbaum.gv
	$(DOT) -Teps stammbaum.gv > stammbaum.eps

stammbaum.png: stammbaum.gv
	$(DOT) -Tpng stammbaum.gv > stammbaum.png

stammbaum.gv: main.py stammbaum.py
	$(PYTHON) main.py > stammbaum.log 2>&1

.PHONY: test
test:
	$(PYTHON) main.py | tee stammbaum.log 2>&1

.PHONY: readme
readme: README.pdf
README.pdf: README.md
	$(PANDOC) -o README.pdf README.md

.PHONY: clean
clean:
	-rm README.pdf
	-rm stammbaum.eps
	-rm stammbaum.gv
	-rm stammbaum.log
	-rm stammbaum.png
	-rm *.aux
	-rm *.log
	-rm *.out
	-rm *.pdf
	-rm *.pyc
	-rm *.synctex.gz

