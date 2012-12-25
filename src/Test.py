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
import logging
logging.basicConfig()

# Default logging level.  
DEFAULT_LOGGING_LEVEL = 1
# DEFAULT_LOGGING_LEVEL = logging.DEBUG
# DEFAULT_LOGGING_LEVEL = logging.INFO
# DEFAULT_LOGGING_LEVEL = logging.WARN
# DEFAULT_LOGGING_LEVEL = logging.ERROR

# Config file telling us what tests to run and what data to use with the tests
DEFAULT_CONFIG_FILE = 'test.conf.ini'
# Screen width, in chars
# Don't forget about the "INFO:Fourchapy" width
DISPLAY_WIDTH = 150
# Test results
RESULTS_PASS = "PASS"
RESULTS_FAIL = "FAIL"

logger = logging.getLogger("Fourchapy")
logger.setLevel(DEFAULT_LOGGING_LEVEL)
log = logger.log

from ConfigParser import SafeConfigParser
import re

def Thread_Main_Test(cfg, testName, testType):
    log(10, "Loading library")
    from Fourchapy import FourchapyThread
    
    log(10, "Getting config")
    threadID = cfg.getint(testName, 'threadID')
    boardID = cfg.get(testName, 'boardID')
        
    log(10, "Creating thread object with ID=%r from board %r", threadID, boardID)
    t = FourchapyThread(boardID = boardID, threadID = threadID)
    log(10, "Created %r", t)
    
    return RESULTS_PASS


def Boards_Main_Test(cfg, testName, testType):
    log(10, "Loading library")
    from Fourchapy import FourchapyBoardIndex
    
    log(10, "Getting config")
    # Recurse into this board+page+threads
    pageID = cfg.getint(testName, 'pageID')
    boardID = cfg.get(testName, 'boardID')
    # HTTP/HTTPS
    proto = cfg.get(testName, 'proto')
    
    log(10, "Creating board index object")
    index = FourchapyBoardIndex(proto = proto)
    
    for board in index.Boards:
        log(5, "Looking at board %r", board)
        if board.BoardID == boardID:
            log(10, "Found a board to work with")
            for page in board.getPages(minPage = pageID, maxPage = pageID):
                log(10, "Looking at page %r", page)
                assert page.Page == pageID
                for thread in page.Threads:
                    log(10, "Found thread %r", thread)
    
    return RESULTS_PASS


# Regexs used to match the section names to different tests
TEST_NAME_REGEXS = dict(
                        ThreadMain = dict(
                                          re = re.compile(r'^ThreadMain\-\d+$'),
                                          func = Thread_Main_Test,
                                          ),
                        BoardsMain = dict(
                                          re = re.compile(r'^BoardsMain\-\d+$'),
                                          func = Boards_Main_Test,
                                          ),
                        )

if __name__ == "__main__":
    log(20, "Initing")
    cfg = SafeConfigParser()
    results = {}
    
    log(20, "Loading config")
    cfg.read(DEFAULT_CONFIG_FILE)
    
    log(20, "Setting up logging")
    if not cfg.has_section('Global'):
        cfg.add_section('Global')
    if not cfg.has_option('Global', 'loggingLevel'):
        cfg.set('Global', 'loggingLevel', DEFAULT_LOGGING_LEVEL)
    logger.setLevel(cfg.getint('Global', 'loggingLevel'))
    
    log(20, "Begining tests")
    for testName in cfg.sections():
        log(10, "Looking at test %r", testName)
        for testType, info in TEST_NAME_REGEXS.items():
            if not results.has_key(testType):
                results[testType] = {}
            if info['re'].match(testName):
                log(20, "Trying test %r of type %r", testName, testType)
                try:
                    results[testType][testName] = info['func'](cfg = cfg, testName = testName, testType = testType)
                except Exception, e:
                    results[testType][testName] = e
                    logger.exception("Error %r in test %r of type %r" % (e, testName, testType))
        log(10, "Done with %r", testName)

    log(20, "All tests have completed")
        
    for testType, names in results.items():
        log(20, "-"*DISPLAY_WIDTH)
        log(20, testType.center(DISPLAY_WIDTH))
        log(20, "-"*DISPLAY_WIDTH)
        for testName, result in names.items():
            if isinstance(result, Exception):
                begin = testName.rjust(30) + ": " + RESULTS_FAIL
                log(20, begin + repr(result)[:DISPLAY_WIDTH - len(begin)])
            else:
                log(20, testName.rjust(30) + ": " + result)
        log(20, "-"*DISPLAY_WIDTH)
        log(20, " "*DISPLAY_WIDTH)
    
    log(20, "All Done")
    
