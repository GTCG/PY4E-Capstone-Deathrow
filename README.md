# Retrieve the last statements from inmates on Texas Death Row

I wrote this program as a capstone project for the Python For Everybody Course (PY4E, lecturer is Charles Severance, main website can be found [here](https://py4e.com)). It retrieves the last statements of the executed inmates on Texas death row and shows the 100 most used words in a word cloud, thanks to the D3.js module. More information about the D3.js module can be found [here](https://github.com/d3/d3/zipball/master). The website where you can find these statements (and other information) can be found [here](https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html). There is a version of the program for python 2.7 and 3 versions for Python 3.x. The 2.7 version gets its data from the included csv file which I made on a third party website. I really encourage you to download the newest version which I revised in may 2025 as the code is written far better than the previous version. It is probably the only version which still works.

I've completely redesigned this program in December 2023 and May 2025. I've added multiple bugfixes and small improvements:
* The website seems to have gotten a new URL. Had to fix that in my code.
* Fixed errors where certain statements could not be downloaded because they were linked wrong on the website. Please check the script for details.
* Modified the code so it's faster and more efficient.
* Fixed some bugs in character encoding when the most common words are being read from the SQlite database and are being put in the file gword.js.
* Created a list of exclude a lot of most common words because they are not relevant to display in the word cloud. Words like "there, been, could, ...". Please see gwords.py to see the list.
* Fixed a bug in pywords.py where the output of the program would not show the numbers of the counts of the words that are most the most and least used. I also added the words themselves with the highest and lowest count.
* Added a few extra rows with some more information about the inmates. They were not included in previous versions but I've done a small effort into including them.
* Other minor bug fixes and improvements.
* Since May 2025: Better error handeling in case certain HTML elements are not found in the structure of the website. The last statement were not always in the same HTML code, so I had to write extra code to catch those (case 1-4 in the script)
* Since May 2025: Minor bugfixes + added a sleep timer of 0.5 after the retrieval of relevant information of each inmate so the website doesn't get hammered
* Since May 2025: fixed some typo's that were in the code
* Since May 2025: The retrieval of the statements has now been written into a function
* Since May 2025: added a user agent to prevent from being blocked while scraping
* Since May 2025: I included a requirements.txt file for easier installation

**1)What the program does:**
* It creates a database called deathrow.sqlite, with the table "Inmates" and a bunch of rows which include information about the inmates.
* It retrieves the data and the statements from each inmate from the death row while counting each retrieval.
* It imports this cleaned data into the database deathrow.sqlite, in the table "Inmates".
* It creates a word cloud with the most common words in the last statements of the inmates. Instruction of how this is done can be seen after running the program.

**2)Requirements:**
* Python ofcourse, being at least v 2.7 or higher [download python](http://www.python.org).
* Notepad++, Visual Studio Code, or whatever suits your needs
* The modules which you can find in the requirements.txt file (use: pip install -r requirements.txt) for installation
* Sqlite, which can be downloaded from [here](https://sqlitebrowser.org/dl/).

**3)Howto:**
* Download all the files which are compatible with your Python version (which will probably be the lastest version)
* Run "Deathrow.py". It will run for a few minutes. You can check the output to see if it retrieves each statement correctly.
* Check deathrow.sqlite to verify if the data is actually in the database. You should have one table called "Inmates" which has all the information you need.
* Run gword.py. This program will create gword.js, in which the most 100 common words are being stored, except those that are in the "ignore" list in gword.py. These are meaningless words like "are, you, be, ...". Feel free to modify this list.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js. This cloud needs d3.layout.cloud.js and d3.v2 to run. Feel free to check and modify the gword.htm file to suit your needs.
* See the beauty of the word cloud :)

Feel free to report bugs, fixes, or stuff to make the program better.
