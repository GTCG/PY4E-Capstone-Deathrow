import sqlite3
import re
from bs4 import BeautifulSoup
import requests
import string
import urllib
import urllib3
import ssl
from datetime import datetime

ExecutionID= None
linkLS = None
conn = sqlite3.connect('Deathrow.sqlite')
requests.urllib3.disable_warnings()
conn.text_factory = str
cur = conn.cursor() 
cur.execute("DROP TABLE IF EXISTS Inmates")
cur.execute("CREATE TABLE Inmates (id integer primary key, Execution text, Lastname text, Firstname text, TDCJNumber text, Age integer, Date text, Race text, County text, Laststatement text, LastStatementURL text, InmateInformation text)")
conn.commit()
url='https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
data = requests.get(url,verify = False).text
soup = BeautifulSoup(data,"html.parser")
table = soup.find('table', attrs={'class': "tdcj_table indent"})
headers = table.find_all("th")
rows = table.find_all('tr')
for row in table.find_all("tr") [1:]:	
	cells = row.find_all('td')
	ExecutionID= str(cells[0].get_text())
	InmateInformation = 'https://www.tdcj.texas.gov/death_row/' + cells[1].a['href']
	linkLS = 'https://www.tdcj.texas.gov/death_row/' + cells[2].a['href']
	Lastname = str(cells[3].get_text())
	Firstname = str(cells[4].get_text())
	TDJC = str(cells[5].get_text())
	Age = int(cells[6].get_text())
	Date = (cells[7].get_text())
	Date = datetime.strptime(Date, '%m/%d/%Y').date()
	Race = str(cells[8].get_text())
	County = str(cells[9].get_text())
	print ("--- retrieving execution data for execution ID",ExecutionID,Lastname,",",Firstname," ---")
	if ExecutionID == "545":
		linkLS = "https://www.tdcj.texas.gov/death_row/dr_info/cardenasrubenlast.html"
	elif ExecutionID == "544":
		linkLS = "https://www.tdcj.texas.gov/death_row/dr_info/pruettrobertlast.html"
	elif ExecutionID == "552":
		linkLS ="https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html"
	r = requests.get(linkLS,verify = False)
	print ("--- retrieving statement for execution ID",ExecutionID,Lastname,",",Firstname, " ---")
	document = urllib.request.urlopen(linkLS)
	html = document.read()
	soup = BeautifulSoup(html,"html.parser")
	pattern = re.compile("Last Statement:")
	try:
		statement = soup.find(string=pattern).findNext('p').contents[0]
		statement = str(statement)
		statement = statement.lstrip(' ')
		statement = statement.rstrip(' ')
		statement = statement.replace("<span class=", "")
		statement = statement.replace("</span>", "")
		statement = statement.replace('"', "")
		statement = statement.replace("text_italic>", "")
	except Exception:
			print("An error has occured while retrieving the statement. Proceeding...")
			statement = ""
			continue

	cur.execute("INSERT OR IGNORE INTO Inmates (Execution, Lastname, Firstname, TDCJNumber, Age, Date, Race, County, Laststatement, LastStatementURL, InmateInformation) VALUES(?,?,?,?,?,?,?,?,?,?,?);", (str(ExecutionID), str(Firstname), str(Lastname), str(TDJC), int(Age), str(Date), str(Race), str(County), str(statement), str(linkLS), str(InmateInformation)))
conn.commit()
conn.close()
print ("Retrieval complete. Open deathrow.sqlite to see the data. Execute gword.py to create the wordcloud.")	