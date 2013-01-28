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
''' The base class for all objects that fetch data
Created on Jan 27, 2013

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''

from apiclient import APIClient, RateLimiter, MemcachdCacher

class FourChanFetcher(APIClient):
    # Base URLs to use for API requests
    BASE_URL_HTTP = "http://api.4chan.org/"
    BASE_URL_HTTPS = "https://api.4chan.org/"
    # Base URLs for fetching images
    BASE_URL_HTTP_IMG = "http://images.4chan.org/"
    BASE_URL_HTTPS_IMG = "https://images.4chan.org/"
    # Base URLs for fetching thumbnails of images
    BASE_URL_HTTP_THUMB = "http://thumbs.4chan.org/"
    BASE_URL_HTTPS_THUMB = "https://thumbs.4chan.org/"
    # The MAX_REQUESTS per MAX_REQUESTS_SECONDS seconds 
    # Set MAX_REQUESTS to None to completely disable
    MAX_REQUESTS = 10
    MAX_REQUESTS_SECONDS = 10
    # When we are going over the rate limit, we should sleep 
    # rather than immediately raise an error. Only used if
    # MAX_REQUESTS is not None.  
    shouldSleep = True
    
    
    def __init__(self, proto = "HTTP", proxies = {}, sleep = None, memcachedServers = []):
        """
        @param proto: HTTP or HTTPS to indicate if SSL should be used or not.  
        @param proxies: A dict of protocol:url strings that indicate what proxy to use
        when accessing a given protocol. Ex: 
        proxies=dict(http="http://p1.someproxy.com:3128",https="http://p2.someproxy.com:3128") 
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-method and/or per-class shouldSleep value.       
        @param memcachedServers: A list or tuple of strings. Each string should have a 
        memcached server listed as "<hostname|IP>:<port>". Alternatively, each element in the
        list may be a tuple of ("<hostname|IP>:<port>",weight).  
        """
        if proto.lower() == "https":
            self.BASE_URL = self.BASE_URL_HTTPS
        elif proto.lower() == "http":
            self.BASE_URL = self.BASE_URL_HTTP
        else:
            raise ValueError("Expected the protocol to be HTTP or HTTPS, not %r" % proto)
        if self.MAX_REQUESTS is None:
            rateLimit = None
        else:
            rateLimit = RateLimiter(
                                    max_messages = 10,
                                    every_seconds = 1,
                                    )
        if sleep is None:
            self.shouldSleep = sleep
        # Enable distributed caching of all data we fetch
        if len(memcachedServers) > 0:
            cache = MemcachdCacher(servers = memcachedServers)
        else:
            cache = None 
        APIClient.__init__(
                           self = self,
                           rate_limit_lock = rateLimit,
                           cache = cache,
                           )
        
        
        
        
