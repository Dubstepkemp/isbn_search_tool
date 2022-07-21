
#Author: Kevin Kemp
#purpose: this script makes it easier to look up book titles and isbns

##### ##### ##### ##### ##### ##### ##### #####
#this file has been updated with a logger
#I thought it might be useful to keep a log of all the queries I've made,
#and their results and keep them in a file. That way, even when I don't have internet access,
# I can still find the isbn's of books I have searched.
# Now, while this logger does not exclusively need to be a singleton
# in this instance, if the logger was used for multiple files simultaneously,
# having it as a singleton could save system resources.
# the query and the results is all we are interested logging at present
#edits to the original file have been surrounded a line of 40 #'s (pounds) to make it easier
#to find the new code. The line without spaces is before, and the line without spaces closes it.
########################################

#import statements
import urllib.parse
import requests


##### ##### ##### ##### ##### ##### ##### #####
#singleton logger
class _Singleton(object):

    def __init__(self):
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()
        #the log file name is logger.txt for this example, but could be anything
        self.log = open("logger.txt","a")

    #appends to the log
    def addToLog(self,log):
        #skips a line after each entry
        self.log.write("\n" + log)

    def closeLog(self):
        #marks end of current log, securely closes log 
        self.log.write("\nend of results\n") 
        self.log.close()
_singleton = _Singleton()

def Singleton(): return _singleton
########################################


##### ##### ##### ##### ##### ##### ##### #####
#now to add our logger to this file, it could also have been done with an import statement
logger = Singleton()
########################################


#user input
print("MENU:")
print("(1) find book name by isbn")
print("(2) find isbn by book name")
#user selection
selection = input()
#initializing variables
userInput = ""
main_api ='https://www.googleapis.com/books/v1/volumes?q'
url = ""
searchType = ""

# (1) isbn or (2) book
if(selection == "1"):
    print("please input the isbn number: ")
    userInput = input()
    searchType = "isbn:"
else:
    print("please input the name of the book: ")
    userInput = input()
    searchType = "book:"

##### ##### ##### ##### ##### ##### ##### #####
#log the user query
logger.addToLog("searched for " + userInput + "\n")
########################################

#set the url
url = main_api + urllib.parse.urlencode({"":searchType + userInput})
print(url)

#retrieve the data as json
json_data = requests.get(url).json()

#often a name will refer to more than one book, we want to list them all
books = len(json_data['items'])


#prints the requested information
for x in range(books):

    #these were found separately to make the print statement more readable
    title = json_data['items'][x]['volumeInfo']['title']
    n = len(json_data['items'][x]['volumeInfo']['industryIdentifiers'])
    if(n > 1):
        isbnTen = json_data['items'][x]['volumeInfo']['industryIdentifiers'][0]['identifier']
        isbnThirteen = json_data['items'][x]['volumeInfo']['industryIdentifiers'][1]['identifier']
    elif(n > 0):
    #print (json_data ['items'][x]['volumeInfo']['industryIdentifiers'])
        isbnTen = json_data['items'][x]['volumeInfo']['industryIdentifiers'][0]['identifier']
        isbnThirteen = ""
    else:
        isbnTen = ""
        isbnThirteen = ""
    #makes it easy to print and add to the logger
    printer = "{} | isbn10 {} isbn13 {}".format(title,isbnTen,isbnThirteen)

    # printing requested information (title and isbns are both given in case more than one result returned...
    # each title can be matched to the correct isbn
    print(title, " | isbn10 ", isbnTen, " isbn13 " , isbnThirteen)
    print(printer)


    ##### ##### ##### ##### ##### ##### ##### #####
    #now to add the results to the log
    logger.addToLog(printer)
    ########################################

##### ##### ##### ##### ##### ##### ##### #####
#now to close the log
logger.closeLog()
########################################


        
#googleapi.py
#Displaying googleapi.py.
