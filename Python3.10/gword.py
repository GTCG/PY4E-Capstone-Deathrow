import sqlite3
import time
import urllib
import zlib
import string
import os.path


base_dir= os.path.dirname("C:\\capstone revisited\\python3.5\\gmane\\")
db_path = os.path.join(base_dir, "Deathrow.sqlite")
conn = sqlite3.connect(db_path)
conn.text_factory = str
cur = conn.cursor()
cur.execute('''SELECT Laststatement FROM Inmates''')
nostat = ["This offender declined to make a last statement." , "no last statement given." , "no statement was made." , "no statement given." , "None" , "Written statement",  "No last statement"]
counts = dict()
for message_row in cur :
	text = message_row[0]
	if text in nostat:
		text = ""
	text = text.translate({ord(i):None for i in string.punctuation}) 
	text = text.translate({ord(i):None for i in '1234567890'})
	text = text.replace("\u2019", "'")
	text = text.strip()
	text = text.lower()
	words = text.split()
	list=["this", "that", "have", "know", "will", "want", "would", "with", "been", "give", "done", "statement", "these", "some", "things", "must", "bring", "made" "like",
	    "what", "yall", "there", "them", "make", "just", "going", "tell", "they", "take", "here", "from", "when", "find", "back", "much", "only", "very", "still", "said", "were", "declined", "each", "cant",
		"more", "down", "ones", "where", "y'all", "dont", "warden", "keep", "again", "made", "thing", "like", "right", "their", "thats", "could", "those",
		 "didnt","well", "told", "your", "words", "guys", "doing", "long", "into", "name", "look", "mean", "even", "move", "side", "don't", "happy", "hold", "need",
		 "every", "part","shall","else"]
	for word in words:
		if len(word) < 4 or word in list : continue
		counts[word] = counts.get(word,0) + 1

# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for w in words[:100]:
	if highest is None or highest < counts[w] :
		highest = counts[w]
	if lowest is None or lowest > counts[w] :
		lowest = counts[w]
print ('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in words[:100]:
	if not first : fhand.write( ",\n")
	first = False
	size = counts[k]
	size = (size - lowest) / float(highest - lowest)
	size = int((size * bigsize) + smallsize)
	fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print ("Output written to gword.js")
print ("Open gword.htm in a browser to view")
