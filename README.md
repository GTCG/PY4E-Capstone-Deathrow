# Deathrow

1)What it does:
* It creates a database in Sqlite, being deathrow.sqlite, with table "Inmates"
* It retrieves the data and the statements from each inmate
* It imports this cleaned data into the database deathrow.sqlite, in table "Inmates"
* Create a word cloud with the most common words in the last statements of the inmates.(Optional)

2)Requirements:
* Python ofcourse, being at least v 2.7 or higher
* Sqlite which can be downloaded from https://sqlite.org/
* BeautifulSoup4 module which can be downloaded via pip in python 3.5. for python 2.7 one has to download pip manually. Plenty of guides can be found on the net explaining how to handle this.

3)Howto:
* Download all the files
* Run "Deathrow.py". Make sure you select the correct version, beging Python 2.7 or 3.6
* Check deathrow.sqlite to verify if the data is actually in the database
* Run gword.py. This program will create gword.js, in which the most common words are being stored.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js
* See the beauty of the word cloud :)
