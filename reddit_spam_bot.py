import praw
import time
from pprint import pprint

# user = person to spam
# message_user = username of spammer
# message_pass = password of spammer
# so everytime user makes a new post, send them a message
# has some obvious bugs with users deleting comments
# but this is mostly to annoy a friend so i don't care too much
def spamming(user, message_user, message_pass):

	r = praw.Reddit("Spammer Bot 9001")
	r.login(message_user, message_pass)

	user = r.get_redditor(user)

	w=user.get_comments(limit=1)
	latest_id="";
	for i in w:
		latest_id = i.id

	msg = "So I see you made a post, eh?"

	while True:
		w=user.get_comments(limit=1)
		for j in w:
			w_id = j.id
			if w_id != latest_id:
				latest_id = w_id
				r.send_message(user, 'PRAW Thread', msg)
		time.sleep(60)

if __name__ == "__main__":

	spamming('fakeuser', 'fakespammer', 'idk')
