''' 4chapy Unit Tests
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging
log = logging.getLogger("Fourchapy")

log.debug("Initing")
import unittest

from Fourchapy.tests.BoardIndex import *
from Fourchapy.tests.BoardPages import *
from Fourchapy.tests.Posts import *

if __name__ == "__main__":
    unittest.main()
