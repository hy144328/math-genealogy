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

#!/usr/bin/env python

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

# NPJ.
npj_node = Node(-1, 'Nicholas P. Jamieson')
npj_node.advisors.append(student_ident)
g.mathematicians[npj_node.ident] = npj_node

# Source code for dot.
g.print_dot([npj_node])

