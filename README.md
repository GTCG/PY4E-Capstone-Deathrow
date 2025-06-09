# Retrieve the last statements from inmates on Texas Death Row

I wrote this program as a capstone project for the Python For Everybody Course (PY4E, lecturer is Charles Severance, main website can be found [here](https://py4e.com)). It retrieves the last statements of the executed inmates on Texas death row and shows the 100 most used words in a word cloud, thanks to the D3.js module. More information about the D3.js module can be found [here](https://github.com/d3/d3/zipball/master). The website where you can find these statements (and other information) can be found [here](https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html). There is a version of the program for python 2.7 and 3 versions for Python 3.x. The 2.7 version gets its data from the included csv file which I made on a third party website. I really encourage you to download the newest version which I revised in may 2025 as the code is written far better than the previous version. It is probably the only version which still works.

I've completely revised this program in December 2023 and in May-June 2025. I've added multiple bugfixes and small improvements:
* The website seems to have gotten a new URL. Had to fix that in my code.
* Fixed errors where certain statements could not be downloaded because they were linked the wrong way on the website.
* Modified the code so it's faster and more efficient.
* Fixed some bugs in character encoding when the most common words are being read from the SQlite database and are being put in the file gword.js.
* Created a list to exclude a lot of most common words because they are not relevant to display in the word cloud. Words like "there", "been", "could", ... . are excluded. Please see gwords.py to see the list.
* Fixed a bug in pywords.py where the output of the program would not show the numbers of the counts of the words that are most the most and least used. I also added the words themselves with the highest and lowest count.
* Added a few extra rows with some more information about the inmates. They were not included in previous versions but I've done a small effort into including them.
* Other minor bug fixes and improvements.
* Since May 2025: Better error handeling in case certain HTML elements are not found in the structure of the website. The last statement were not always in the same HTML tags, so I had to write extra code to catch those (case 1-4 in the script)
* Since May 2025: Minor bugfixes + added a sleep timer of 0.5 after the retrieval of relevant information of each inmate so the website doesn't get hammered.
* Since May 2025: fixed some typo's that were in the code.
* Since May 2025: The retrieval of the statements has now been written into a function.
* Since May 2025: added a user agent to prevent from being blocked/banned from the website while scraping.
* Since May 2025: I included a requirements.txt file for easier installation of the script.
* Since June 2025: Statements which had multiple paragraphs were not fully added into the database. Only the first paragraph was added. This has now been fixed.
* Since June 2025: removed certain quotes (") in the beginning and ending of certain statements. Improved the handling of quotes and other artifacts in the statements.

**1)What the program does:**
* It creates a database called deathrow.sqlite, with the table "Inmates" and a bunch of rows which include information about the inmates.
* It retrieves the data and the statements from each inmate from death row while counting each retrieval.
* It imports this cleaned data into the database deathrow.sqlite, in the table "Inmates".
* It creates a word cloud with the most common words in the last statements of the inmates. Instructions of how this is done can be seen after running deathrow.py.

**2)Requirements:**
* Python ofcourse, being at least v 2.7 or higher [download python](http://www.python.org).
* Notepad++, Visual Studio Code, or whatever suits your needs.
* The modules which you can find in the requirements.txt file (use: pip install -r requirements.txt) for installation.
* Sqlite, which can be downloaded from [here](https://sqlitebrowser.org/dl/).

**3)Howto:**
* Download all the files which are compatible with your Python version (which will probably be the lastest version)
* Run "Deathrow.py". It will run for a few minutes. You can check the output to see if it retrieves each statement correctly.
* Check deathrow.sqlite to verify if the data is actually in the database. You should have one table called "Inmates" which has all the information you need.
* Run gword.py. This program will create gword.js, in which the most 100 common words are being stored, except those that are in the "ignore" list in gword.py. These are meaningless words like "are", "you", "be", .... Feel free to modify this list.
* Open gword.htm to see a word cloud. This cloud is based on the file gword.js. This cloud needs d3.layout.cloud.js and d3.v2 to run. Feel free to check and modify the gword.htm file to suit your needs.
* See the beauty of the word cloud :)

**4)Short video:**
* You can watch a short video about this video here: https://youtu.be/fzju-O1fpfY

**5)Picture of the wordcloud:**

You can see a picture of the wordcloud below. I drew rectangles around the words with the hightest count (love) and the lowest count (wife). This version is of June 2025. 

![Picture of the wordcloud](wordcloud.png)

Feel free to report bugs, fixes, or stuff to make the script even better!
