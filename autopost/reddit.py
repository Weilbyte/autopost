import os
import sys 
import random
import time

import praw 

# TODO Add documentation to functions here

def environVarPresent():
    if (os.environ.get('USER_AGENT') == None) or (os.environ.get('CLIENT_ID') == None) or (os.environ.get('CLIENT_SECRET') == None) or (os.environ.get('USERNAME') == None) or (os.environ.get('PASSWORD') == None):
        return False 
    return True

def getInstance():
    if not environVarPresent():
        sys.exit('[FATAL] Missing required authentication environment variables.')
    redditInstance = praw.Reddit(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        user_agent=os.environ.get('USER_AGENT'),
        username=os.environ.get('USERNAME'),
        password=os.environ.get('PASSWORD')
    )
    return redditInstance

def digest(rule):
    redditInstance = getInstance()
    time.sleep(2)
    setFlairID(redditInstance, rule)

    submission = submit(redditInstance, rule)
    print(f'Submission {submission} sent to r/{rule.subreddit}')

    reply(redditInstance, rule, submission)

def submit(redditInstance, rule):
    if (rule.kind == 'text'):
        return redditInstance.subreddit(rule.subreddit).submit(title=random.choice(rule.titles), selftext=random.choice(rule.bodies), flair_id=rule.flair)
    else:
        return redditInstance.subreddit(rule.subreddit).submit(title=random.choice(rule.titles), url=random.choice(rule.bodies), flair_id=rule.flair)

def setFlairID(redditInstance, rule):
    if (rule.flair is not None):
        if (len(rule.flair) > 15) and ('-' in rule.flair):
            return
        else:
            templates = redditInstance.subreddit(rule.subreddit).flair.link_templates
            for template in templates:
                if (template['text'] == rule.flair):
                    rule.flair = template['id']
                    return
        sys.exit(f'[FATAL] Could not find flair id for {rule.flair} in r/{rule.subreddit}')

def reply(redditInstance, rule, submission):
    if (rule.comments is not None):
        time.sleep(4.272188888122201229) # Required for bypassing Reddit spam filter
        reply = submission.reply(random.choice(rule.comments))
        print(f'Reply {reply} sent to {submission}')