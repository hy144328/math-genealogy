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
        self.year = None
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

        # year
        year = None
        idx2 = 0
        while idx2 != -1:
            idx2 = the_page.find("</span>", idx2 + 1)
            idx1 = the_page.rfind(" ", 0, idx2)
            if the_page[idx1 + 1:idx2].isdigit():
                year = int(the_page[idx1 + 1:idx2])
                parent.year = year
                print(year)
                break

        idx1 = the_page.find('Advisor')
        while idx1 != -1:
            # Test for 'Advisor: Unknown'.
            idx1 = the_page.find(':', idx1) + 2
            idx2 = idx1 + 7
            if the_page[idx1:idx2] == 'Unknown':
                print "{:d}, {:s}".format(level+1, "Advisor unknown")
                idx1 = the_page.find('Advisor', idx1)
                continue

            # ID
            idx1 = the_page.find('id=', idx1) + 3
            idx2 = the_page.find('"', idx1)
            ident = int(the_page[idx1:idx2])
            
            # name
            idx1 = idx2 + 2
            idx2 = the_page.find('<', idx1)
            name = " ".join(the_page[idx1:idx2].split())
            
            # Add child.
            parent.advisors.append(ident)
            self.set_advisors(Node(ident, name), level+1)

            # Next advisor.
            idx1 = the_page.find('Advisor', idx1)

    # Enforce maximum level.
    # Run twice to ensure that there are no dangling advisors.
    def cut_tree(self, parent, level=0):
        for child_id in parent.advisors[:]:
            try: # Recursion.
                child = self.mathematicians[child_id]
                self.cut_tree(child, level+1)
            except(KeyError): # Remove dangling advisor.
                parent.advisors.remove(child_id)

        # Remove node.
        if level > self.max_level:
            del self.mathematicians[parent.ident]

        # Leaves have no children.
        if level == self.max_level:
            parent.advisors = []

    # Print dot input.
    def print_dot(self, root_nodes, output_file="stammbaum.gv"):
        # First version.
        output_file_temp = output_file+".temp"
        f = open(output_file_temp, 'w')
        f.write("digraph Stammbaum {\n")
        f.write("rankdir = BT;\n")
        f.write("node [shape=box, style=rounded];\n")
        f.write("\n")

        # Order root.
        f.write("{\n")
        f.write("rank = same;\n")
        f.write("\n")
        for node_it in root_nodes:
            if node_it.year == None:
                f.write("\"{:s}\";\n".format(node_it.name))
            else:
                f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(node_it.name, 21 - node_it.year // 100))
            #elif node_it.year >= 1990:
            #    f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(node_it.name, 202 - node_it.year // 10))
            #else:
            #    f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(node_it.name, 23 - node_it.year // 100))
        f.write("}\n")
        f.write("\n")

        # Print nodes.
        for it_id in self.mathematicians:
            if self.mathematicians[it_id].year == None:
                f.write("\"{:s}\";\n".format(self.mathematicians[it_id].name))
            else:
                f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(self.mathematicians[it_id].name, 21 - self.mathematicians[it_id].year // 100))
            #elif self.mathematicians[it_id].year >= 1990:
            #    f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(self.mathematicians[it_id].name, 202 - self.mathematicians[it_id].year // 10))
            #else:
            #    f.write("\"{:s}\" [style=\"rounded,filled\", colorscheme=pastel19, fillcolor={:d}];\n".format(self.mathematicians[it_id].name, 23 - self.mathematicians[it_id].year // 100))
        f.write("\n")

        # Print edges.
        f.write("{\n")
        for it in root_nodes:
            self.print_dot_branch(it, f)
        f.write("}\n")
        f.write("\n")

        f.write("}\n")
        f.close()

        # Second version.
        self.print_dot_uniq(output_file)
        os.remove(output_file_temp)

    # Recursive function.
    def print_dot_branch(self, parent_node, f):
        for child_id in parent_node.advisors:
            child_node = self.mathematicians[child_id]
            f.write("\"{:s}\" -> \"{:s}\" [dir=back];\n".format(parent_node.name, child_node.name))
            self.print_dot_branch(child_node, f)
            
    # Remove duplicate lines.
    def print_dot_uniq(self, output_file):
        f = open(output_file, 'w')
        lines_seen = set()

        for line in open(output_file+".temp", 'r'):
            if len(line) < 3:
                f.write(line)
                continue

            if line not in lines_seen:
                lines_seen.add(line)
                # Remove parentheses.
                while True:
                    idx1 = line.find(' (')
                    idx2 = line.find(')')
                    if idx1 == -1 or idx2 == -1:
                        break
                    line = line[:idx1] + line[idx2+1:]
                f.write(line)

        f.close()

