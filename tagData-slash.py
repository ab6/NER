import argparse
import subprocess
import os
import re

parser = argparse.ArgumentParser(description='Tag plain text.')
parser.add_argument('nerPath', help='Folder path for ner tagger.')
parser.add_argument('modelName', help='Name of the additional trained model.')
parser.add_argument('-tag', help='Folder path for root folder of data.')
parser.add_argument('-test', nargs=2, help='Provide paths to tagged test document and plain text test doc.')
args = parser.parse_args()

ner = args.nerPath
model = args.modelName
folder = args.tag
testFile = args.test[0]
testPlain = args.test[1]

##Need to fix /tab problem in test and training sets

def tag(filePath):
	#previous = ""
	default = subprocess.check_output(["java", "-mx1500m", "-cp", ner + "\\stanford-ner.jar", "edu.stanford.nlp.ie.crf.CRFClassifier", 
		"-loadClassifier", ner + "\\classifiers\\english.all.3class.distsim.crf.ser.gz", "-textFile", filePath, "-outputFormat", "slashTags"])
	custom = subprocess.check_output(["java", "-mx1500m", "-cp", ner + "\\stanford-ner.jar", "edu.stanford.nlp.ie.crf.CRFClassifier", 
		"-loadClassifier", ner + "\\classifiers\\" + model, "-textFile", filePath, "-outputFormat", "slashTags"])
	
	tags = []
	for gold, test in zip(default.split(), custom.split()):
		if not cmp(gold, test) == 0:
			if test.endswith("/O"):
				tags.append(gold)
				#if not cmp(previous[previous.find("/")+1:], gold[gold.find("/")+1:]) == 0:
					#tags.write("\n")
				#tags.write(gold + " ")
				#previous = gold
			else:
				if test.endswith("/OT"):
					tags.append(test.replace("/OT", "/O"))
				else: 
					tags.append(test)
			#if not gold.endswith("/O"):
				#if not cmp(previous[previous.find("/")+1:], test[test.find("/")+1:]) == 0:
					#tags.write("\n")
				#tags.write(test + " ")
			#previous = test
		else:
			tags.append(test)
	#previous = ""
	return tags

def compareTags(gold, test, delimiter):
	tp = 0.0
	fp = 0.0
	fn = 0.0
	total = 0
	for goldToken, testToken in zip(gold, test):
		if goldToken.endswith(delimiter + "O"):
			if not testToken.endswith(delimiter + "O"):
				fp += 1.0
				print goldToken + " " + testToken
		else:
			total += 1
			if testToken.endswith(delimiter + "O"):
				fn += 1.0
			elif cmp(goldToken, testToken) == 0:
				tp += 1.0
			else:
				fp += 1.0
				print goldToken + " " + testToken
	precision = tp / (tp + fp)
	recall = tp / (tp + fn)
	f1 = 2*(precision * recall)/(precision + recall)
	print "tp = " + str(tp)
	print "fp = " + str(fp)
	print "fn = " + str(fn)
	print "total = " + str(total)
	print "precision = " + str(precision)
	print "recall = " + str(recall)
	print "f1 = " + str(f1)

if folder:
	for root, directory, files in os.walk(folder):
		for name in files:
			if name.find(".tagged") == -1:
				filePath = os.path.join(root, name)
				tags = tag(filePath)
				h = open(filePath + ".tagged", 'w')
				for tag in tags:
					h.write(tag.replace("/", "\t") + "\n")
				h.close()

if testFile:
	test = open(testFile, 'r')
	testTagged = test.read()
	test.close()
	tags = tag(testPlain)
	results = compareTags(testTagged.replace("\t", "/").split(), tags, "/")