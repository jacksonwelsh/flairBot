# redditBot

A reddit bot created to help moderate [/r/MurderedByWords](https://reddit.com/r/MurderedByWords)

## Features

Currently, the bot is able to:

* Automatically comment on every new post
* Flair posts based on the score of the comment
* Report posts based on the score of that comment
* Remove posts that receive high numbers of upvotes and haven't been approved.
* Log all actions in a separate text file.

## FAQ

There is currently a short FAQ hosted [here](https://www.reddit.com/r/1442dump/wiki/murderedbybots-faq)

## Getting Started

Alright! Now that the bot is universalized, we can get the show on the road!

1. Clone the repo. Simply type `git clone https://github.com/jackson1442/redditBot` where you want this directory.

2. Open `botconfig.ini`. Change all the values in there to what you want them to be. If you need something to be blank (like special notices), just put in `\n`in the blank. **Do not leave fields blank!**

3. Then, after all that is done, change the file name of `samplelogin.ini` to `praw.ini`.

3. Create a reddit app. Go [here](https://www.reddit.com/prefs/apps/)
    * scroll to the bottom and select "Create another app...".
    * Make up a name and description and select `script`.
    * Set the redirect url to `http://127.0.0.1`
    * Add your bot account as a developer
    * Inset the public and secret keys into `praw.ini`.
    * Insert your username and password into `praw.ini`. (you can't have 2FA on)
    * **DO NOT UPLOAD CONFIG.INI TO THE INTERNET, NOW OR EVER!!!** Keep this stored locally.

5. Run it! The main file is main.py, it'll create a log for you. Based on your system, you can set it as a scheduled job to run main.py every x minutes. For cron on linux systems, you'll want to use launcher.sh.
