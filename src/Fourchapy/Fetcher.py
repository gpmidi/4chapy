''' Provide a base class that makes it easy to add 
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

from urllib import urlopen
import datetime
from json import loads
import time

from Errors import NoDataReturnedError, RequestRateTooHigh

# Keep track of last request
last = {}

class Fetch4chan(object):
    """ Base class for classes that need to fetch and process data from
    4chan's JSON API. 
    """
    # Min time between requests, in seconds, per calling class
    MinRequestTime = datetime.timedelta(seconds = 1)
    # The URL to fetch
    URL = None
    # All of our attributes that are waiting to be accessed before
    # being populated.     
    lazyAttrs = {}
    # Should override if needing to change globally
    shouldSleep = True
    ignoreRateLimit = False
                     
    def __init__(self, proxies = {}, url = None, sleep = None, ignoreRateLimit = None):
        """
        @param proxies: A dict of protocol:url strings that indicate what proxy to use
        when accessing a given protocol. Ex: 
        proxies=dict(http="http://p1.someproxy.com:3128",http2="http://p2.someproxy.com:3128") 
        @param url: The URL to fetch when requesting data. Must return JSON data. If
        this is a value other than None, it overrides the per-class default URL. 
        Example: url='https://api.4chan.org/board/res/123456.json'         
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-method and/or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-method and/or per-class 
        ignoreRateLimit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions.         
        """
        if sleep is not None:
            self.shouldSleep = sleep
        if ignoreRateLimit is not None:
            self.ignoreRateLimit = ignoreRateLimit
        if self.URL and url:
            log(20, "Overwriting %r with %r" % (self.URL, url))
        if url:
            self.URL = url
        if not self.URL:
            log(40, "No URL defined")
            raise ValueError, "No URL defined"
        self.Proxies = proxies
        # A list of attrs that have been acquired for this object
        self._autoFetched = {}
        
    @classmethod
    def addLazyDataObjDec(cls, attrName):
        """
        @param attrName: The attribute that will be updated with the value 
        update method's return value. The attrName must be unique for a given
        class.
        """
        log(10, "Going to add lazy data object, %r, to %r", attrName, cls)
        def decorator(func):
            def newFunc(self, *args, **kw):
                log(5, 'Running %r', func)
                ret = func(self, *args, **kw)
                setattr(self, attrName, ret)
                return ret
            newFunc.__doc__ = func.__doc__
            # We can use the class attr cls.lazyAttrs because it's a 
            # list for this class as a whole, not individual objects.
            assert attrName not in cls.lazyAttrs 
            cls.lazyAttrs[attrName] = newFunc
            log(10, "Created new func %r and added it to %r", newFunc, cls.lazyAttrs)
            return newFunc
        log(10, "Built decorator %r", decorator)
        return decorator
        
    def __getattr__(self, attr):
        if attr in self.lazyAttrs:
            log(10, "Incoming request for our information via %r.%r", self, attr)
            # Set it to make sure we don't end up back here if the update method
            # doens't set it for some reason. 
            setattr(self, attr, None)
            
            # Make very sure we only run once
            # FIXME: This and the lazy fetching in general will lead to possible race conditions 
            # when this lib is used by multi-threaded code. 
            if attr in self._autoFetched and self._autoFetched[attr]:
                log(50, "We've (%r) already tried to update. We didn't succeed for some reason. Not re-running fetch. ", self)
                raise RuntimeError("Already run an update for %r once on %r- Not running it again. " % (attr, self))    
            self._autoFetched[attr] = True            
            
            # Get the data    
            method = self.lazyAttrs[attr]
            value = method(self)
            log(5, "Got %r from %r on %r", value, method, self)
            
            # Don't need to do this as the decorator does it for us
            # setattr(self, attr, value)
            assert hasattr(self, attr)
            
            # Return the data
            return value
        else:
            raise AttributeError("No such attribute %r" % attr)
    
    def fetchText(self, data = '', sleep = None, ignoreRateLimit = None):
        """ Fetch all data from self.URL
        @param data: A key:value mapping of post data to send with the request 
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-object or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-object or per-class ignore
        rate limit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions.  
        """
        t = type(self).__name__
        if last.has_key(t):
            log(5, "Last request: %r", last[t])
            delta = datetime.datetime.now() - last[t]
            if delta < datetime.timedelta.min:
                log(10, "Time seems to have gone backwards by %r. Letting request proceed as-is. ", delta)
            elif delta < self.MinRequestTime:
                # Time is going forward & we're requesting too quickly
                if ignoreRateLimit or self.ignoreRateLimit:
                    log(20, "Ignoring rate limit! We're requesting too fast. Last request was %r ago. Min normally required is %r. ", delta, self.MinRequestTime)
                elif sleep or (sleep is None and self.shouldSleep):
                    sleepTime = self.MinRequestTime - delta
                    sleepTimeFloat = float((sleepTime.days * 86400) + sleepTime.seconds + (sleepTime.microseconds / 1E6))
                    log(10, "Request rate too high. Sleeping for %r (aka %r seconds). ", sleepTime, sleepTimeFloat)
                    # FIXME: Add in days and microseconds
                    time.sleep(sleepTimeFloat) 
                else:
                    raise RequestRateTooHigh("Request rate is too high. Last request was %r ago. Min time since last request must be %r. " % (delta, self.MinRequestTime))
        else:
            log(5, "First request - No need to rate limit yet. ")
        
        # Record last request dt
        last[t] = datetime.datetime.now()
                
        if data is None:
            data = ''
        elif isinstance(data, dict):
            for k, v in data.items():
                if k is None or v is None:
                    del data[k]
        elif isinstance(data, str):
            pass
        else:
            log.warn("Unknown data value type. Got %r. ", data)
        log(50, "Going to open %r with data %r", self.URL, data)
        fHandle = urlopen(url = self.URL, data = data, proxies = self.Proxies)
        log(10, "Successfully opened url: %r", fHandle)
            
        try:
            log(5, "Starting to read data")
            text = fHandle.read()
            log(10, "Read %d bytes", len(text))
            self._raw_text = text
            return text
        finally:
            fHandle.close()
    
    def fetchJSON(self, data = '', sleep = None, ignoreRateLimit = None):
        """ Fetch all JSON from self.URL and return decoded
        @param data: A key:value mapping of post data to send with the request 
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-object or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-object or per-class ignore
        rate limit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions. 
        """
        log(10, 'Going to fetch %r as JSON', self.URL)
        text = self.fetchText(
                              data = data,
                              sleep = sleep,
                              ignoreRateLimit = ignoreRateLimit,
                              )
        if len(text) == 0:
            raise NoDataReturnedError, "A zero byte file was returned"
        i = 1
        while i * 50 < len(text):
            log(5, 'Fetched data (line %05d): %r' % (i, text[(i - 1) * 50:i * 50]))
            i += 1
        log(10, "Translating JSON into objects")            
        try:
            ret = loads(text)
        except ValueError, e:
            log(30, 'Failed to decode JSON with %r', e)
            log(10, "-"*10 + "Begin Data" + "-"*10)
            for line in text.splitlines():
                log(10, "Line: %r" % line)
            log(10, "-"*10 + "End Data" + "-"*10)
        log(5, 'Decoded %r', ret)
        return ret
