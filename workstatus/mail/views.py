# Create your views here.
# directory: workstatus/mail
from string import*
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import workstatus.mail.models
from django.core.mail import send_mail
from datetime import datetime

import feedparser
from django.contrib.auth.models import User
from workstatus.mail.loaddb import addMessage, addUser
from workstatus.mail.models import Message, User
from workstatus.sendingMassEmail.views import *
from datetime import date
import time, os
import smtplib

#Settings
USERNAME="umanage.mpd@gmail.com"
PASSWORD=" yashar2bananapeel"
PROTO="https://"
SERVER="mail.google.com"
PATH="/gmail/feed/atom"

getInitialFeed = feedparser.parse(PROTO + USERNAME + ":" + PASSWORD + "@" + SERVER + PATH)
lastModified = getInitialFeed.entries[0].modified
ignoreList = []

###########################################################################################################    
def read(request):
    #get initial time from feed
    getInitialFeed = feedparser.parse(PROTO + USERNAME + ":" + PASSWORD + "@" + SERVER + PATH)
    lastModified = getInitialFeed.entries[0].modified
    while True:
        #keep checking for feed
        scrapedFeed = feedparser.parse(PROTO+USERNAME+":"+PASSWORD+"@"+SERVER+PATH)
        scrapedModified = scrapedFeed.entries[0].modified #get time when feed is being checked
        if lastModified < scrapedModified: #if there is a new message (timestamp is greater than the last time the feed was checked)
            lastModified = scrapedModified #update the last time a new message arrived
            name1 = scrapedFeed.entries[0].author_detail.name #get details
            email1 = scrapedFeed.entries[0].author_detail.email
            content = str(scrapedFeed.entries[0].title) 
            
            try:
                user = User.objects.get(email = email1) #try to get user who sent it from database
            except:
                x = find(name1,' ')+1 #if user does not exist, create user in database
                first = name1[:x]
                addUser(name1, email1, first)    
                user = User.objects.get(email = email1)
            
            time1 = str(scrapedModified) #parse into string so it can be sliced
            time2 = time1[:10]+' '+time1[11:19] #edit string into a time that can be parsed
            time3 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S') #parse string into a datetime object
            underscorename = convert(user.username,' ','_')
            addMessage(user, email1, content, time3, underscorename) #add new Message object to database
        
        current = str(time.strftime('%X')) #get current time
        today = date.today() #get day of week today
        dayofweek = today.isoweekday() #get day of week

        check(current, dayofweek)
            
    return HttpResponse()
############################################################################################################

def parser(request):
    """Filters through a message to find projects and their work progress status"""
    """Example: What needs to get done: #Project1, #Project2, #Project"""

    showEntries = []
    m = Message.objects.all() #get all messages
    
    if len(m) < 10: length = len(m) #if there are more than 10 messages, only show the latest 10 in the feed
    else: length = 10
    
    for i in range(0,length):
        showEntries.append(m[len(m)-1-i]) #add latest object, which is at end of m

    content0 = showEntries[0].content #get latest content and information (to be displayed larger on template)
    user0 = showEntries[0].user.username
    under0 = showEntries[0].underscorename
    time0 = str(showEntries[0].time1)
    
    showEntries.remove(showEntries[0])

    template = get_template('testing.html')
    variables = Context({'showEntries':showEntries, 'under0':under0, 'content0':content0, 'time0':time0, 'user0':user0})
    output = template.render(variables)

    return HttpResponse(output) #output onto web page

#############################################################################################################

def user_page(request,name):
    messages = []
    username = convert(name, '_', ' ') #convert name in url to username
    user1 = User.objects.get(username = username) #find user by username
    user_msgs = list(Message.objects.filter(user = user1)) #list(QuerySet of messages by user)
    user_msgs.reverse() #reverse list so that the most updated posts are first
    first_name = User.objects.get(username = username).first_name #get first name of User
    
    initial = user_msgs[0] #get latest message and information
    time0 = initial.time1 
    content0 = initial.content
    
    if len(user_msgs) > 1: x = 1 #if User has more than one message, create additional list
    else: x = 0 #otherwise, do not include list of older messages
        
    for i in range (x,len(user_msgs)): #add latest messages to list
        messages.append(user_msgs[i])
    
    template = get_template('user_page.html')
    variables = Context({ 'messages':messages, 'first_name':first_name, 'time0':time0, 'content0':content0})   
    output = template.render(variables)
    
    return HttpResponse(output) #show output on page

def convert (name, char1, char2):
    """takes a string and converts char1 to char2"""
    target = find(name,char1) #locate index of character needed to be converted
    final = name[:target]+char2+name[(target+1):]
    while(find(final, char1)!=-1): #if someone's name has more than one char1, look for next instance
        target = find(final,char1)
        final = name[:target]+char2+name[(target+1):]
    return final
    