import sqlite3
import re
from bs4 import BeautifulSoup
import requests
import urllib3
from datetime import datetime

ExecutionID = None
linkLS = None
conn = sqlite3.connect('Deathrow.sqlite')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn.text_factory = str
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Inmates")
cur.execute("""CREATE TABLE Inmates (
    id integer primary key,
    Execution text,
    Lastname text,
    Firstname text,
    TDCJNumber text,
    Age integer,
    Date text,
    Race text,
    County text,
    Laststatement text,
    LastStatementURL text,
    InmateInformation text)""")
conn.commit()

url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
data = requests.get(url, verify=False).text
soup = BeautifulSoup(data, "html.parser")
table = soup.find('table', attrs={'class': "tdcj_table indent"})

for row in table.find_all("tr")[1:]:
    cells = row.find_all('td')
    ExecutionID = str(cells[0].get_text())
    InmateInformation = 'https://www.tdcj.texas.gov/death_row/' + cells[1].a['href']
    link_tag = cells[2].find('a')
    if link_tag:
        linkLS = 'https://www.tdcj.texas.gov/death_row/' + link_tag['href']
    else:
        linkLS = 'https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html'

    Lastname = str(cells[3].get_text())
    Firstname = str(cells[4].get_text())
    TDCJ = str(cells[5].get_text())  # <- fixed variable name
    Age = int(cells[6].get_text())
    Date = datetime.strptime(cells[7].get_text(), '%m/%d/%Y').date()
    Race = str(cells[8].get_text())
    County = str(cells[9].get_text())

    print(f"--- retrieving execution data for execution ID {ExecutionID}, {Lastname}, {Firstname} ---")

    if ExecutionID == "545":
        linkLS = "https://www.tdcj.texas.gov/death_row/dr_info/cardenasrubenlast.html"
    elif ExecutionID == "544":
        linkLS = "https://www.tdcj.texas.gov/death_row/dr_info/pruettrobertlast.html"
    elif ExecutionID == "552":
        linkLS = "https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html"

    print(f"--- retrieving statement for execution ID {ExecutionID}, {Lastname}, {Firstname} ---")
    
    try:
        response = requests.get(linkLS, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        pattern = re.compile("Last Statement:")
        p = soup.find(string=pattern)
        if p:
            next_para = p.find_next('p')
            statement = next_para.get_text(strip=True) if next_para else ""
        else:
            statement = ""
        statement = statement.replace("<span class=", "")
        statement = statement.replace("</span>", "")
        statement = statement.replace('"', "")
        statement = statement.replace("text_italic>", "")
    except Exception as e:
        print(f"An error has occurred while retrieving the statement. Proceeding... ({e})")
        statement = ""
        continue

    cur.execute("""INSERT OR IGNORE INTO Inmates 
        (Execution, Lastname, Firstname, TDCJNumber, Age, Date, Race, County, Laststatement, LastStatementURL, InmateInformation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (ExecutionID, Lastname, Firstname, TDCJ, Age, str(Date), Race, County, statement, linkLS, InmateInformation))

conn.commit()
conn.close()
print("Retrieval complete. Open deathrow.sqlite to see the data. Execute gword.py to create the wordcloud.")
