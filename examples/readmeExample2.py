#!/usr/bin/python
#===============================================================================
#    This file is part of 4chapy. 
#
#    4chapy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    4chapy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with 4chapy.  If not, see http://www.gnu.org/licenses/old-licenses/gpl-2.0.html 
#===============================================================================
''' Second example from the README file
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''

# Import the library
from Fourchapy import Thread
# Download a thread from diy with an ID of 12345
t = Thread(boardID = 'diy', threadID = 12345)
# Loop over all posts in the thread and print out info from the post
for post in t.Posts:
    print "--- %d ---" % post.Number
    print "Subject: %s" % post.Subject
    print "Comment: %s" % post.Comment
