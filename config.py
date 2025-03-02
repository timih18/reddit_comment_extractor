import praw


reddit = praw.Reddit(client_id = 'CLIENT_ID',
                     client_secret = 'CLIENT_SECRET',
                     usertname = 'USERNAME',
                     password = 'PASSWORD',
                     user_agent = 'Comment Extraction',
                     chache_timeout = 0)

post = 'POST_ID'
