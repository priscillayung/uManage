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
    getInitialFeed = feedparser.parse(PROTO + USERNAME + ":" + PASSWORD + "@" + SERVER + PATH)
    lastModified = getInitialFeed.entries[0].modified
    while True:
        scrapedFeed = feedparser.parse(PROTO+USERNAME+":"+PASSWORD+"@"+SERVER+PATH)
        scrapedModified = scrapedFeed.entries[0].modified
        if lastModified < scrapedModified: #if there is a new message
            lastModified = scrapedModified
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
            addMessage(user, email1, content, time3) #add new Message object to database
        
        current = str(time.strftime('%X'))
        today = date.today()
        dayofweek = today.isoweekday()

        check(current, dayofweek)
            
    return HttpResponse()
############################################################################################################

def parser(request):
    """Filters through a message to find projects and their work progress status"""
    """Example: What needs to get done: #Project1, #Project2, #Project"""

    showEntries = []
    m = Message.objects.all()
    
    if len(m) < 10: length = len(m)
    else: length = 10
    
    for i in range(0,length):
        showEntries.append(m[len(m)-1-i]) #add latest object, which is at end of m

    content0 = showEntries[0].content
    user0 = showEntries[0].user.username
    time0 = str(showEntries[0].time1)
    space = find(user0,' ')
    name0 = user0[:space]+'_'+user0[(space+1):]
    
    showEntries.remove(showEntries[0])

    template = get_template('testing.html')
    variables = Context({'showEntries':showEntries, 'name0':name0, 'content0':content0, 'time0':time0, 'user0':user0})
    output = template.render(variables)

    return HttpResponse(output)

#############################################################################################################

def user_page(request,name):
    messages = []
    underscore = find(name,'_') #convert '_' to ' ' and parse name from url into username
    username = name[:underscore]+' '+name[(underscore+1):] 
    user1 = User.objects.get(username = username) #find user by username
    user_msgs = list(Message.objects.filter(user = user1)) #list(QuerySet of messages by user)
    user_msgs.reverse()
    first_name = User.objects.get(username = username).first_name
    
    initial = user_msgs[0]
    time0 = initial.time1
    content0 = initial.content
    
    if len(user_msgs) > 1: x = 1
    else: x = 0
        
    for i in range (x,len(user_msgs)):
        messages.append(user_msgs[i])
    
    template = get_template('user_page.html')
    variables = Context({ 'messages':messages, 'first_name':first_name, 'time0':time0, 'content0':content0})   
    output = template.render(variables)
    
    return HttpResponse(output)


    