import { validateRules, parseRules, ruleInterface } from './rules';
import { digest} from './reddit';

if (!validateRules()) {
    console.log('[FATAL] Please ensure all rules are formatted properly.') 
    process.exit(1);
} 

async function test(rule : ruleInterface) {
    setInterval(() => {
        console.log(`Digesting scheldued rule for ${rule.subreddit}`)
        digest(rule)
    }, rule.every)
}

parseRules(test);