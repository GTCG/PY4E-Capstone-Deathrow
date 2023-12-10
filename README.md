# Retrieve the last statements from inmates on Texas Death Row

I wrote a program which retrieves the last statements of the executed inmates on Texas death row and shows the 100 most used words in a word cloud, thanks to the D3.js module. More information about the D3.js module can be found [here](https://github.com/d3/d3/zipball/master). The website where you can find these statements (and other information) can be found [here](https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html). There is a version of the program for python 2.7 and 2 versions for Python 3.x. The 2.7 version gets its data from the included csv file which I made on a third party website. I really encourage you to download the 3.10  version -which I made around December 2023- as it is much, much better. Version 3.10 is probably the only version which still works because the website of Texas death row seems to have changed over the last couple of years.

I've completely redesigned this program since December 2023. I've added multiple bugfixes and small improvements:
* The website seems to have gotten a new URL. Had to fix that in my code.
* Fixed errors where certain statements could not be downloaded because they were linked wrong on the website. Please check the script for details.
* Modified the code so it's faster and more efficient.
* Fixed some bugs in character encoding when the most common words are being read from the SQlite database and are being put in the file gword.js.
* Created a list of exclude a lot of most common words because they are not relevant to display in the word cloud. Words like "there, been, could, ...". Please see gwords.py to see the list.
* Fixed a bug in pywords.py where the output of the program would not show the numbers of the counts of the words that are most the most and least used.
* Added a few extra rows with some more information about the inmates. They were not included in previous versions but I've done a small effort into including them.
* Other minor bug fixes and improvements.

I've also updated this readme.

**1)What the program does:**
* It creates a database called deathrow.sqlite, with the table "Inmates" and a bunch of rows which include information about the inmates.
* It retrieves the data and the statements from each inmate from the death row while counting each retrieval.
* It imports this cleaned data into the database deathrow.sqlite, in the table "Inmates".
* It creates a word cloud with the most common words in the last statements of the inmates. Instruction of how this is done can be seen after running the program.

**2)Requirements:**
* Python ofcourse, being at least v 2.7 or higher [download python](http://www.python.org).
* Notepad++, or Visual Studio Code, or use your own preference.
* Sqlite, which can be downloaded from [here](https://sqlitebrowser.org/dl/).
* BeautifulSoup4 module which can be downloaded via pip. For python 2.7 I have put the module in the folder.

**3)Howto:**
* Download all the files which are compatible with your Python version which will most likely be the latest.
* Run "Deathrow.py". It will run for a few minutes. You can check the output to see if it retrieves each statement correctly.
* Check deathrow.sqlite to verify if the data is actually in the database.
* Run gword.py. This program will create gword.js, in which the most 100 common words are being stored, except those that are in the list in gword.py.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js.
* See the beauty of the word cloud :)

Feel free to report bugs, fixes, or stuff to make the program better. See you in another 7 years!
