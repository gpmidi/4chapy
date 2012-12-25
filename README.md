FourChapy
=====
A simple library for accessing 4chan's JSON API.  


Using 4chapy
-----
From the bottom up: 
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
    
If you know the board and thread you want: 
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
2.  Edit "Test.conf.ini"
	a) Update the threadID with the thread ID number from current threads
	b) Optionally, change what board is being used
	c) Optionally, change the loggingLevel. The logging module's DEBUG, INFO, 
		and other level variables will give the meaning of different values. 
	d) Optionally, Add additional sections with other threads to repeat a test.  
3.  Run "Test.py". No arguments are required. 
4.  If logging is set at or below INFO, a table will be displayed that shows
	the results of the different tests.  
5.  Reimplement this as unit tests. 


TODO
-----
1.  Change Test.py over to unit tests or something more standard, less stupid. 
