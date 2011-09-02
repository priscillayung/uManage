##workstatus>mail

from string import *
    
def asdf():
    """asdf"""
    string = "I am working on #jelly and #this. I paused #project. I am done #lunch, #dinner, and #breakfast."
##############01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234
    ##########00000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999


    doingKeys = ['working on', 'in progress','resume']
    doneKeys = ['completed','done','finished']
    pauseKeys = ['pause','on hold']
    keys = [doingKeys, doneKeys, pauseKeys]

    doingPros = [] #store names of projects
    donePros = []
    pausePros = []
    projects = [doingPros,donePros,pausePros]

    doingTemp = [] #stores locations of keywords
    doneTemp = []
    pauseTemp = []
    temp = [doingTemp,doneTemp,pauseTemp]

    locate = [] #stores locations of key words

    #search for key words

    k = len(keys)

    for i in range(k):
        for j in range(len(keys[i])):
            x = find(string,keys[i][j])
            while x != -1:
                locate.append(x)
                temp[i].append(x)
                x = find(string,keys[i][j],x+1)

##    for i in range(len(temp)):
##        for x in range(len(temp[i])):
##            print temp[i][x]

    locate.sort()
    #print 'locate, sorted:',locate,'\n'

    #search for hash tags after each keyword location

    for i in range (k):
        for j in range(len(temp[i])):
            start = temp[i][j] #location of keyword
            n = locate.index(start) #index of location in the locate list
            #print n
            #print 'locate [ n ] = start'
            #print 'locate [',n,'] =',start
            if (n == len(locate)-1): end = len(string)
            else: end = locate[n+1]
            #print 'end',end
            x = find(string, '#', start)
            #print 'x ',x
            while x!= -1 and x < end: #while a hash tag can be found
                sub = ''
                x+=1
                #print string[x],ord(string[x])
                while (ord(string[x]) > 64 and ord(string[x]) < 91) or (ord(string[x]) > 96 and ord(string[x]) < 123) or (ord(string[x]) >47 and ord(string[x])<58):
                    #while next space, period, comma etc is not reached yet
                    sub += string[x]
                    #print 'sub:',sub
                    x += 1
                projects[i].append(sub) #add project name to list
                #print projects[i]
                start = x+1
                x = find(string, '#', start)

    print 'This is the message: \n',string
    print '\nThese are the projects in progress:'
    print doingPros
    print '\nThese are the projects that are finished:'
    print donePros
    print '\nThese are the projects that have been paused:'
    print pausePros

asdf()            
                

    

