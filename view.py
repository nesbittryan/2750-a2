#!/usr/bin/python3
import os, sys, curses

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
            readList.append(line)
        else:
            unreadList.append(line)
        for char in line:
            count = count + 1
    fPtr.close()
    return readList, unreadList

def printToWindow(window, readList, unreadList, currentLineNumber):
    window.clear()
    allList = unreadList + readList
    count = 0
    currentLines = 0
    for line in allList:
        if(count < int(currentLineNumber)):
            count = count + 1
            continue
        if(currentLines < 23):
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
            fpcopy.write(username + " " + str(count))
        else:
            fpcopy.write(line)
    fpcopy.close
    os.rename("copy", outFileUserName)
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
    curses.noecho()
    window = curses.newwin(24, 80, 0, 0)

    # looping and printing
    unreadList = []
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
                currentLineNumber = 0
                updateListFlag = 0
                needToPrint = 1
        elif updateListFlag == 1:
            unreadList = []
            readList = []
            readList, unReadList = getToPrint(readList, unreadList, inputFlag, username)
            currentLineNumber = 0
            updateListFlag = 0
            needToPrint = 1

        # determines if it needs to print if a certain action is taken
        if needToPrint == 1:
            printToWindow(window, readList, unreadList, currentLineNumber)
            window.addstr(23, 0, "Page Up   Page Down   O-order toggle   M-mark all   S-stream   C-check for new")
            needToPrint = 0

        c = window.getch()

        if c == 65:         # change to page up
            currentLineNumber = currentLineNumber - 23;
            if currentLineNumber < 0:
                currentLineNumber = 0
            needToPrint = 1
        elif c == 66:       # change to page down
            currentLineNumber = currentLineNumber + 23;
            maxline = getLastLine(readList, unreadList)
            if currentLineNumber > int(maxline):
                currentLineNumber = currentLineNumber - 23
            needToPrint = 1
        #elif c == ord('o') or c == ord('O'):
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
