#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Copyright (C) 2016  Hans Yu <hans.yu@outlook.de>
#
# This file is part of MathDjinn.
#
# MathDjinn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MathDjinn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MathDjinn.  If not, see <http://www.gnu.org/licenses/>.

import sys

from stammbaum import *

# settings
max_level = 30

# parent
student_ident = 149678
student_name = 'Matthew P. Juniper'
student_node = Node(student_ident, student_name)

# Generate genealogy.
g = Stammbaum(max_level)
g.set_advisors(student_node, 1)
g.cut_tree(student_node, 1)
g.cut_tree(student_node, 1) # Run for a second time (see stammbaum).

# Cut leafs.
leafs = []
leafs.append('Johannes von Gmunden')
leafs.append('Heinrich von Langenstein')
leafs.append('Nicole Oresme')
leafs.append('Johannes von Gmunden')
leafs.append('Leo Outers')
keys = []
for key_it in g.mathematicians:
    if g.mathematicians[key_it].name in leafs:
        keys.append(key_it)
        print("{} cut.".format(g.mathematicians[key_it].name))
for key_it in keys:
    del g.mathematicians[key_it]
g.cut_tree(student_node, 1)

# NPJ.
root_names = []
root_years = []
root_names.append("Simon Rees")
root_years.append(2009)
root_names.append("Gary Chandler")
root_years.append(2010)
root_names.append("Larry Li")
root_years.append(2011)
root_names.append("Iain Waugh")
root_years.append(2013)
root_names.append("Ubaid Qadri")
root_years.append(2013)
root_names.append("Karthik Kashinath")
root_years.append(2013)
root_names.append("Vikrant Gupta")
root_years.append(2014)
root_names.append("Giulio Ghirardo")
root_years.append(2015)
root_names.append("Luca Magri")
root_years.append(2015)
root_names.append("Alessandro Orchini")
root_years.append(2016)
root_names.append("Nicholas Jamieson")
root_years.append(2018)
root_names.append("José Aguilar Perez")
root_years.append(2019)
root_names.append("Jack Brewster")
root_years.append(2019)
root_nodes = []
for root_ct in range(len(root_names)):
    name_it = root_names[root_ct]
    node_it = Node(-root_ct, name_it)
    node_it.year = root_years[root_ct]
    node_it.advisors.append(student_ident)
    g.mathematicians[node_it.ident] = node_it
    root_nodes.append(node_it)

# Source code for dot.
if len(sys.argv) > 1:
    g.print_dot(root_nodes, sys.argv[1])
else:
    g.print_dot(root_nodes)
