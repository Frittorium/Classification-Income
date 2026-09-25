# Income Classification: One-Page Summary

## Overview

This project addresses binary income classification using the Adult Income dataset, which contains demographic, educational, employment, and financial attributes. The prediction target is whether an individual’s annual income is above $50,000 (`>50K`) or at or below $50,000 (`<=50K`). The task is a supervised classification problem that explores how these attributes relate to income category.
The dataset was prepared by handling missing-value markers in selected categorical fields and consolidating education categories into broader ordered groups. Categorical variables were transformed using binary and one-hot encoding. The resulting features were standardized and divided into training and test sets.

Several classification approaches were evaluated using stratified five-fold cross-validation and F1 score for model comparison. The notebook also includes a one-dimensional convolutional neural network experiment with Optuna-based hyperparameter tuning. A Gradient Boosting classifier was selected for the application’s prediction workflow, and its fitted model and preprocessing components were serialized for reuse.

## Rationale and Design Decisions

Missing-value markers in categorical fields were represented as an explicit `Unknown` category so those records could remain in the dataset. Education categories were grouped to reduce the number of distinct levels while retaining an interpretable ordering. Binary and one-hot encoding were used to convert categorical information into numerical features suitable for the selected estimators.

Stratified splitting and cross-validation were used to preserve class proportions during evaluation. F1 score was used as the comparison metric to account for both precision and recall, which is relevant when the two income classes are not equally represented. Saving the model alongside the scaler, encoders, and feature order keeps prediction-time preprocessing consistent with training.

## Implementation

The workflow is implemented in `classification.ipynb`. The `predict.py` module loads the saved Gradient Boosting model and its preprocessing artifacts, transforms a supplied record, and returns a predicted class and the probability associated with the `>50K` class. The `classification_GUI.py` script provides a Tkinter interface for entering a record and displaying the prediction.

The notebook expects the dataset at `dataset/adult.csv`. That dataset is not included in the repository. The trained model, scaler, encoders, and feature-order artifacts are included for the standalone prediction workflow.

## Results and Findings

The project produces a reusable income-classification pipeline and a simple graphical interface for inference. Gradient Boosting is the classifier used by the saved prediction application. The notebook also compares multiple classifiers and experiments with a tuned neural-network approach.

No numerical performance metrics are stated in this summary because verified evaluation scores were not available for confirmation. The model’s output represents a prediction from patterns in the dataset and should not be interpreted as a definitive assessment of an individual’s actual income.
