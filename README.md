FourChapy
=====
A simple library for accessing 4chan's JSON API.  


Features
-----
* Simple and easy to use
* Built-in request rate throttling ensures that you won't accidently get 
your IP banned due to request flooding. See the API rules for details about
max request rates (https://github.com/4chan/4chan-API#api-rules)
* Lazy fetching - The 4chapy API will not try to fetch data from 4chan's
servers until your app requests data that it doesn't already have. This 
helps ensure that your app is not making unnecessary requests which would
slow down your app and increase load on 4chan's servers for no reason. 


Using 4chapy - From the bottom up
-----
	# Import the library
	from Fourchapy import BoardIndex
	# Download a list of all boards and basic info about them (via http)
	b = BoardIndex()
	# Look over the first two boards only
	for board in b.Boards[:2]:
		# Watch out for the unicode
		print u"Board %s (%s)" % (board.Board, board.BoardName)
		if board.SafeForWork:
			print "Safe for work"
		else:
			print "Not safe for work"
		# Get the first two pages only
		for page in board.getPages(maxPage = 1):
			print "Looking at page %d of board %r" % (page.Page, board.Board)
			# Get the first two threads only
			for thread in page.Threads[:2]:
				print "---- Thread %d ----" % thread.Thread
				for post in thread.Posts:
					print "--- %d ---" % post.Number
					print "Subject: %r" % post.Subject
					print "Comment: %r" % post.Comment
	
	
Using 4chapy - If you know the board and thread you want
-----
	# Import the library
	from Fourchapy import Thread
	# Download a thread from diy with an ID of 12345
	t = Thread(boardID = 'diy', threadID = 12345)
	# Loop over all posts in the thread and print out info from the post
	for post in t.Posts:
		print "--- %d ---"%post.Number
		print "Subject: %s"%post.Subject
		print "Comment: %s"%post.Comment


Simple Example Using Only Python 2.6 Built-in Libraries
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
			
		
4chapy Testing Steps
-----
1.  Copy "Test.conf.ini.sample" to "Test.conf.ini"
2.  Edit "Test.conf.ini" and validate that the logging level is 
acceptable. 1=Super Debug, 10=Debug, etc
3.  Edit "Test.conf.ini" and validate that the four RecursiveOptions are 
set low. The number of HTTP(S) requests made to 4chan's servers PER
TEST is the first three values multiplied by each other. 
4.  Run "/src/Fourchapy/tests/__init__.py" with no args. The script's working
directory should be the same folder where "Test.conf.ini" is located. 
