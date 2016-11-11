import sqlite3 #Modules required to do the job. Most important ones are urllib2, BeatifulSoup and Requests. I have imported "re" for some regex and 
import csv # "csv" to handle csv files.
import re
import urllib2
from urllib2 import Request, urlopen, URLError
from BeautifulSoup import BeautifulSoup
import requests
import string
URLS = ["http://www.tdcj.state.tx.us/death_row/dr_info/hernandezramontorreslast.html", #URLS not in standard form [lastname][firstname]last.html.
		"http://www.tdcj.state.tx.us/death_row/dr_info/garciafrankmlast.html", #I needed to add these manually.
		"http://www.tdcj.state.tx.us/death_row/dr_info/martinezdavidlast999173.html", 
		"http://www.tdcj.state.tx.us/death_row/dr_info/moselydaroycelast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/martinezdavidlast999288.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/hernandezadophlast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/carterrobertanthonylast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/livingstoncharleslast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/gentrykennethlast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/gentrykennethlast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/wilkersonrichardlast.html",
		"http://www.tdcj.state.tx.us/death_row/dr_info/hererraleonellast.html",]

conn = sqlite3.connect('prison.sqlite') #creation of the database
conn.text_factory = str
cur = conn.cursor() #interface between python and sqlite

# We create the table "prison" and put some columns in it.
cur.execute("DROP TABLE IF EXISTS prison")
cur.execute("CREATE TABLE Prison ( Execution text, link1 text, link2 text, LastName text, Firstname text, TDCJNumber text, Age integer, date text, race text, county text)")
conn.commit()


csvfile = open("prisonfile.csv","rb") #Open the csv file that has been made by an external website and fill up the columns with data.
creader = csv.reader(csvfile, delimiter = ",")
creader.next() #We do not need the first line of the csv file because those are the headers.
for t in creader:
	cur.execute('INSERT INTO  Prison VALUES (?,?,?,?,?,?,?,?,?,?)', t, ) #Import all the data from the csv file into the table "prison". One ? per field.

for column in cur.execute("SELECT LastName, Firstname FROM prison"): #We need the Lastname and firstname from our database for our links to the last
	lastname = column[0] #statements. For this we created 2 var's and start some garbage cleaning on them. This was trial and error. One ready, we
	firstname = column[1] #implement lowercase. This is needed, because otherwise we could invalidate links (e.g. jonaS Rowan) The link for the last statement
	name = lastname+firstname # has the following parts: Baseurl, Lastname, Firstname, last.html. All these links get added to a list, being called "URLS."
	CleanName = name.translate(None, ",.!-@'#$" "") #We will use every link in this list to check if it exists, and download the last statements.
	CleanName = CleanName.replace(" ", "")
	CleanName = CleanName.replace("III","")
	CleanName = re.sub("Sr","",CleanName)
	CleanName = re.sub("Jr","",CleanName)
	CleanName = CleanName.lower()
	Baseurl = "http://www.tdcj.state.tx.us/death_row/dr_info/"
	Link = Baseurl+CleanName+"last.html"
	URLS.append(Link)

cur.execute("DROP TABLE IF EXISTS Statements") #We create a new table, Statements, with a column, Statement.
cur.execute("CREATE TABLE Statements (Statement text)")
conn.commit()
	
	
for Link in URLS: #The fun part. We check every URL in the list. If the URL checks out ok we use Beatifulsoup to download the last statements.
	try: #This is being done by looking for certain tags on the website (this can be found by looking at the site source in your browser). I also inplemented
		r = requests.get(Link) #some debugging. This is useful for links not checking out for one reason or the other. I used this to find bugs in the naming
		r.raise_for_status() #or the URLS and added a few valid URL's manually. See above.
		print "URL OK", Link
		document = urllib2.urlopen(Link)
		html = document.read()
		soup = BeautifulSoup(html)
		pattern = re.compile("Last Statement:") #There were bugs in the HTML tagging. I had to fix a few links by adding some very small regex expression.
		Statement = soup.find(text=pattern).findNext('p').contents[0]
		print Statement
		cur.execute("INSERT OR IGNORE INTO Statements VALUES(?);", (str(Statement),)) #A little critter. Stuff being pulled by soup is an object. We must convert
		continue #it to string, because sqlite needs to be able to handle it.
	except requests.exceptions.HTTPError as err:
		print err
		print "Offender has made no statement.", Link # Some offenders did not make a last statement. If so, it leads to another URL instead of the basic one.
		 #If The URL does not check out, it means the offender did not make a last statement. But I had to make sure my program would not crash because of that.

csvfile.close() #Close the csvfile. I guess I could have put this earlier in the program
conn.commit() #commit and close the interfance between sqlite and python.
conn.close()