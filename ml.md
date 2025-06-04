# ML Topics

- Test/Train data
- Confusion Matrix
  - Prediction on the left, Actual on Top
  - Measures prediction for a ML algorithm
  - Compare confusion matrices to determine the most accurate ML algorithm
  - Size is based on the number of things we want to predict
  - True Positives, True Negatives, False Negatives, False Positives
  - Sensitivity = (True Positives)/(True Positives + False Negatives)
  - Specificity = (True Negatives)/(True Negatives + False Positives)

- ROC
  - Graphs that plots (x,y) (False Posititve Rate, True Positive rate)
- AUC (Area Under the Curve)
  - Larger AUC = better ML algorithm
  - If Losistics Regression AUC > Random Forest AUC, then we will pick Logistics Regression