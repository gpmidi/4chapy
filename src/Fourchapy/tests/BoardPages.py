'''
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import unittest
from ConfigBase import ConfigBasedTests
from Fourchapy.tests.BoardIndex import BoardConfigBasedTests

class BoardPageConfigBasedTests(BoardConfigBasedTests):
    
    def setUp(self):
        BoardConfigBasedTests.setUp(self)
        self.boardPages = {}
        
        # Run the fetches now rather than wait
        for boardID, board in self.index.BoardsDict.items()[:self.recursionMaxBoards]:
            self.boardPages[boardID] = dict(
                                          board = board,
                                          pages = {},
                                          )
            for page in board.getPages()[:self.recursionMaxPages]:
                self.boardPages[boardID][page.Page] = page

class BoardPageInitialTestSequence(BoardPageConfigBasedTests):

    
