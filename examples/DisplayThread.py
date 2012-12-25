#!/usr/bin/python
''' A simple script that will display the requested thread. 
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
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
import logging
logging.basicConfig()

# Default logging level.  
# DEFAULT_LOGGING_LEVEL = logging.DEBUG
# DEFAULT_LOGGING_LEVEL = logging.INFO
DEFAULT_LOGGING_LEVEL = logging.WARN
# DEFAULT_LOGGING_LEVEL = logging.ERROR

logger = logging.getLogger("DisplayThread")
logger.setLevel(DEFAULT_LOGGING_LEVEL)
log = logger.log

from optparse import OptionParser
from Fourchapy import FourchapyThread
import sys

if __name__ == "__main__":
    log(20, "Initing")
    parser = OptionParser(
                        usage = "%prog ",
                        # version = "%prog 0.1",
                        prog = "DisplayThread",
                        description = """
Author: Paulson McIntyre (GpMidi)
License: GPLv2
                        """,
                        )
    parser.add_option(
                      "--proto",
                      action = "store",
                      type = "choice",
                      dest = "protocol",
                      default = 'http',
                      choices = ('http', 'https'),
                      help = "The protocol to use when connecting to 4chan's API server. http or https. [default: %default]",
                      )
    parser.add_option(
                      "--board",
                      action = "store",
                      type = "string",
                      dest = "boardID",
                      default = None,
                      help = "The board to access. [default: %default]",
                      )
    parser.add_option(
                      "--thread",
                      action = "store",
                      type = "int",
                      dest = "threadID",
                      default = None,
                      help = "The ID number of the thread to display. [default: %default]",
                      )
    parser.add_option(
                      "--nameWidth",
                      action = "store",
                      type = "int",
                      dest = "nameWidth",
                      default = 15,
                      help = "The number of chars to reserve for the name portion of each post's field display. [default: %default]",
                      )
    log(10, "Parsing args")
    (opts, args) = parser.parse_args()
    
    log(10, "Getting config")
    threadID = opts.threadID
    boardID = opts.boardID
    if not boardID:
        print "Please use --board to define a board name. "
        sys.exit(1)
    if not threadID:
        print "Please use --thread to define a thread ID number. "
        sys.exit(1)
        
    log(10, "Creating thread object with ID=%r from board %r", threadID, boardID)
    t = FourchapyThread(boardID = boardID, threadID = threadID)
    log(10, "Created %r", t)
    
    print '=' * 100 
    print " Board %s - Thread %d" % (boardID, threadID)
    print '=' * 100
    print ""
    for post in t.Posts:
        post.display(nameWidth = opts.nameWidth)
    print ""
    print ""
    log(20, "All Done")
    
