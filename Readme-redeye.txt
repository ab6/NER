1. Download and unzip Stanford NER tagger: http://nlp.stanford.edu/software/CRF-NER.shtml#Download
	Add the stanford-ner.jar to your classpath

2. Start Mongo and load data (I have only used the ingestion gui)

3. Run createTrainData.py, passing in the path to the tagger and the root folder of the training data

4. Annotate resulting training file (tagged.txt)

5. Ensure that testProperties.prop is in stanford folder and that the first line of the file has the actual path to the corrected training file

6. Train model with the following command from within the tagger folder:
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop testProperties.prop

Command to test model
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier test-ner-model.ser.gz -testFile trainData.txt

7. Run tagData-slash.py
	Parameters: Folder path for the ner tagger
				Name of the additional trained model (test-ner-model.ser.gz, unless changed in the testProperties.prop file before step 6)
				-tag and the folder path for the data and path for output files (to tag data)
				-test and path to tagged test document and path to plain text (to test system)