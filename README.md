FourChapy
=====
A simple library for accessing 4chan's JSON API.  


Simple Example Using Python 2.6 Built-in Libraries
-----
	# Import standard libraries 
	from urllib import urlopen
	from json import loads
	from pprint import pprint
	# Open the thread's JSON data URL and read data from the connection
	f=urlopen(url = '%s://api.4chan.org/%s/res/%d.json' % ('http', 'diy', 12345))
	data=f.read()
	f.close()
	# Convert JSON into Python data structures
	decoded=loads(data)
	# Display the data
	pprint(decoded)


Using 4chapy
-----
	# Import the library
	from Fourchapy import FourchapyThread
	# Download a thread from diy with an ID of 12345
	t = FourchapyThread(boardID = 'diy', threadID = 12345)
	# Loop over all posts in the thread and print out info from the post
	for post in t.Posts:
		print "--- %d ---"%post.Number
		print "Subject: %s"%post.Subject
		print "Comment: %s"%post.Comment
		
		
4chapy Testing Steps
-----
	1) Copy "Test.conf.ini.sample" to "Test.conf.ini"
	2) Edit "Test.conf.ini"
		a) Update the threadID with the thread ID number from current threads
		b) Optionally, change what board is being used
		c) Optionally, change the loggingLevel. The logging module's DEBUG, INFO, 
			and other level variables will give the meaning of different values. 
		d) Optionally, Add additional sections with other threads to repeat a test.  
	3) Run "Test.py". No arguments are required. 
	4) If logging is set at or below INFO, a table will be displayed that shows
		the results of the different tests.  


TODO
-----
1.  Change Test.py over to unit tests or something more standard, less stupid. 
