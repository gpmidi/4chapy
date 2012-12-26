'''
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import unittest
from Fourchapy.tests.BoardPages import BoardPageConfigBasedTests

class PostTestSequence(BoardPageConfigBasedTests):

    def testPostObjs(self):
        for boardID, info in self.boardPages.items():
            self.log.log(5, "Looking at board %r", boardID)
            for pageNumber, page in info['pages'].items():
                self.log.log(5, "Looking at page %r", page)
                for threadID, thread in page.ThreadsDict.items()[:self.recursionMaxThreads]:
                    self.log.log(4, "Looking at thread %r", thread)
                    for postID, post in thread.PostsDict.items()[:self.recursionMaxPosts]:
                        self.log.log(3, "Looking at post %r", post)
                        # Basic attributes tests
                        self.assertTrue(isinstance(post.Index, int) or post.Index is None, "The post index should be an int")
                        self.assertTrue(isinstance(post.Board, (str, unicode)), "The board ID string should be a str")
                        self.assertTrue(isinstance(post.Proto, (str, unicode)), "The protocol should be a str")
                        self.assertTrue(post.Proto.lower() in ['http', 'https'], "Proto %r isn't http or https" % post.Proto)

                        
                        # Bulk attr tests - Make sure things don't change by accident
                        # Attr tests for PostObj.Sticky
                        self.assertTrue(hasattr(post, 'Sticky'), 'Sticky should be defined')
                        self.assertTrue(isinstance(post.Sticky, bool) or post.Sticky is None, 'Sticky should be bool based')
                        
                        # Attr tests for PostObj.CustomSpoiler
                        self.assertTrue(hasattr(post, 'CustomSpoiler'), 'CustomSpoiler should be defined')
                        self.assertTrue(isinstance(post.CustomSpoiler, int) or post.CustomSpoiler is None, 'CustomSpoiler should be int based')
                        
                        # Attr tests for PostObj.UserType
                        self.assertTrue(hasattr(post, 'UserType'), 'UserType should be defined')
                        self.assertTrue(isinstance(post.UserType, unicode) or post.UserType is None, 'UserType should be unicode based')
                        
                        # Attr tests for PostObj.Subject
                        self.assertTrue(hasattr(post, 'Subject'), 'Subject should be defined')
                        self.assertTrue(isinstance(post.Subject, unicode) or post.Subject is None, 'Subject should be unicode based')
                        
                        # Attr tests for PostObj.Number
                        self.assertTrue(hasattr(post, 'Number'), 'Number should be defined')
                        self.assertTrue(isinstance(post.Number, int) or post.Number is None, 'Number should be int based')
                        
                        # Attr tests for PostObj.Tripcode
                        self.assertTrue(hasattr(post, 'Tripcode'), 'Tripcode should be defined')
                        self.assertTrue(isinstance(post.Tripcode, unicode) or post.Tripcode is None, 'Tripcode should be unicode based')
                        
                        # Attr tests for PostObj.FileSize
                        self.assertTrue(hasattr(post, 'FileSize'), 'FileSize should be defined')
                        self.assertTrue(isinstance(post.FileSize, int) or post.FileSize is None, 'FileSize should be int based')
                        
                        # Attr tests for PostObj.OrgFilename
                        self.assertTrue(hasattr(post, 'OrgFilename'), 'OrgFilename should be defined')
                        self.assertTrue(isinstance(post.OrgFilename, unicode) or post.OrgFilename is None, 'OrgFilename should be unicode based')
                        
                        # Attr tests for PostObj.RenamedFilename
                        self.assertTrue(hasattr(post, 'RenamedFilename'), 'RenamedFilename should be defined')
                        self.assertTrue(isinstance(post.RenamedFilename, int) or post.RenamedFilename is None, 'RenamedFilename should be int based')
                        
                        # Attr tests for PostObj.Closed
                        self.assertTrue(hasattr(post, 'Closed'), 'Closed should be defined')
                        self.assertTrue(isinstance(post.Closed, bool) or post.Closed is None, 'Closed should be bool based')
                        
                        # Attr tests for PostObj.CountryName
                        self.assertTrue(hasattr(post, 'CountryName'), 'CountryName should be defined')
                        self.assertTrue(isinstance(post.CountryName, unicode) or post.CountryName is None, 'CountryName should be unicode based')
                        
                        # Attr tests for PostObj.ThumbnailHeight
                        self.assertTrue(hasattr(post, 'ThumbnailHeight'), 'ThumbnailHeight should be defined')
                        self.assertTrue(isinstance(post.ThumbnailHeight, int) or post.ThumbnailHeight is None, 'ThumbnailHeight should be int based')
                        
                        # Attr tests for PostObj.Email
                        self.assertTrue(hasattr(post, 'Email'), 'Email should be defined')
                        self.assertTrue(isinstance(post.Email, unicode) or post.Email is None, 'Email should be unicode based')
                        
                        # Attr tests for PostObj.UnixDateTime
                        self.assertTrue(hasattr(post, 'UnixDateTime'), 'UnixDateTime should be defined')
                        self.assertTrue(isinstance(post.UnixDateTime, int) or post.UnixDateTime is None, 'UnixDateTime should be int based')
                        
                        # Attr tests for PostObj.FileDeleted
                        self.assertTrue(hasattr(post, 'FileDeleted'), 'FileDeleted should be defined')
                        self.assertTrue(isinstance(post.FileDeleted, bool) or post.FileDeleted is None, 'FileDeleted should be bool based')
                        
                        # Attr tests for PostObj.DateTime
                        self.assertTrue(hasattr(post, 'DateTime'), 'DateTime should be defined')
                        self.assertTrue(isinstance(post.DateTime, unicode) or post.DateTime is None, 'DateTime should be unicode based')
                        
                        # Attr tests for PostObj.MD5
                        self.assertTrue(hasattr(post, 'MD5'), 'MD5 should be defined')
                        self.assertTrue(isinstance(post.MD5, unicode) or post.MD5 is None, 'MD5 should be unicode based')
                        
                        # Attr tests for PostObj.SpoilerImage
                        self.assertTrue(hasattr(post, 'SpoilerImage'), 'SpoilerImage should be defined')
                        self.assertTrue(isinstance(post.SpoilerImage, bool) or post.SpoilerImage is None, 'SpoilerImage should be bool based')
                        
                        # Attr tests for PostObj.Name
                        self.assertTrue(hasattr(post, 'Name'), 'Name should be defined')
                        self.assertTrue(isinstance(post.Name, unicode) or post.Name is None, 'Name should be unicode based')
                        
                        # Attr tests for PostObj.ThumbnailWidth
                        self.assertTrue(hasattr(post, 'ThumbnailWidth'), 'ThumbnailWidth should be defined')
                        self.assertTrue(isinstance(post.ThumbnailWidth, int) or post.ThumbnailWidth is None, 'ThumbnailWidth should be int based')
                        
                        # Attr tests for PostObj.ImageHeight
                        self.assertTrue(hasattr(post, 'ImageHeight'), 'ImageHeight should be defined')
                        self.assertTrue(isinstance(post.ImageHeight, int) or post.ImageHeight is None, 'ImageHeight should be int based')
                        
                        # Attr tests for PostObj.FileExtension
                        self.assertTrue(hasattr(post, 'FileExtension'), 'FileExtension should be defined')
                        self.assertTrue(isinstance(post.FileExtension, unicode) or post.FileExtension is None, 'FileExtension should be unicode based')
                        
                        # Attr tests for PostObj.ReplyTo
                        self.assertTrue(hasattr(post, 'ReplyTo'), 'ReplyTo should be defined')
                        self.assertTrue(isinstance(post.ReplyTo, int) or post.ReplyTo is None, 'ReplyTo should be int based')
                        
                        # Attr tests for PostObj.ImageWidth
                        self.assertTrue(hasattr(post, 'ImageWidth'), 'ImageWidth should be defined')
                        self.assertTrue(isinstance(post.ImageWidth, int) or post.ImageWidth is None, 'ImageWidth should be int based')
                        
                        # Attr tests for PostObj.CountryCode
                        self.assertTrue(hasattr(post, 'CountryCode'), 'CountryCode should be defined')
                        self.assertTrue(isinstance(post.CountryCode, unicode) or post.CountryCode is None, 'CountryCode should be unicode based')
                        
                        # Attr tests for PostObj.Capcode
                        self.assertTrue(hasattr(post, 'Capcode'), 'Capcode should be defined')
                        self.assertTrue(isinstance(post.Capcode, unicode) or post.Capcode is None, 'Capcode should be unicode based')
                        
                        # Attr tests for PostObj.Comment
                        self.assertTrue(hasattr(post, 'Comment'), 'Comment should be defined')
                        self.assertTrue(isinstance(post.Comment, unicode) or post.Comment is None, 'Comment should be unicode based')
