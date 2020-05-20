import threading 

import reddit as reddit

def scheduleRule(rule):
    """
    Schedules a rule to run every X seconds

    Parameters:
    rule (class): Rule to be scheduled
    """
    def run():
        reddit.digest(rule)
        scheduleRule(rule)
    threading.Timer(rule.every, run).start()
