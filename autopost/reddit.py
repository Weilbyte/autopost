import os
import sys
import random
import time

import praw

def environVarPresent():
    """
    Checks if the required environment variables are present

    Returns:
    bool: True if present, otherwise False
    """
    if (os.environ.get('USER_AGENT') == None) or (os.environ.get('CLIENT_ID') == None) or (os.environ.get('CLIENT_SECRET') == None) or (os.environ.get('USERNAME') == None) or (os.environ.get('PASSWORD') == None):
        return False
    return True

def getInstance():
    """
    Creates an instance of praw.Reddit

    Returns:
    reddit: The created instance
    """
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
    """
    Processes the rule.

    Parameters:
    rule (dict): The rule to be processed
    """
    redditInstance = getInstance()
    time.sleep(2)
    setFlairID(redditInstance, rule)

    submission = submit(redditInstance, rule)
    print(f'Submission {submission} sent to r/{rule.subreddit}')

    reply(redditInstance, rule, submission)

def submit(redditInstance, rule):
    """
    Submits rule post to subreddit.

    Parameters:
    redditInstance (Reddit): The Reddit instance to use
    rule (dict): The rule to base the post on

    Returns:
    Submission: The resulting submission
    """
    if (rule.kind == 'text'):
        return redditInstance.subreddit(rule.subreddit).submit(title=random.choice(rule.titles), selftext=random.choice(rule.bodies), flair_id=rule.flair)
    else:
        return redditInstance.subreddit(rule.subreddit).submit(title=random.choice(rule.titles), url=random.choice(rule.bodies), flair_id=rule.flair)

def setFlairID(redditInstance, rule):
    """
    Sets rule flair.

    If rule.flair is either None or a flair ID then it doesn't change anything.
    Otherwise if rule.flair is flair text then it looks through the subreddits flairs and tries to find a flair text the same as rule.flair.
    When found, it sets rule.flair to the flair's ID.

    Parameters:
    redditInstance (Reddit): The Reddit instance to use
    rule (dict): The rule to set flair ID for
    """
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
    """
    Replies to a submission.

    It replies to the submission with a random comment from rule.comments (if it is not None).

    Parameters:
    redditInstance (Reddit): The Reddit instance to use
    rule (dict): The rule to fetch comments from
    submission (Submission): The submission to reply to
    """
    if (rule.comments is not None):
        time.sleep(4.272188888122201229) # Required for bypassing Reddit spam filter
        reply = submission.reply(random.choice(rule.comments))
        print(f'Reply {reply} sent to {submission}')