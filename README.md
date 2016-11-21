# Retrieve the last statements from deathrow-inmates

I wrote a program which retrieves the last statements of the executed inmates on death row. The website where you can these statements can be found [here](https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html). There is a version of the program for python 2.7 and one for Python 3.x.

**1)What it does:**
* It creates a database in Sqlite, being deathrow.sqlite, with table "Inmates"
* It retrieves the data and the statements from each inmate
* It imports this cleaned data into the database deathrow.sqlite, in table "Inmates"
* Create a word cloud with the most common words in the last statements of the inmates.(Optional)

**2)Requirements:**
* Python ofcourse, being at least v 2.7 or higher
* Sqlite which can be downloaded from https://sqlite.org/
* BeautifulSoup4 module which can be downloaded via pip in python 3.5. for python 2.7 one has to download pip manually. Plenty of guides can be found on the net explaining how to handle this.

**3)Howto:**
* Download all the files
* Run "Deathrow.py". Make sure you select the correct version: Python 2.7 or 3.6
* Check deathrow.sqlite to verify if the data is actually in the database
* Run gword.py. This program will create gword.js, in which the most common words are being stored.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js
* See the beauty of the word cloud :)

I've also made a small screencast with an explanation of how the program works.
<a href="http://www.youtube.com/watch?feature=player_embedded&v=R2cGUJTw6lc
" target="_blank"><img src="http://img.youtube.com/vi/R2cGUJTw6lc/0.jpg" 
alt="Capstone" width="240" height="180" border="10" /></a>


Feel free to report bugs, fixes, or stuff to make the program better in general.
