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

class FourchapyBoard(object):
    """ A 4chan board
    """
    POSTOBJECTS = {
                   'board':dict(type = str, name = "BoardID", desc = "Board ID string"),
                   'title':dict(type = str, name = "BoardName", desc = "Human readable board name"),
                   'ws_board':dict(type = bool, name = "SafeForWork", desc = "The board's contents are work safe"),
                   'per_page':dict(type = int, name = "ThreadsPerPage", desc = "The number of threads displayed per page"),
                   'pages':dict(type = int, name = "Pages", desc = "The number of pages of threads"),
                   }
    
    def __init__(self, boardData = None, proto = 'http'):
        self.Proto = proto
        self._rawData = boardData
        
        for code, info in self.POSTOBJECTS.items():
            if boardData.has_key(code):
                log(5, "Found %r. Set %r to %r", code, info['name'], boardData[code])
                setattr(self, info['name'], boardData[code])
            else:
                log(5, "Didn't find %r", code)
                setattr(self, info['name'], None)
        
    def displayToString(self, nameWidth = 15):
        """ Return a multi-line string that displays this post's info. """
        ret = '=' * 50 + "\n"
        ret += " %s #%d: %r" % (self.Board, self.Number, self.Subject) + "\n"
        ret += '=' * 50 + "\n"
        for code, info in self.POSTOBJECTS.items():
            value = str(getattr(self, info['name']))
            if value == "None":
                continue
            if value.count('\n') == 0:
                for line in value.split('<br>'):
                    ret += info['name'].rjust(nameWidth) + ": " + line + "\n"
            else:
                for line in value.splitlines():
                    for line2 in line.split('<br>'):
                        ret += info['name'].rjust(nameWidth) + ": " + line2 + "\n"
        return ret
    
    def display(self, nameWidth = 15):
        """ Return a multi-line string that displays this post's info. """
        print self.displayToString(nameWidth = nameWidth)
    
    def getMinPage(self):
        """ Returns the lowest page number for the board """
        return 0
    
    def getMaxPage(self):
        """ Returns the highest page number. """
        return self.Pages - 1
    
    def TotalThreads(self):
        """ Returns the total number of threads that are active """
        return self.Pages * self.ThreadsPerPage
    
    def getBoardAPIPageURL(self, page = 0):
        """ Returns the URL of the JSON data that contains a 
        thread index for the page requested.
        @param page: int 0 to self.Pages-1
        """
        page = int(page)
        if hasattr(self, 'Pages') and hasattr(self, 'BoardID'):
            if page >= 0 and page < self.Pages:
                return "%s://api.4chan.org/%s/%d.json" % (
                                                          self.Proto,
                                                          self.BoardID,
                                                          page,
                                                          )
        return None
    
    
