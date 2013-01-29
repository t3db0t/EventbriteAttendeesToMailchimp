#!/usr/bin/python

import eventbrite
from postmonkey import PostMonkey

print "Authorizing..."

# authorization
eb_auth_tokens = {'app_key':  'YOUR_APP_KEY',
                  'user_key': 'YOUR_USER_KEY'}
eb_client = eventbrite.EventbriteClient(eb_auth_tokens)

pm = PostMonkey('YOUR_MAILCHIMP_API_KEY')


userEvents = eb_client.user_list_events()
#print pm.ping() # returns u"Everything's Chimpy!"
idlist = [evnt['event']['id'] for evnt in userEvents['events']]
print "Found %s event(s)" % len(idlist)
print idlist

all_emails = []

print "Getting attendee emails..."
for thisid in idlist:
	try:
		peeps = eb_client.event_list_attendees({'id':thisid})
	except EnvironmentError as e:
		print e
	these_emails = [peep['attendee']['email'] for peep in peeps['attendees']]
	print "%s: [%s]" % (thisid, these_emails)
	all_emails.extend(these_emails)

print "Found %s email(s)" % len(all_emails)

print "Updating Mailchimp list..."
mc_list_id = pm.lists()['data'][0]['id']

# the Mailchimp API wants an array of structs
email_structs = [{'EMAIL':eml} for eml in all_emails]

results = pm.listBatchSubscribe(id=mc_list_id, batch=email_structs, update_existing=True, double_optin=False)

print results
print "*** DONE ***"