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

# settings
max_level = 5
address_base = 'https://genealogy.math.ndsu.nodak.edu/id.php?id=' # Matthew Juniper

# parent
student_ident = 149678
student_name = 'Matthew P. Juniper'

mathematicians = {}

class Node:
    ident = -1
    name = ''
    advisors = []

    def __init__(self, anIdent, aName):
        self.ident = anIdent
        self.name = aName
        self.advisors = []

    def __str__(self):
        return "({:d}, {:s})".format(self.ident, self.name)

def set_advisors(parent, level):
    if level == max_level:
        return

    response = urllib2.urlopen(address_base+str(parent.ident))
    the_page = response.read()
    idx1 = the_page.find('Advisor')
    
    while idx1 != -1:
        # ID
        idx1 = the_page.find('id=', idx1) + 3
        idx2 = the_page.find('"', idx1)
        print the_page[idx1:idx2]
        try:
            ident = int(the_page[idx1:idx2])
        except ValueError:
            continue
        
        # name
        idx1 = idx2 + 2
        idx2 = the_page.find('<', idx1)
        name = the_page[idx1:idx2]
        
        mathematicians[ident] = Node(ident, name)
        parent.advisors.append(ident)

        idx1 = the_page.find('Advisor', idx1)

    print level+1, [mathematicians[m].name for m in parent.advisors]

    for m in parent.advisors:
        set_advisors(mathematicians[m], level+1)

