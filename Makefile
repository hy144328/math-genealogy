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

PYTHON = python
DOT = dot
PANDOC = pandoc

.PHONY: default
default:
	$(PYTHON) main.py

.PHONY: readme
readme: README.pdf
README.pdf: README.md
	$(PANDOC) -o README.pdf README.md

.PHONY: clean
clean:
	-rm README.pdf
	-rm *.pyc

