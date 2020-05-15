import * as fs from 'fs';
import * as yaml from 'js-yaml';

const ruleFile : string = process.env.RULE_FILE || 'rules.yml'

export interface ruleInterface {
    subreddit : string,
    type: string,
    titles: string[],
    bodies: string[],
    comments?: string[],
    every: number
}


function getRuleYaml(): any {
    try {
        return yaml.safeLoad(fs.readFileSync(ruleFile).toString())
    } catch (err) {
        console.log(`[FATAL] Error while reading rule file: ${err}`)
        process.exit(1)
    }
}

export async function parseRules(callback : any) {
    var rules = getRuleYaml();
    for (var rule in rules['rules']) {
        var IRule : ruleInterface = {
            type: rules['rules'][rule]['type'],
            subreddit: rules['rules'][rule]['subreddit'],
            titles: rules['rules'][rule]['titles'],
            bodies: rules['rules'][rule]['bodies'],
            comments: rules['rules'][rule]['comments'],
            every: rules['rules'][rule]['every']
        }
        await callback(IRule);
    }
    return true;
}

export function validateRules() : boolean {
    var rules = getRuleYaml();
    for (var rule in rules['rules']) {
        if (!ruleValid(rules['rules'][rule])) {
            return false;
        }
    }
    return true;
}

function ruleValid(rule: any) {
    if (rule == null) {
        return false
    } else {
        if (!('subreddit' in rule) || !('titles' in rule) || !('bodies' in rule) || !('every' in rule) || !('type' in rule)) {
            return false
        }

        if (rule['subreddit'] === null || rule['titles'] === null || rule['bodies'] === null || rule['every'] === null || rule['type'] === null) {
            return false
        }

        if (rule['type'] === 'text' || rule['type'] === 'link') {
            return true
        }
    }
}