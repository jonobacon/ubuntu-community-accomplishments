#!/usr/bin/python
import urllib2, datetime, sys, os, time, chardet
from accomplishments.daemon import dbusapi

#Get the nickname of the user from the Identification window
api = dbusapi.Accomplishments()
f = api.get_extra_information("ubuntu-community", "irc-nickname")
if bool(f[0]["irc-nickname"]) == False:
    sys.exit(4)
else:
    nickname = f[0]["irc-nickname"]

#We only want to check once every hour, when logs are updated. Checking 
#last timestamp, if any exists...
fd = open(os.path.join(os.path.expanduser("~") + "/.cache/accomplishments/", "chatonirc"), "r")
if fd:
    content = fd.read()
    fd.close()
    #if no time stamp logged
    if len(content) > 0:
        timestamp = float(content) +3600
        #Temporary hack to ensure being able to use accomplishments-battery
        if not nickname == "ubottu" and not nickname == "failfailfail"\
            and timestamp > time.time():
            print "Skipping Ubuntu IRC Chatter accomplishment this time."
            sys.exit(1)

#Writing new timestamp
fd = open(os.path.join(os.path.expanduser("~") + "/.cache/accomplishments/",\
    "chatonirc"), "w")
fd.write(str(time.time()))
fd.close()

#Find the date of today
now = datetime.datetime.now()
today_year = str(now.year)
today_month = str(now.month)
today_day = str(now.day)

if len(today_day) < 2:
    today_day = '0' + today_day

pagelist = []
#Use the channel list of today to find the valid channels
try:
    pageurl = "http://irclogs.ubuntu.com/"+today_year+"/"+today_month+"/"+today_day
    channelpage = urllib2.urlopen(pageurl)
    pagelist = channelpage.readlines()
    channelpage.close()
except Exception, e:
    #The log file for today might not yet exist. We will check again later.
    print "Error on loading channel list: " + str(e) 

channellist = []

for line in pagelist:
    indexno = line.find('#')+1
    indexdot = line.find('.txt',indexno)
    if indexno is not -1 and indexdot != -1:
        channellist.append(line[indexno:indexdot])

search_string = "] <" + nickname

total_count_result = 0

for irc_channel in channellist:
    #build dynamic txt file link from vars
    today_web_page = "http://irclogs.ubuntu.com/"+today_year+"/"+today_month+"/"+today_day+"/%23"+irc_channel+".txt"
    today_count_result = 0
    try:
        today_response = urllib2.urlopen(today_web_page)
        #this variable now contains the entire txt file
        today_page_source = today_response.read()
        encoding = chardet.detect(today_page_source)
        if not isinstance(type(encoding['encoding']), str):
                    encoding['encoding'] = 'utf-8'
        tekst = today_page_source.decode(encoding['encoding'], "ignore")
        #count number of times user spoke today
        today_count_result = tekst.count(search_string)
        today_response.close()

    except Exception, e:
        #maybe someone wrote a strange character. It doesn't matter.
        #We can skip that line or file.
        print "Error on channel " + irc_channel + ": " + str(e)

    #get grand total
    total_count_result += today_count_result

    #we want to see if user has been chatting (said more than two lines)
    if total_count_result > 2:
        sys.exit(0)
else:
    #We reached the last file without gathering enough lines.
    #Accomplishment not yet fulfilled.
    sys.exit(1)
