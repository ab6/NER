1. Run createTrainingData.py, passing in the path to the tagger and the root folder of the training data


2. Train model with the following command:
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop testProperties.prop

Command to test model
java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier test-ner-model.ser.gz -testFile trainData.txt


3. 