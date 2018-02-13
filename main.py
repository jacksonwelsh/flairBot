#---            Official /r/MurderedByWords bot by /u/jackson1442           ---#
# You are free to use any or all of the content of this bot for your own
# pursposes. You are not required to attrubite this work to me. See more cool
# stuff with extremely specific applications at github.com/jackson1442

import praw, time
# import kdapi
r = praw.Reddit('murderedbybots', user_agent="i don't even know what i'm supposed to put here.")
# poltags = ['[pol]', '[political]', '[politics]', '[politician]']

murderScore = 30
burnScore = -30
modAlert = -50
clearComment = 60
commentText = '''**Please help us decide if this is a murder or a burn.** \n\nIf you believe this post is a murder, please upvote *this comment*. \n\nIf you believe this post is a burn, please downvote *this comment*. \n\nIf you believe this post does not belong on this sub, please downvote *the parent post.* and report it if you think the mods need to see it.\n\n*^^I'm ^^a ^^bot, ^^and ^^this ^^action ^^was ^^performed ^^automatically. ^^If ^^you ^^have ^^any ^^questions, ^^please [^^contact ^^the ^^moderators ^^of ^^this ^^subreddit.](https://www.reddit.com/message/compose?to=%2Fr%2FMurderedByWords&subject=&message=)*\n\n'''
burnComment = commentText + '\n\nThis post has successfully been marked as a `Burn`. This *can* still change, depending on votes.'
murderComment = commentText + '\n\nThis post has successfully been marked as a `Murder`. This *can* still change, depending on votes.'

f = open("logfile.txt", "a+")
#--- comment on new posts, hide from /new ---#
for p in r.subreddit('MurderedByWords').new():
    if time.time() - p.created_utc > 86400: break
   # linktitle = p.title.lower()
   # if any(string in linktitle for string in poltags): p.mod.flair(text='pol')
    c = p.reply(commentText)
    c.mod.distinguish(how='yes', sticky=True)
    c.save()
#--- kd module not working yet ---#
    #similar, lessSimilar = kdapi.check('https://www.reddit.com' + p.permalink,True)
    #for item in lessSimilar:
    #    if item.subreddit == 'MurderedByWords':
    #        print(item.title + "(" + str(item.time) + ") : " + item.link)
    #        f.write('Possible repost of ' + p.permalink + 'found here: ' + item.title + "(" + str(item.time) + ") : " + item.link)
    #        p.report("This post may be a repost of: " item.title + "(" + str(item.time) + ") : " + item.link)
    p.hide()
    print('Commented on post id ' + p.id)
    f.write('\nCommented on post ' + p.permalink)
    c.clear_vote()
#--- check for unapproved posts ---#
for u in r.subreddit('MurderedByWords').mod.unmoderated():
    if u.score > 5000:
        tempRemovalMessage = 'Greetings, '+str(u.author)+'! Your [post]('+u.permalink+') on /r/MurderedByWords has been temporarily removed so a moderator can review it. This prevents low quality content from making the frontpage.\n\nThe moderators have been notified of this action, and will reinstate your post if it belongs here. You will receive a reply regardless of the decision.\n\nIf you have any questions, please [send the moderators a message](https://www.reddit.com/message/compose?to=%2Fr%2FMurderedByWords&subject=Question+about+the+temporary+removal+of+a+post&message= '+u.permalink+') **do not send me a message, because I am a bot.**'
        r.subreddit('MurderedByWords').modmail.create('Post temporarily removed', tempRemovalMessage, str(u.author))
        c = u.reply(tempRemovalMessage)
        c.mod.distinguish(how='yes', sticky=True)
        u.mod.remove()
        u.report("Temporarily removed due to upvotes with no approval. Please verify.")
        print('temporarily removed post ' + u.permalink)
        f.write('\nRemoved post ' + u.permalink + ' temporarily for review')
time.sleep(10)
#--- Sort through previously made comments, flair/edit accordingly. ---#
for c in r.redditor('murderedbybots').saved():
    print(c.parent().permalink)
    if time.time() - c.created_utc > 423000: c.parent().mod.flair(text="Burn"); c.delete(); continue
    if c.stickied != True: c.delete(); continue
    if c.author != 'murderedbybots': continue
    if c.parent().author == '[deleted]': c.delete(); continue
    if c.score > murderScore:
        if c.parent().flair != 'Murder': c.parent().mod.flair(text='Murder'); f.write('\nFlaired post ' + c.parent().permalink + ' as Murder')
        if c.body != murderComment: c.edit(murderComment)
        if c.score > clearComment: c.delete()
    elif c.score < burnScore:
        if c.parent().flair != 'Burn': c.parent().mod.flair(text='Burn'); f.write('\nFlaired post ' + c.parent().permalink + ' as Burn')
        if c.body != burnComment: c.edit(burnComment)
        if c.score < modAlert:
            #--- temporarily disabled modmail feature because it was blowing up and annoying ---#
            # r.subreddit('MurderedByWords').message('Possible LQ content alert', 'The following post has been marked as a burn with a *very* low score.\n\nPlease investigate at your convenience.\n\n' + c.parent().permalink)
            c.parent().report("Potential low quality content, overwhelmingly voted as burn.")
            f.write('\nReported post ' + c.parent().permalink + ' as potential low quality')
            c.delete()
    else: continue
    print(c.parent().permalink)
f.close()
exit()
