#---            Official /r/MurderedByWords bot by /u/jackson1442           ---#
# You are free to use any or all of the content of this bot for your own
# pursposes. You are not required to attrubite this work to me. See more cool
# stuff with extremely specific applications at github.com/jackson1442
import praw, time, ConfigParser

Config = ConfigParser.ConfigParser()
print(Config.read("botconfig.ini"))
nextline = "\n\n"


def getstring(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

accountName = Config.get("basics", 'account name')
# import kdapi
r = praw.Reddit('murderedbybots', user_agent="trying this garbage again")
# poltags = ['[pol]', '[political]', '[politics]', '[politician]']

def uniqid():
    return hex(int(time.time()*10000000))[2:17]

currentSubreddit = Config.get("basics", 'subreddit')
print(currentSubreddit)
logsub = Config.get("logging", 'logsub')

scoreA = Config.getint("flairing", "flair a")
scoreB = Config.getint("flairing", "flair b")

removeB = Config.getint("flairing", "remove b")
removeA = Config.getint("flairing", "remove a")

commentText = Config.get("basics", 'autocomment').decode("string-escape")
commentA = commentText + Config.get("flairing", 'flair success a').decode("string-escape")
commentB = commentText + Config.get("flairing", 'flair success b').decode("string-escape")

nameA = Config.get("flairing", 'flair a name')
classA = Config.get("flairing", 'flair a class')
nameB = Config.get("flairing", 'flair b name')
classB = Config.get("flairing", 'flair b class')

footer = Config.get("basics", 'footer').decode("string-escape")
notice1 = Config.get("notices", 'message 1').decode("string-escape")
notice2 = Config.get("notices", 'message 2').decode("string-escape")

if time.time() < Config.getint("notices", "timestamp 1"):
    specialNotice = notice1
else:
    specialNotice = ""
if time.time() < Config.getint("notices", "timestamp 2"):
    specialNotice += notice2

f = open("logfile.txt", "a+")
#--- comment on new posts, hide from /new ---#
for p in r.subreddit(currentSubreddit).new():
    actionID = uniqid()
    lp = r.subreddit(logsub).submit(actionID + ' - Commented on post "' + p.title[:50] + '"', url='https://reddit.com' + p.permalink)
    lp.mod.lock()
    if time.time() - p.created_utc > 86400: break
    c = p.reply(commentText + specialNotice + footer + '['+actionID+']('+lp.permalink+')')
    c.mod.distinguish(how='yes', sticky=True)
    c.save()
    p.hide()
    print('Commented on post id ' + p.id)
    f.write('\nCommented on post ' + p.permalink + ' - ' + actionID)
    c.clear_vote()
    lp.mod.approve()
#--- check for unapproved posts ---#
if Config.getboolean("approval", "required"):
    for u in r.subreddit(currentSubreddit).mod.unmoderated():
        if u.score > Config.getint("approval", "threshold"):
            link = u.permalink
            author = str(u.author)
            actionID = uniqid()
            lp = r.subreddit(logsub).submit(actionID + ' - Temporarily removed post "' + u.title[:50] + '"', url='https://reddit.com' + u.permalink)
            lp.mod.lock()
            tempRemovalMessage = Config.get("approval", 'comment')
            r.subreddit(currentSubreddit).modmail.create('Post temporarily removed', tempRemovalMessage + footer + '['+actionID+']('+lp.permalink+')', str(u.author))
            c = u.reply(tempRemovalMessage + footer + '['+actionID+']('+lp.permalink+')')
            c.mod.distinguish(how='yes', sticky=True)
            u.mod.remove()
            u.report("Temporarily removed due to upvotes with no approval. Please verify.")
            print('temporarily removed post ' + u.permalink)
            f.write('\nRemoved post ' + u.permalink + ' temporarily for review - ' + actionID)
            lp.mod.approve()

time.sleep(10)
#--- Sort through previously made comments, flair/edit accordingly. ---#
for c in r.redditor(accountName).saved():
    currentComment = c.body.split('#')[0]
    print currentComment
    actionID = uniqid()
    print(c.parent().permalink)
    if time.time() - c.created_utc > 423000:
        c.parent().mod.flair(text=nameB, css_class=classB)
        r.subreddit(logsub).submit(actionID + ' - Flaired post "' + c.parent().title[:50] + '" as ' + nameB + ' (auto-old)', url='https://reddit.com' + c.parent().permalink).mod.lock()
        c.delete()
        continue
    if c.stickied != True: c.delete(); continue
    if c.author != accountName: continue
    if c.parent().author == '[deleted]': c.delete(); continue

    if c.score > scoreA:
        if currentComment != commentA + footer[-1]:
            lp = r.subreddit(logsub).submit(actionID + ' - Flaired post "' + c.parent().title[:50] + '"... as ' + nameA, url='https://reddit.com' + c.parent().permalink)
            lp.mod.lock()
            c.edit(commentA + specialNotice + footer + '['+actionID+']('+lp.permalink+')')
            c.parent().mod.flair(text=nameA, css_class=classA)
            f.write('\nFlaired post ' + c.parent().permalink + ' as ' + nameA + ' - ' + actionID)
            lp.mod.approve()

        if c.score > removeA: c.delete()

    elif c.score < scoreA:
        if currentComment != commentB + footer[-1]:
            lp = r.subreddit(logsub).submit(actionID + ' - Flaired post "' + c.parent().title[:50] + '"... as ' + nameB, url='https://reddit.com' + c.parent().permalink)
            lp.mod.lock()
            c.edit(commentB + specialNotice + footer + '['+actionID+']('+lp.permalink+')')
            c.parent().mod.flair(text=nameB, css_class=classB);
            f.write('\nFlaired post ' + c.parent().permalink + ' as ' + nameB + ' - ' + actionID)
            lp.mod.approve()

        if (c.score < removeB) and Config.getboolean("flairing", "report"):
            c.parent().report(Config.get("flairing", 'reason') + actionID)
            f.write('\nReported post ' + c.parent().permalink + ' as potential low quality - ' + actionID)
            r.subreddit(logsub).submit(actionID + ' - Reported post "' + c.parent().title[:50] + '" as potential LQ', url='https://reddit.com' + c.parent().permalink).mod.lock()
            c.delete()
    else: continue
    print(c.parent().permalink)
f.close()
exit()
