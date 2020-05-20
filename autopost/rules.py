import yaml

class Rule:
    """Rule object."""
    def __init__(self, subreddit, kind, titles, bodies, comments, flair, every):
        """Initializes a Rule class."""
        self.subreddit = subreddit
        self.kind = kind
        self.titles = titles
        self.bodies = bodies
        self.comments = comments
        self.flair = flair
        self.every = every

def parseRules(rules, callback):
    """
    Parses rules into interfaces and provides them as arg to callback.

    Parameters:
    rules (dict): Rules YAML dict
    callback (func): Callback to call with rule interfaces
    """
    for rule in rules['rules']:
        IRule = Rule(
            rules['rules'][rule]['subreddit'],
            rules['rules'][rule]['kind'],
            rules['rules'][rule]['titles'],
            rules['rules'][rule]['bodies'],
            rules['rules'][rule]['comments'],
            rules['rules'][rule]['flair'],
            rules['rules'][rule]['every']
        )
        callback(IRule)

def validateRules(rules):
    """
    Valiates the YAML rules file.

    Parameters:
    rules (dict): Rules YAML dict

    Returns:
    bool: False if invalid rules are present, otherwise True.
    """
    for rule in rules['rules']:
        if not ruleValid(rules['rules'][rule]):
            return False
    return True

def ruleValid(rule):
    """
    Checks whether or not a rule has all required properties.

    Parameters:
    rule (dict): A single rule

    Returns:
    bool: False if rule does not meet requirements, otherwise True
    """
    if rule == None:
        return False
    if not ('subreddit' in rule) or not ('titles' in rule) or not ('bodies' in rule) or not ('every' in rule) or not ('kind' in rule):
        return False
    if (rule['subreddit'] == None) or (rule['titles'] == None) or (rule['bodies'] == None) or (rule['every'] == None) or (rule['kind'] == None):
        return False

    if (rule['kind'] == 'text' or rule['kind'] == 'link'):
        return True

def getYAML(file):
    """
    Returns loaded YAML from a file.

    Parameters:
    file (string): Path to the YAML file

    Returns:
    dict: The loaded YAML
    """
    try:
        with open(file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as err:
                exit(f'[FATAL] Unexpected YAML error: {err}')
    except FileNotFoundError:
        exit(f'[FATAL] File {file} could not be found.')