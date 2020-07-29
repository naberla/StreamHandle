import tweepy
import json
from datetime import datetime, timedelta
import os, sys
from twilio.rest import Client
import time as t
import random
import stream_listener
import logging
import httplib, urllib
from credentials import *

cr = credentials()
cr.load_credentials()

def send_push_notifications(text):
	try:
		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		urllib.urlencode({
		"token": cr.PUSHOVER_APP_TOKEN,
		"user": cr.PUSHOVER_USER_TOKEN,
		"message": text,
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()
	except Exception as e:
		logging.info("Unsuccessful notification for: " + text)
		logging.info(str(e))


client = Client(cr.twilio_account_sid , cr.twilio_account_token)

auth = tweepy.OAuthHandler(cr.CONSUMER_KEY, cr.CONSUMER_SECRET)	
auth.set_access_token(cr.ACCESS_TOKEN, cr.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=False,
    wait_on_rate_limit_notify=False)

try:
	logging.basicConfig(filename=sys.argv[-1],level=logging.INFO)
	logging.info("Starting logging...")
except Exception as e:
	print(e)
	sys.exit(0)

try:
    api.verify_credentials()
    logging.info("Authentication OK")
    timestamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") 
    logging.info(timestamp)
except:
    logging.info("Error during authentication")

sent_tweets = []
latest_tweet_id = 1288200555383455745
error_flag = False
max_retries = 15
i = 0
while(1): 
	t.sleep(1)
	try:
		if(int(datetime.now().strftime("%S"))%30 == 0):	
			data = api.rate_limit_status()
			logging.info((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
			logging.info("Limit: {}".format(data['resources']['statuses']['/statuses/user_timeline']['limit']))
			logging.info("Remaining: {}".format(data['resources']['statuses']['/statuses/user_timeline']['remaining']))  
	    	for tweet in tweepy.Cursor(api.user_timeline, screen_name= cr.twtr_handle, exclude_replies=False, since_id = latest_tweet_id).items():                  
			tweet_text = tweet.text  
			time = tweet.created_at  
			tweeter = tweet.user.screen_name  
			tweet_dict = {"tweet_text" : tweet_text.strip(), "timestamp" : str(time), "user" :tweeter}  
			tweet_json = json.dumps(tweet_dict)  
			timestamp = (datetime.now() - timedelta(seconds = 2*3600+60*10)).strftime("%Y-%m-%d %H:%M:%S") 
			if error_flag == True:
				error_flag = False
				i = 0
				logging.info("We are back online!")
			if (tweet_text.strip() not in sent_tweets) and (error_flag == False) and (str(time) > timestamp):
				latest_tweet_id = tweet.id
				client.messages.create(body=tweet_text.strip(), from_=cr.from_whatsapp_number, to=cr.to_whatsapp_number)
				client.messages.create(body=tweet_text.strip(), from_=cr.from_whatsapp_number, to=cr.to_whatsapp_number_selim)
				send_push_notifications(tweet_text.strip())
				logging.info(tweet_text.strip())
				sent_tweets.append(tweet_text.strip())

	except Exception as e:  
		error_flag = True
		timestamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") 
		logging.info("\n\n\n ERROR AT: " + timestamp + "\n\n\n\n" + str(e) + "\n\n\n\n")
		i = i+1
		if (i>max_retries):
			client.messages.create(body="\n\n\n ERROR AT: " + timestamp + "\n\n\n\n" + str(e) + "\n\n\n\n More than {} errors, something is wrong. Exiting...".format(max_retries), from_=cr.from_whatsapp_number, to=cr.to_whatsapp_number)
			t.sleep(1)
			client.messages.create(body="\n\n\n ERROR AT: " + timestamp + "\n\n\n\n" + str(e) + "\n\n\n\n More than {} errors, something is wrong. Exiting...".format(max_retries), from_=cr.from_whatsapp_number, to=cr.to_whatsapp_number_selim)
			send_push_notifications("\n\n\n ERROR AT: " + timestamp + "\n\n\n\n" + str(e) + "\n\n\n\n More than {} errors, something is wrong. Exiting...".format(max_retries))
			sys.exit(0)
		t.sleep(30)


