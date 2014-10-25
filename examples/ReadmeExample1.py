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
''' First example from the README file
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging
logging.basicConfig(level=logging.DEBUG)


# Import the library
from Fourchapy import BoardIndex
# Download a list of all boards and basic info about them (via http)
b = BoardIndex()
# Look over the first two boards only
for board in b.Boards[:2]:
    # Watch out for the unicode
    print u"Board %s (%s)" % (board.Board, board.BoardName)
    if board.SafeForWork:
        print "Safe for work"
    else:
        print "Not safe for work"
    # Get the first two pages only
    for page in board.getPages(maxPage = 1):
        print "Looking at page %d of board %r" % (page.Page, board.Board)
        # Get the first two threads only
        for thread in page.Threads[:2]:
            print "---- Thread %d ----" % thread.Thread
            for post in thread.Posts:
                print "--- %d ---" % post.Number
                print "Subject: %r" % post.Subject
                print "Comment: %r" % post.Comment
