#!/usr/bin/python
import urllib2, datetime, sys, json
from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

#Get the nickname of the user from the Identification window
api = dbusapi.Accomplishments()
f = api.get_extra_information("ubuntu-community", "irc-nickname")
if bool(f[0]["irc-nickname"]) == False:
    sys.exit(4)
else:
    nickname = f[0]["irc-nickname"]

#Find the date of today and yesterday
now = datetime.datetime.now()	#this section gets today
today_year = str(now.year)
today_month = str(now.month)
today_day = str(now.day)

if len(today_day) < 2:
	today_day = '0' + today_day
yesterday = datetime.datetime.now() - datetime.timedelta(1)	#this section gets yesterday
yesterday_year = str(yesterday.year)
yesterday_month = str(yesterday.month)
yesterday_day = str(yesterday.day)

if len(yesterday_day) < 2:
	yesterday_day = '0' + yesterday_day

#Use the channel list of today to find the valid channels
try:
	pageurl = "http://irclogs.ubuntu.com/"+yesterday_year+"/"+yesterday_month+"/"+yesterday_day
	channelpage = urllib2.urlopen(pageurl)
	pagelist = channelpage.readlines()
	channelpage.close()
except (UnicodeDecodeError, urllib2.HTTPError):
	pass

channellist = []

for line in pagelist:
	indexno = line.find('#')+1
	indexdot = line.find('.txt',indexno)
	if indexno is not -1 and indexdot != -1:
		channellist.append(line[indexno:indexdot])

search_string = "] <" + nickname

total_count_result = 0

for irc_channel in channellist:
	today_web_page = "http://irclogs.ubuntu.com/"+today_year+"/"+today_month+"/"+today_day+"/%23"+irc_channel+".txt"	#build dynamic txt file link from vars
	today_count_result = 0
	try:
		today_response = urllib2.urlopen(today_web_page)	
		today_page_source = today_response.read()   			#this variable now contains the entire txt file
		today_count_result = today_page_source.count(search_string)  	#count number of times user spoke today
		today_response.close()
		
	except (UnicodeDecodeError, urllib2.HTTPError):
		pass
	yesterday_count_result = 0
	yesterday_web_page = "http://irclogs.ubuntu.com/"+yesterday_year+"/"+yesterday_month+"/"+yesterday_day+"/%23"+irc_channel+".txt"	#build dynamic txt file link from vars
	try:
		yesterday_response = urllib2.urlopen(yesterday_web_page)
		yesterday_page_source = yesterday_response.read()   					#this variable now contains the entire txt file
		yesterday_count_result = yesterday_page_source.count(search_string)  	#count number of times user spoke yesterday
		yesterday_response.close()
	except (UnicodeDecodeError, urllib2.HTTPError):
		pass #Maybe the file was not there the day before, maybe someone wrote a strange character. It doesn't matter. We can skip that line or file.
	total_count_result += today_count_result + yesterday_count_result  		#get grand total

	if total_count_result > 2:    				#we want to see if user has been chatting (said more than two lines)
		sys.exit(0)
else:
	sys.exit(1)	#We reached the last file without gathering enough lines. Accomplishment not yet fulfilled.
