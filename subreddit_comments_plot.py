import praw
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

# incremenets dic[key] by value. if key is not in dic
# assume dic[key]=0
def increment_dict(dic, key, value):
	if key in dic:
		dic[key] += value
	else:
		dic[key] = value

# given dict where the values are comparable (so integers for us), returns
# the dict with the top n keys (or fewer if the dict is too small)
# where a key is higher ranked if it has a higher value
def top_n_dict(dic, n):
	top_keys = list(reversed(sorted(dic, key=dic.get)))
	top_keys = top_keys[0:n]
	new_dic = {};
	for i in range(len(top_keys)):
		new_dic[top_keys[i]]=dic[top_keys[i]]
	return new_dic


# plots subreddit vs. comment count, and subreddit vs. total score of comments in subreddit
# by user for the top n subreddits of the above metrics, where the comments are pulled
# from the last past_comment_number comments of the user
# note that if past_comment_number = None, then it pulls all possible comments
# (which reddit limits to 1000)
def plot_user_subreddits(user, n, past_comment_number):
	r = praw.Reddit("plotting Gina comments")
	u = r.get_redditor(user)

	subreddit_com_count = {} #dict mapping subreddit to number of comments
	subreddit_upvote_count = {} #dict mapping subreddit to total upvotes of comments in subreddit

	#loop through comments, increment above 2 dicts
	for comment in u.get_comments(limit=past_comment_number):
		sub = comment.subreddit.display_name
		increment_dict(subreddit_upvote_count, sub, comment.score)
		increment_dict(subreddit_com_count, sub, 1)

	subreddit_com_count = top_n_dict(subreddit_com_count, n)
	subreddit_upvote_count = top_n_dict(subreddit_upvote_count, n)

	### plotting stuff

	# could have abstracted this, but i think this makes it easier to understand
	# (well, for me anyway)

	labels_com = []
	com_count=[]
	num_com = 0

	labels_upvote=[]
	upvote_count=[]
	num_upvote=0

	for subreddit in subreddit_com_count:
		num_com += 1
		labels_com.append(subreddit)
		com_count.append(subreddit_com_count[subreddit])

	for subreddit in subreddit_upvote_count:
		num_upvote += 1
		labels_upvote.append(subreddit)
		upvote_count.append(subreddit_upvote_count[subreddit])

	ind_com = np.arange(num_com) #where x axis ticks should be
	ind_upvote = np.arange(num_upvote)
	width = 0.25

	#first plot!

	plt.subplot(1,2,1)
	plt.bar(ind_com, com_count, width, color='r')
	plt.ylabel("Comment Count")
	plt.title("Comment Counts By Subreddit")
	plt.xticks(ind_com, labels_com)

	locs, labels = plt.xticks()
	plt.setp(labels, rotation=90)

	plt.tight_layout()

	#second plot! 

	plt.subplot(1,2,2)
	plt.bar(ind_upvote, upvote_count, width, color='y')
	plt.ylabel("Vote Count")
	plt.title("Vote Counts By Subreddit")
	plt.xticks(ind_upvote, labels_upvote)

	locs, labels = plt.xticks()
	plt.setp(labels, rotation=90)

	plt.tight_layout()

	plt.show()

if __name__ == "__main__":
	user = input("username: ") #raw_input but for python 3.2+
	plot_user_subreddits(user, 15, None)