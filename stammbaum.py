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

#!/usr/bin/env python

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
        # Add parent.
        self.mathematicians[parent.ident] = parent

        # Exit recursion.
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
                continue
            
            # name
            idx1 = idx2 + 2
            idx2 = the_page.find('<', idx1)
            name = the_page[idx1:idx2]
            
            # Add child.
            parent.advisors.append(ident)
            print "{:d}, {:s}".format(level+1, name)
            self.set_advisors(Node(ident, name), level+1)
    
            # Next advisor.
            idx1 = the_page.find('Advisor', idx1)
    
