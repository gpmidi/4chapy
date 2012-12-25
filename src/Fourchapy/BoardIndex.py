'''
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

# Setup logging
import logging
logger = logging.getLogger("Fourchapy." + __name__)
log = logger.log

from Fetcher import Fetch4chan
from Board import FourchapyBoard
from Errors import NoDataReturnedError  # Don't import *; it will overwrite logging vars

class FourchapyBoardIndex(Fetch4chan):
    """ Represent a list of all boards and info about those boards. 

    """
    
    def __init__(self, proto = 'http', **kw):
        self.Proto = proto
        
        log(10, "Creating %r", self)
        self.URL = '%s://api.4chan.org/boards.json' % self.Proto
        
        Fetch4chan.__init__(self, **kw)      
    
    @Fetch4chan.addLazyDataObjDec(attrName = 'Boards')
    def updateBoardsList(self, sleep = True):
        """ Download and update local data with data from 4chan. """
        # try:
        json = self.fetchJSON(sleep = sleep)
        # except NoDataReturnedError:
        #    raise NoDataReturnedError, "Failed to read board data from the 4chan servers"
        boards = []
        for boardData in json['boards']:
            board = FourchapyBoard(
                                 boardData = boardData,
                                 proto = self.Proto,
                                 )
            boards.append(board)
            log(5, "Created board %r", board)
        log(10, "Found %d boards", len(boards))
        return boards
    
    @Fetch4chan.addLazyDataObjDec(attrName = 'BoardsDict')
    def updateBoardsDict(self, sleep = True):
        ret = []
        for board in self.Boards:
            ret[board.Board] = board
        return ret
        
    def __repr__(self):
        return "<BoardIndex Use:%r>" % self.Proto
