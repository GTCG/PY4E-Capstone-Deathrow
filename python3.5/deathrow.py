import sqlite3  #warning: using charset 65001 by typing in cmd "chcp 65001" Only when showing last statements on screen.
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import string
inmatecount = 0
statementcount = 1

conn = sqlite3.connect('Deathrow.sqlite') 
conn.text_factory = str
cur = conn.cursor() 
cur.execute("DROP TABLE IF EXISTS Inmates")
cur.execute("CREATE TABLE Inmates (id integer primary key, execution text, lastname text, firstname text, TDCJNumber text, age integer, date text, race text, county text, laststatement text)")
conn.commit()
url='http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
lines = urllib.request.urlopen(url)
prisondata = lines.read()
lines.close()
soup = BeautifulSoup(prisondata,"html.parser")
rows = soup.find_all('tr')
url2 = url[:38]
for row in rows:
	try:
		td = row.find_all('td')
		print ("--- retrieving inmate data for inmate ",inmatecount," ---")
		inmatecount +=1
		execution = str(td[0].get_text())
		lastname = str(td[3].get_text())
		firstname = str(td[4].get_text())
		tdcj = str(td[5].get_text())
		age = str(td[6].get_text())
		date = str(td[7].get_text())
		race = str(td[8].get_text())
		county = str(td[9].get_text())
		links = row.find_all("a")
		link = links[1].get("href")
		lastStatementLink = url2 + link
		r = requests.get(lastStatementLink) 
		r.raise_for_status() 
		print ("--- retrieving statement", statementcount," ---")
		statementcount +=1
		document = urllib.request.urlopen(lastStatementLink)
		html = document.read()
		soup = BeautifulSoup(html,"html.parser")
		pattern = re.compile("Last Statement:") 
		statement = soup.find(text=pattern).findNext('p').contents[0]
		statement = str(statement)
		statement = statement.lstrip(' ')
		statement = statement.rstrip(' ')
		statement = statement.replace("<span class=", "")
		statement = statement.replace("</span>", "")
		statement = statement.replace('"', "")
		statement = statement.replace("text_italic>", "")
		cur.execute("INSERT OR IGNORE INTO Inmates (execution, lastname, firstname, TDCJNumber, age, date, race, county, laststatement) VALUES(?,?,?,?,?,?,?,?,?);", (str(execution), str(firstname), str(lastname), str(tdcj), str(age), str(date), str(race), str(county), str(statement), ))
		continue
	except Exception:
		print ("Ignoring row headers. Proceeding.")
		continue

conn.commit()
conn.close()
print ("Retrieval complete. Open deathrow.sqlite to see the data. Execute gword.py to create the wordcloud.")	