##Iterates over documents in mongo database and pulls out sampling.
##Tags that sampling and formats the output to a file.
##Parameters: Folder path for ner tagger and for root folder of data where you want output.


from pymongo import MongoClient
import base64
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Tag plain text.')
parser.add_argument('nerPath', help='Folder path for ner tagger.')
parser.add_argument('rootFolder', help='Folder path for root folder of data.')
args = parser.parse_args()

ner = args.nerPath
folder = args.rootFolder

client = MongoClient()
db = client.test
posts = db.redeye
cursor = posts.find({ "text": { "$exists": True }}, [ "text" ])

train = open(folder + "\\train.txt", 'w')
output = folder + "\\tagged.txt"
count = 1
length = 0
for post in cursor:
	if count%12 == 0:
		text = base64.b64decode(post["text"]).split()
		if len(text) < 200:
			train.write(" ".join(text) + "\n")
			length = length + len(text)
		else:
			train.write(" ".join(text[:200]) + "\n")
			length = length + 200

	if length > 8000:
		break
	count = count + 1

train.close()

tagged = subprocess.check_output(["java", "-mx1500m", "-cp", ner + "\\stanford-ner.jar", "edu.stanford.nlp.ie.crf.CRFClassifier", 
	"-loadClassifier", ner + "\\classifiers\\english.all.3class.distsim.crf.ser.gz", "-textFile", folder + "\\train.txt", "-outputFormat", "slashTags"])

f = open(output, 'w')
for line in tagged.split("\n"):
	for word in line.split():
		f.write(word.replace("/", "\t") + "\n")
	f.write("\n")
f.close()