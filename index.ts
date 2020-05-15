import { validateRules, parseRules, ruleInterface } from './rules';
import { digest, auth} from './reddit';

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

 if (!auth()) {
    console.log('[FATAL] Missing required environment variables for authentication.');
    process.exit(1);
 } else {
    parseRules(test);
 }
