#!/usr/bin/python3
import os, sys, curses
from datetime import datetime

def getUsername(inputArgs):
    if len(inputArgs) <= 1:
        print ("Please include a username...")
        exit()
    username = " ";
    for word in inputArgs:
        if word != "./view.py":
            username = username + " " + word
    username = username.lstrip()
    return username

def createStreamList():
    streamList = []
    streamListFile = open("messages/streamList", "r")
    for line in streamListFile:
        streamList.append(line.strip())
    streamListFile.close()
    return streamList

def createPermissionList(username, streamList):
    userPermissionStreamList = []
    flag = 0
    for word in streamList:
        userFileName = "messages/" + word + "UserStream"
        userListFile = open(userFileName, "r")
        for line in userListFile:
            if username == line.strip(" \n0123456789"):
                flag = 1
                userPermissionStreamList.append(word)
    if flag == 0:
        print ("User has no permissions...")
        exit()
    return userPermissionStreamList

def getStreamChoice(userPermissionStreamList):
    userChoice = input()
    properInputFlag = "none"
    #if user selects all
    if userChoice.strip() == "all":
        properInputFlag = "all"
    # else
    else:
        for word in userPermissionStreamList:
            if(userChoice.strip() == word.strip()):
                properInputFlag = word.strip()

    if properInputFlag == "none":
        print ("Invalid stream choice, choose from the list...")
        exit()

    return properInputFlag

def getReadMessages(username, outFileUserName):
    fPtr = open(outFileUserName, "r")
    for line in fPtr:
        if line.strip(" \n0123456789") == username:
            for s in line.split():
                if s.isdigit():
                    fPtr.close()
                    return s
    return 0

def getToPrint(readList, unreadList, streamname, username):
    outFileStreamName = "messages/" + streamname + "Stream"
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    i = getReadMessages(username, outFileUserName)
    offset = 0;
    if int(i) != 0:
        fPtr = open(outFileDataName, "r")
        count = 1
        for line in fPtr:
            if int(i) == int(count):
                offset = int(line)
                break;
            count = count + 1
        fPtr.close()
    fPtr = open(outFileStreamName, "r")
    count = 0
    for line in fPtr:
        if count < offset:
            if "Sender:" in line:
                readList.append("Stream: " + streamname + "\n")
            readList.append(line)
        else:
            if "Sender:" in line:
                unreadList.append("Stream: " + streamname + "\n")
            unreadList.append(line)
        for char in line:
            count = count + 1

    fPtr.close()

    return readList, unreadList

def sortByDate(myList):
    dateList = []
    tempList = []
    for item in myList:
        if "Stream:" in item:
            if tempList:
                copyList = tempList[:]
                dateList.append(copyList)
                tempList[:] = []
        tempList.append(item)
    if tempList:
        copyList = tempList[:]
        dateList.append(copyList)
    dateList.sort(key=lambda date: datetime.strptime(date[2], "Date: %b. %d, %Y, %I : %M %p\n"))
    finalList = []
    for l in dateList:
        for item in l:
            finalList.append(item)
    return finalList

def sortByAuthor(readList, unreadList):
    combinedList = readList + unreadList
    authorList = []
    tempList = []
    for item in combinedList:
        if "Stream:" in item:
            if tempList:
                copyList = tempList[:]
                authorList.append(copyList)
                tempList[:] = []
        tempList.append(item)
    if tempList:
        copyList = tempList[:]
        authorList.append(copyList)

    authorList.sort(key=lambda x: x[1])
    finalList = []
    for l in authorList:
        for item in l:
            finalList.append(item)
    return finalList

def printToWindow(window, readList, unreadList, currentLineNumber):
    window.clear()
    allList = readList + unreadList
    count = 0
    currentLines = 0
    for line in allList:
        if(count < int(currentLineNumber)):
            count = count + 1
            continue
        if currentLines < 23 :
            window.addstr(line)
            currentLines = currentLines + 1
            count = count + 1

def getLastLine(readList, unreadList):
    allList = unreadList + readList
    count = 0
    for line in allList:
        count = count + 1
    return count

def markAllRead(username, streamname):
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    fp = open(outFileDataName, "r")
    count = 0
    for line in fp:
        count = count + 1
    fp.close()
    fp = open(outFileUserName, "r")
    fpcopy = open("copy", "w")
    for line in fp:
        if line.strip(" \n0123456789") == username:
            fpcopy.write(username + " " + str(count) + "\n")
        else:
            fpcopy.write(line)
    fpcopy.close
    os.rename("copy", outFileUserName)

def updateReadMessages(streamname, username, currentLineNumber, unreadList, readList):
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    outFileStreamName = "messages/" + streamname + "Stream"
    j = 0
    read = 0
    postStream = "DEFAULT"
    allList = readList + unreadList
    for item in allList:
        if "Stream:" in item:
            postStream = item[8:].strip()
        if "Date: " in item:
            if postStream == streamname:
                read = read + 1
        j = j + 1
        x = currentLineNumber + 23
        if j >= x:
            break
    infileRead = int(getReadMessages(username, outFileUserName))
    if read < int(infileRead):
        read = int(infileRead)
    #writing to output file
    fpUser = open(outFileUserName, "r+")
    fpcopy = open("copy", "w")
    for line in fpUser:
        if username == line.strip(" \n0123456789"):
            fpcopy.write(username + " " + str(read) + "\n")
        else:
            fpcopy.write(line)
    fpUser.close()
    fpcopy.close()
    os.rename("copy", outFileUserName)

def getLastItem(myList):
    count = 0
    for item in myList:
        count = count + 1
    return count

def main():
    #checking for valid username, and placing it into variable
    username = getUsername(sys.argv)
    # creating list of all streams
    streamList = createStreamList()
    # checking each user file for a list of streams they are associated with
    userPermissionStreamList = createPermissionList(username, streamList)

    # printing all options user has permission for
    for word in userPermissionStreamList:
        print (word.strip(), end=' ')
    print ("all")

    # check which stream they would like to view
    inputFlag = getStreamChoice(userPermissionStreamList)

    # init curses
    window = curses.initscr()
    #curses.start_color()
    curses.noecho()
    window = curses.newwin(24, 80, 0, 0)

    # looping and printing
    unreadList = []
    mode = "chrono"
    readList = []
    currentLineNumber = 0
    updateListFlag = 1
    needToPrint = 1
    while True:
        if inputFlag == "all" and updateListFlag == 1:
            unreadList = []
            readList = []
            for stream in userPermissionStreamList:
                readList, unReadList = getToPrint(readList, unreadList, stream, username)
            currentLineNumber = getLastItem(readList)
            if mode == "author":
                readList = sortByAuthor(readList, unreadList)
                currentLineNumber = 0
            else:
                readList = sortByDate(readList)
                unreadList = sortByDate(unreadList)
            if not unreadList:
                currentLineNumber = 0
            updateListFlag = 0
            needToPrint = 1
        elif updateListFlag == 1:
            unreadList = []
            readList = []
            readList, unReadList = getToPrint(readList, unreadList, inputFlag, username)
            currentLineNumber = getLastItem(readList)
            if mode == "author":
                readList = sortByAuthor(readList, unreadList)
                currentLineNumber = 0
            else:
                readList = sortByDate(readList)
                unreadList = sortByDate(unreadList)
            if not unreadList:
                currentLineNumber = 0
            updateListFlag = 0
            needToPrint = 1

        #add update read messages
        if inputFlag == "all" and mode == "chrono":
            for stream in userPermissionStreamList:
                updateReadMessages(stream, username, currentLineNumber, unreadList, readList)
        elif mode == "chrono":
            updateReadMessages(inputFlag, username, currentLineNumber, unreadList, readList)

        # determines if it needs to print if a certain action is taken
        if needToPrint == 1:
            printToWindow(window, readList, unreadList, currentLineNumber)
            window.addstr(23, 0, "Page Up   Page Down   O-order toggle   M-mark all   S-stream   C-check for new")
            needToPrint = 0

        c = window.getch()
        if c == 65:
            currentLineNumber = currentLineNumber - 23;
            if currentLineNumber < 0:
                currentLineNumber = 0
            needToPrint = 1
        elif c == 66:
            currentLineNumber = currentLineNumber + 23;
            maxline = getLastLine(readList, unreadList)
            if currentLineNumber >= int(maxline):
                currentLineNumber = currentLineNumber - 23
            needToPrint = 1
        elif c == ord('o') or c == ord('O'):
            if mode == "author":
                mode = "chrono"
            else:
                mode = "author"
            updateListFlag = 1
        elif c == ord('m') or c == ord('M'):
            if inputFlag == "all":
                for stream in userPermissionStreamList:
                    markAllRead(username, stream)
            else:
                markAllRead(username, inputFlag)
            updateListFlag = 1
        elif c == ord('s') or c == ord('S'):
            updateListFlag = 1
            curses.echo()
            curses.endwin()
            for word in userPermissionStreamList:
                print (word.strip(), end=' ')
            print ("all")
            inputFlag = getStreamChoice(userPermissionStreamList)
            window = curses.initscr()
            curses.noecho()
            window = curses.newwin(24, 80, 0, 0)
        elif c == ord('c') or c == ord('C'):
            updateListFlag = 1
        elif c == ord('q') or c == ord('Q'):
            break  # Exit the while loop

        window.refresh()

    # terminating curses
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()
