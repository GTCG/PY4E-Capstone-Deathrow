# Retrieve the last statements from deathrow-inmates

I wrote a program which retrieves the last statements of the executed inmates on death row and shows the most used words in a word cloud, thanks to the D3.js module. More information about the D3.js module can be found [here](https://github.com/d3/d3/zipball/master) The website where you can these statements can be found [here](https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html). There is a version of the program for python 2.7 and a version for Python 3.x. The 2.7 version gets its data from the included csv file which I made on a third party website. I really encourage you to download the 3.x version as it is much, much better and has much better error-handeling.

**1)What it does:**
* It creates a database in Sqlite, being deathrow.sqlite, with the table "Inmates"
* It retrieves the data and the statements from each inmate while counting each retrieval.
* It imports this cleaned data into the database deathrow.sqlite, in the table "Inmates"
* It creates a word cloud with the most common words in the last statements of the inmates. Instruction of how this is done can be seen after running the program.

**2)Requirements:**
* Python ofcourse, being at least v 2.7 or higher [download python](http://www.python.org)
* Sqlite, which can be downloaded from [here](https://sqlite.org/)
* BeautifulSoup4 module which can be downloaded via pip in python 3.5. for python 2.7 I have put the module in the folder.

**3)Howto:**
* Download all the files
* Run "Deathrow.py". Make sure you select the correct version: Python 2.7 or 3.x or expect the program to go haywire.
* Check deathrow.sqlite to verify if the data is actually in the database
* Run gword.py. This program will create gword.js, in which the most common words are being stored.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js
* See the beauty of the word cloud :)

I've also made a small screencast with an explanation of how the program works. Click the image below.



Feel free to report bugs, fixes, or stuff to make the program better.
