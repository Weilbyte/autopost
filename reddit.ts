import * as snoowrap from 'snoowrap';
import { ruleInterface } from './rules';

var redditBot = undefined

export function auth() {
    if (process.env.USER_AGENT == null || process.env.CLIENT_ID == null || process.env.CLIENT_SECRET == null || process.env.USERNAME == null || process.env.PASSWORD == null ) {
        return false;
    };

    redditBot = new snoowrap({
        userAgent: process.env.USER_AGENT,
        clientId: process.env.CLIENT_ID,
        clientSecret: process.env.CLIENT_SECRET,
        username: process.env.USERNAME,
        password: process.env.PASSWORD
    });
    return true;
}

function getRandom(array) {
    return array[Math.floor(Math.random() * array.length)]
}

export function digest(rule : ruleInterface) {
    if (rule.type == 'text') {
        submitText(rule)
    } else if (rule.type == 'link') {
        submitLink(rule)
    }
}

function submitText(rule : ruleInterface) {
    redditBot.submitSelfpost({subredditName: rule.subreddit, title: getRandom(rule.titles), text: getRandom(rule.bodies)})
    .then(function(submission) {
        if (rule.comments != null) {
            submission.reply(getRandom(rule.comments)).then(function(replySubmission) {
                console.log(`Submission ${submission.name} has been sent a reply - ${replySubmission.name}`);
            })
        };
        console.log(`A post has been submitted to ${rule.subreddit} (${submission.name}).`);
    })
}

function submitLink(rule : ruleInterface) {
    //@ts-ignore
    redditBot.submitLink({subredditName: rule.subreddit, title: getRandom(rule.titles), url: getRandom(rule.bodies)})
    .then(function(submission) {
        if (rule.comments != null) {
            submission.reply(getRandom(rule.comments)).then(function(replySubmission) {
                console.log(`Submission ${submission.name} has been sent a reply - ${replySubmission.name}`);
            })
        };
        console.log(`A link post has been submitted to ${rule.subreddit} -${submission.name}`);
    })
}

