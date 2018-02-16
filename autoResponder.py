# ---                   autoResponder by /u/jackson1442                    --- #
# Automatically responds to any comments pertaining to the removal of content  #
# Licenced with The Unlicense. See licensefile for more details.               # 

import praw

r = praw.Reddit('jackson1442', user_agent="beta v5.2, orange")

for message in r.inbox.unread(limit=5):
    if message.subject == "re: Your submission was removed from /r/MurderedByWords":
        message.reply("Thanks for your message. I am no longer accepting replies to removal messages in my inbox. If you want, you can [send the moderators a message](https://www.reddit.com/message/compose?to=%2Fr%2FMurderedByWords&subject=&message=) or [chat in the discord](https://discord.gg/Fe3eUb6) about this. Be sure to include a link so we can find your post.\n\nThis message has been deleted and will not be replied to.")
        message.mark_read()

exit()
