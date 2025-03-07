# -----------------------------
#   USAGE
# -----------------------------
# python train_svr_grid.py

# -----------------------------
#   IMPORTS
# -----------------------------
# Import the necessary packages
from pyimagesearch import config
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import pandas as pd

# Load the dataset, separate the features and the labels, and then perform a training and testing split using
# 85% of the data for training and 15% for evaluation
print("[INFO] Loading dataset...")
dataset = pd.read_csv(config.CSV_PATH, names=config.COLS)
dataX = dataset[dataset.columns[:-1]]
dataY = dataset[dataset.columns[-1]]
(trainX, testX, trainY, testY) = train_test_split(dataX, dataY, random_state=3, test_size=0.15)

# Standardize the feature values by computing the mean, subtracting the mean from the data points and then dividing by
# the standard deviation
scaler = StandardScaler()
trainX = scaler.fit_transform(trainX)
testX = scaler.transform(testX)

# Initialize the model and define the space of the hyperparameters to perform the grid-search over
print("[INFO] Initializing the support vector regression model...")
model = SVR()
kernel = ["linear", "rbf", "sigmoid", "poly"]
tolerance = [1e-3, 1e-4, 1e-5, 1e-6]
C = [1, 1.5, 2, 2.5, 3]
grid = dict(kernel=kernel, tol=tolerance, C=C)

# Initialize a cross-validation fold and perform a grid-search to tune the hyperparameters
print("[INFO] Grid searching over the hyperparameters...")
cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
gridSearch = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cvFold, scoring="neg_mean_squared_error")
searchResults = gridSearch.fit(trainX, trainY)

# Extract the best model and evaluate it
print("[INFO] Evaluating the model...")
bestModel = searchResults.best_estimator_
print("R2: {:.2f}".format(bestModel.score(testX, testY)))



