#!/usr/bin/env python
"""
Pyhton script for a unix system.

A quick scanner to parse the Logophilia subreddit 
and dump the definitions from the top submissions.

First 100 by default.

Please change the USER_AGENT if you use or modify this yourself.

Requires the "praw" package which is on pypi:
easy_install praw
OR
pip install praw

"""

USER_AGENT = 'logophilia-scanner by joezuntz'
SUBREDDIT = 'logophilia'
NUMBER_SUBMISSIONS = 100

#
import praw
import codecs

# load up reddit
reddit = praw.Reddit(user_agent=USER_AGENT)

# go to the correct subreddit and line up the top 100 submissions
logophilia = reddit.get_subreddit(SUBREDDIT)
top = logophilia.get_top_from_all(limit=NUMBER_SUBMISSIONS)

#we want to record both the valid and badly formed ones,
#so make lists (empty to start with) for both
invalid_submissions = []
valid_submissions = []

#go through each of the top submissions in order
for submission in top:
	# try parsing into the standard logophilia form - a colon separating
	# the word and definition
	try:
		word, definition = submission.title.split(':', max_split=1)
	#some of the top 100 are not in the correct form.
	#record them but then just ignore.
	except ValueError:
		invalid_submissions.append(submission)
		continue
	# Get the reddit user who submitted the post.
	# For some reason some posts do not record this.
	# Probably deleted users?  Or maybe really old ones.
	# Not sure, but if not found just use "???"
	try:
		submitter = submission.author.name
	except AttributeError:
		submitter = '???'

	#Record this entry to our list
	valid_submissions.append((word, definition, submitter))



# Just a simple of what you could do with this list now we have it
# Write a very simple web page containing a table with all the 
# data in.

#Need to use unicode because reddit does and some entries
#have international characters
html = codecs.open('log.html','w', 'utf-8')
#Write the header 
html.write('<HEAD>\n')
html.write('<TITLE>Logophilia Dump</TITLE>\n')
html.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
html.write('</HEAD>\n')
html.write('<BODY>\n')
html.write('<H3>Logophilia Dump</H3>\n')
#Start the table - define columns
html.write('<TABLE>\n')
html.write('<THEAD><TR><TH>Word</TH><TH>Meaning</TH><TH>Submitter</TH></THEAD>\n')
html.write('<TBODY>')

#Loop through our defintions and put them all in the table
for (word, definition, submitter) in valid_submissions:
	html.write(u'<TR><TD>{0}</TD><TD>{1}</TD><TD>{2}</TD></TR>'.format(word, definition, submitter))

#finish up
html.write('</TBODY>')
html.write('</TABLE>')
html.close()
