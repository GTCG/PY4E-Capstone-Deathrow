import sqlite3
import re
from bs4 import BeautifulSoup
import requests
import urllib3
from datetime import datetime
from urllib.parse import urljoin
import time

def extract_last_statement(url, headers):
    try:
        response = requests.get(url, verify=False, headers=headers)
        response.encoding = 'windows-1252'
        soup = BeautifulSoup(response.text, "html.parser")

        statement = ""
        # Case 1: <p class="bold">Last Statement:</p>
        for p in soup.find_all('p', class_='bold'):
            if "last statement" in p.get_text(strip=True).lower():
                next_p = p.find_next_sibling('p')
                if next_p:
                    statement = next_p.get_text(separator="\n", strip=True)
                break

        # Case 2: <p><span class="bold">Last Statement:</span></p>
        if not statement:
            for p in soup.find_all('p'):
                span = p.find('span', class_='bold')
                if span and 'last statement' in span.get_text(strip=True).lower():
                    next_p = p.find_next_sibling('p')
                    if next_p:
                        statement = next_p.get_text(separator="\n", strip=True)
                    break

        # Case 3: <p><strong>Last Statement:</strong></p>
        if not statement:
            for p in soup.find_all('p'):
                strong = p.find('strong')
                if strong and 'last statement' in strong.get_text(strip=True).lower():
                    next_p = p.find_next_sibling('p')
                    if next_p:
                        statement = next_p.get_text(separator="\n", strip=True)
                    break

        # Case 4: fallback sibling or text node
        if not statement:
            for p in soup.find_all('p', class_='bold'):
                if "last statement" in p.get_text(strip=True).lower():
                    next_elem = p.find_next_sibling()
                    if next_elem:
                        statement = next_elem.get_text(strip=True) if hasattr(next_elem, 'get_text') else str(next_elem).strip()
                    if not statement and p.next_sibling:
                        next_sib = p.next_sibling
                        statement = next_sib.get_text(strip=True) if hasattr(next_sib, 'get_text') else str(next_sib).strip()
                    break
        statement = statement.replace("<span class=", "").replace("</span>", "").replace('"', "")
        statement = statement.replace("text_italic>", "")
        statement = statement.replace('’', "'").replace('‘', "'")
        statement = statement.replace('“', '"').replace('”', '"').strip()

        corrections = {
            'â€™': "'", 'â€˜': "'", 'â€œ': '"', 'â€': '"', 'â€”': '—',
            'â€“': '-', 'â€¦': '...', 'Â': '', 'Ã©': 'é', 'Ã¨': 'è', 'Ã': 'à'
        }
        for bad, good in corrections.items():
            statement= statement.replace(bad,good)
        return statement
    
    except Exception as e:
        print(f"An error occurred while retrieving the statement: {e}")
        return ""

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

base_url = 'https://www.tdcj.texas.gov/death_row/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
data = requests.get(url, verify=False, headers=headers).text
soup = BeautifulSoup(data, "html.parser")
table = soup.find('table', attrs={'class': "tdcj_table indent"})

for row in table.find_all("tr")[1:]:
    cells = row.find_all('td')
    ExecutionID = str(cells[0].get_text())
    InmateInformation = urljoin(base_url, cells[1].a['href'])

    link_tag = cells[2].find('a')
    if link_tag:
        linkLS = urljoin(base_url, link_tag['href'])
    else:
        linkLS = 'https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html'

    Lastname = str(cells[3].get_text())
    Firstname = str(cells[4].get_text())
    TDCJ = str(cells[5].get_text()) 
    Age = int(cells[6].get_text())
    Date = datetime.strptime(cells[7].get_text(), '%m/%d/%Y').date()
    Race = str(cells[8].get_text())
    County = str(cells[9].get_text())

    print(f"--- retrieving execution data for execution ID {ExecutionID}, {Lastname}, {Firstname} ---")
    print(f"--- retrieving statement for execution ID {ExecutionID}, {Lastname}, {Firstname} ---")
    statement = extract_last_statement(linkLS, headers)

    if not statement:
            print(f"No valid last statement found for execution ID {ExecutionID}, {Lastname}, {Firstname}")
    time.sleep(0.5)
    
 
    cur.execute("""INSERT OR IGNORE INTO Inmates 
        (Execution, Lastname, Firstname, TDCJNumber, Age, Date, Race, County, Laststatement, LastStatementURL, InmateInformation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (ExecutionID, Lastname, Firstname, TDCJ, Age, str(Date), Race, County, statement, linkLS, InmateInformation))

conn.commit()
conn.close()
print("Retrieval complete. Open deathrow.sqlite to see the data. Execute gword.py to create the wordcloud. Open gword.htm after that. Make sure the files d3.layout.cloud and d3.v2 are in your working directory")
