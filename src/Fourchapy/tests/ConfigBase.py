'''
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging
# Default logging level.  
# DEFAULT_LOGGING_LEVEL = 1
DEFAULT_LOGGING_LEVEL = logging.DEBUG
# DEFAULT_LOGGING_LEVEL = logging.INFO
# DEFAULT_LOGGING_LEVEL = logging.WARN
# DEFAULT_LOGGING_LEVEL = logging.ERROR
logging.basicConfig(level = DEFAULT_LOGGING_LEVEL)
log = logging.getLogger("Fourchapy.tests.ConfigBase")
log.setLevel(DEFAULT_LOGGING_LEVEL)
# Config file telling us what tests to run and what data to use with the tests
DEFAULT_CONFIG_FILE = 'test.conf.ini'

from ConfigParser import SafeConfigParser
import re
import unittest

class ConfigBasedTests(unittest.TestCase):
    
    def setUp(self):
        self.log = logging.getLogger("Fourchapy.tests.ConfigBase.%s" % type(self).__name__)
        
        self.log.debug("Loading config")
        self.cfg = SafeConfigParser()
        self.log.debug("Reading config file")
        self.cfg.read(DEFAULT_CONFIG_FILE)
        
        self.log.debug("Setting up logging")
        if not self.cfg.has_section('Global'):
            self.cfg.add_section('Global')
        # Global config - Logging level
        if not self.cfg.has_option('Global', 'loggingLevel'):
            self.cfg.set('Global', 'loggingLevel', str(DEFAULT_LOGGING_LEVEL))
        self.log.setLevel(self.cfg.getint('Global', 'loggingLevel'))
        # Global config - proxies
        self.proxy = {}
        self.proxy['http'] = self._get_option(
                                              section = 'Global',
                                              option = 'proxy_http',
                                              default = None,
                                              vtype = 'str',
                                              )
# Doesn't actually work atm - urllib doesn't support using
# https and a proxy at the same time. 
#        self.proxy['https'] = self._get_option(
#                                              section = 'Global',
#                                              option = 'proxy_https',
#                                              default = None,
#                                              vtype = 'str',
#                                              )
        for k, v in self.proxy.items():
            if v is None:
                del self.proxy[k]
        self.log.debug("Set proxy to %r", self.proxy)
        
    def _get_option(self, section, option, default, vtype = 'str'):
        """ Get the option and set it if it doesn't exist """
        self.log.debug("Going to get/set %r.%r of type %r, default %r", section, option, vtype, default)
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
            self.log.debug("Added section %r to config", section)
        if not self.cfg.has_option(section, option):
            self.cfg.set(section, option, str(default))
            self.log.debug("Added option %r.%r to config with value %r", section, option, default)
        if vtype == 'str' or vtype is None:
            return self.cfg.get(section, option)
        else:
            attr = "get%s" % vtype
            assert hasattr(self.cfg, attr), "Entry type %r doesn't exist (aka ConfigObj.%r)" % (vtype, attr) 
            return getattr(self.cfg, attr)(section, option)
        
