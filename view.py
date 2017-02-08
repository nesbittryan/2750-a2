#!/usr/bin/python3
import sys
import curses

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

def printToWindow(window, username, streamname, j):
    outFileStreamName = "messages/" + streamname + "Stream"
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    i = getReadMessages( username, outFileUserName)

    offset = 0
    if int(i) != 0:
        fPtr = open(outFileDataName, "r")
        count = 0
        for line in fPtr:
            count = count + 1
            if int(i) == int(count):
                offset = line
                fPtr.close()
                break;
    if j <= 21:
        window.addstr(j, 0, "--------------------\n")
        j = j + 1
        window.addstr(j, 0, "Stream: " + streamname + "\n")
        j = j + 1
    fPtr = open(outFileStreamName, "r")
    offset = int(offset) - 1
    if offset == -1:
        offset = 0
    fPtr.seek(int(offset), 0)
    for line in fPtr:
        if j <= 22:
            window.addstr(j, 0, line)
            j = j + 1
    fPtr.close()
    window.refresh()
    return j


def getReadMessages(username, outFileUserName):
    fPtr = open(outFileUserName, "r")
    for line in fPtr:
        if line.strip(" \n0123456789") == username:
            for s in line.split():
                if s.isdigit():
                    return s
    return 0

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
    while True:
        curses.setsyx(0,0)
        i = 0
        if inputFlag == "all":
            for stream in userPermissionStreamList:
                 i = printToWindow(window, username, stream, i)
                 i = i + 1
        else:
            i = printToWindow(window, username, inputFlag, i)
        #print controls / commands
        window.addstr(23, 0, "Page Up   Page Down   O-order toggle   M-mark all   S-stream   C-check for new")
        window.move(23,79)
        c = window.getch()

        if c == 65:         # change to page up
            window.addstr(0, 0, "page up")
        elif c == 66:       # change to page down
            window.addstr(0, 0, "page down")
        #elif c == ord('o') or c == ord('O'):

        #elif c == ord('m') or c == ord('M'):

        elif c == ord('s') or c == ord('S'):
            curses.echo()
            curses.endwin()
            for word in userPermissionStreamList:
                print (word.strip(), end=' ')
            print ("all")
            inputFlag = getStreamChoice(userPermissionStreamList)
            window = curses.initscr()
            curses.noecho()
            window = curses.newwin(24, 80, 0, 0)

        #elif c == ord('c') or c == ord('C'):

        elif c == ord('q') or c == ord('Q'):
            break  # Exit the while loop

        window.refresh()

    # terminating curses
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    main()
