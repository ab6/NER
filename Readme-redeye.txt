1. Download and unzip Stanford NER tagger: http://nlp.stanford.edu/software/CRF-NER.shtml#Download

2. Start Mongo

3. Run createTrainData.py, passing in the path to the tagger and the root folder of the training data

4. Annotate resulting training file: tagged.txt

5. Ensure that testProperties.prop is in stanford folder and that the first line of the file has the actual path to the corrected training file

6. Train model with the following command:
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop testProperties.prop

Command to test model
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier test-ner-model.ser.gz -testFile trainData.txt

7. Run tagData-slash.py
	Parameters: Folder path for the ner tagger
				Name of the additional trained model (test-ner-model.ser.gz, unless changed in the testProperties.prop file before step 6)
				-tag and the folder path for the data (to tag data)
				-test and path to tagged test document and path to plain text (to test system)