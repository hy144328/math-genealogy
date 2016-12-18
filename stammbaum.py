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

import os
import urllib2

address_base = 'https://genealogy.math.ndsu.nodak.edu/id.php?id='

class Node:
    def __init__(self, ident, name):
        self.ident = ident
        self.name = name
        self.advisors = []

    def __str__(self):
        return "({:d}, {:s})".format(self.ident, self.name)

class Stammbaum:
    def __init__(self, max_level):
        self.mathematicians = {}
        self.max_level = max_level

    # Recursive function.
    def set_advisors(self, parent, level=0):
        # Exit recursion if new branch meets old branch.
        if parent.ident in self.mathematicians:
            return

        # Add node.
        self.mathematicians[parent.ident] = parent
        print "{:d}, {:s} ({:d})".format(level, parent.name, parent.ident)

        # Exit recursion if maximum level is reached.
        if level == self.max_level:
            return
    
        # Open URL.
        response = urllib2.urlopen(address_base+str(parent.ident))
        the_page = response.read()
        idx1 = the_page.find('Advisor')
        
        while idx1 != -1:
            # ID
            idx1 = the_page.find('id=', idx1) + 3
            idx2 = the_page.find('"', idx1)
            #print "{:s}".format(the_page[idx1:idx2])
            try:
                ident = int(the_page[idx1:idx2])
            except ValueError:
                print "{:d}, {:s}".format(level+1, "Advisor unknown")
                continue
            
            # name
            idx1 = idx2 + 2
            idx2 = the_page.find('<', idx1)
            name = the_page[idx1:idx2].replace("  ", " ")
            
            # Add child.
            parent.advisors.append(ident)
            self.set_advisors(Node(ident, name), level+1)
    
            # Next advisor.
            idx1 = the_page.find('Advisor', idx1)

    # Print dot input.
    def print_dot(self, root_nodes, output_file="stammbaum.gv"):
        # First version.
        output_file_temp = output_file+".temp"
        f = open(output_file_temp, 'w')

        f.write("digraph Stammbaum {\n")

        for it_id in self.mathematicians:
            f.write("\"{:s}\";\n".format(self.mathematicians[it_id].name))

        f.write("\n")

        for it in root_nodes:
            self.print_dot_branch(it, f)

        f.write("}\n")
        f.close()

        # Second version.
        self.print_dot_uniq(output_file)
        os.remove(output_file_temp)

    # Recursive function.
    def print_dot_branch(self, parent_node, f):
        for child_id in parent_node.advisors:
            child_node = self.mathematicians[child_id]
            f.write("\"{:s}\" -> \"{:s}\";\n".format(parent_node.name, child_node.name))
            self.print_dot_branch(child_node, f)
            
    # Remove duplicate lines.
    def print_dot_uniq(self, output_file):
        f = open(output_file, 'w')
        lines_seen = set()

        for line in open(output_file+".temp", 'r'):
            if line not in lines_seen:
                f.write(line)
                lines_seen.add(line)

        f.close()

