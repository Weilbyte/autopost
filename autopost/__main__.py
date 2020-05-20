import sys

import rules as rules
import scheduler as scheduler

def index(args):
    if len(args) == 1:
        sys.exit('[FATAL] Missing rule file parameter.')
    ruleYAML = rules.getYAML(args[1])
    if not (rules.validateRules(ruleYAML)):
        sys.exit('[FATAL] Please ensure all rules are formatted properly.')
    rules.parseRules(ruleYAML, scheduler.scheduleRule)

if __name__ == '__main__':
    index(sys.argv)