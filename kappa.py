from sklearn.metrics import cohen_kappa_score

#y1 = ["negative", "positive", "negative", "neutral", "positive"]
#y2 = ["negative", "positive", "negative", "neutral", "negative"]
#cohen_kappa_score(y1, y2)

true_classification =[]
predicted_classification = []

input = "post_tsegmentator_cac_400.txt"
threshold = [100, 400]
#calculates kappa coefficient with each threshold
for t in threshold:
    with open(input, 'r') as inputfile:
        #each line in the inputfile contains predicted and true cac scores for a given image
        for line in inputfile:
            true_class = float(line.split(",")[1].split(":")[1].strip())
            predicted_class = float(line.split(",")[2].split(":")[1].strip())
            #print(true_class, predicted_class)
            
            #after appending a classification in both true and predicted, since this is done line by line
            #index among both lists will correspond to the same image
            if true_class>= t:
                true_classification.append("positive")
            if true_class<t:
                true_classification.append("negative")
            if predicted_class >= t:
                predicted_classification.append("positive")
            if predicted_class<t:
                predicted_classification.append("negative")
    #print(len(true_classification), len(predicted_classification))
    k = cohen_kappa_score(true_classification, predicted_classification)
    print(f" CAC threshold is {t}, and kappa is {k}")
    predicted_classification.clear()
    true_classification.clear()
