"""
===============================================================
PROJECT 2: DATA CLASSIFICATION USING AI
DecodeLabs - Industrial Training Kit (Batch 2026)
Goal: Build a basic classification model using the Iris dataset
Pipeline: INPUT -> PROCESS -> OUTPUT (IPO Framework)
Algorithm: K-Nearest Neighbors (KNN)
===============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix, classification_report,
    accuracy_score, ConfusionMatrixDisplay
)

np.random.seed(42)   # Fixed seed -> reproducible shuffle

# --------------------- 1. INPUT: LOAD DATASET ---------------------
# Iris dataset = 150 samples, 3 classes, 4 features (the "Iris Benchmark")
iris = load_iris()
X = iris.data                       # Features: Sepal/Petal Length & Width
y = iris.target                     # Labels: 0=Setosa, 1=Versicolor, 2=Virginica
class_names = iris.target_names

df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = [class_names[i] for i in y]

print("--- Dataset Loaded ---")
print(f"Samples : {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes : {', '.join(str(c) for c in class_names)}\n")
print(df.head(), "\n")

# --------------- 2. PROCESS: FEATURE SCALING (Gatekeeper Rule) ----
# StandardScaler: mean = 0, variance = 1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------- 3. PROCESS: TRAIN-TEST SPLIT (Shuffle) -----------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,      # 80% train / 20% test
    random_state=42,
    shuffle=True,       # Randomize to remove order bias
    stratify=y          # Keep class balance equal in both sets
)

print("--- Train/Test Split ---")
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples : {X_test.shape[0]}\n")

# --------------- 4. TUNING THE ENGINE: CHOOSING OPTIMAL K ----------
k_values = range(1, 21)
error_rates = []

for k in k_values:
    model_k = KNeighborsClassifier(n_neighbors=k)
    model_k.fit(X_train, y_train)
    pred_k = model_k.predict(X_test)
    error_rates.append(np.mean(pred_k != y_test))

best_k = k_values[np.argmin(error_rates)]

plt.figure(figsize=(7, 4))
plt.plot(k_values, error_rates, marker='o', linestyle='-', color='steelblue')
plt.scatter(best_k, min(error_rates), color='red', s=100, zorder=5, label='Optimal K')
plt.xlabel('K Value')
plt.ylabel('Error Rate')
plt.title('Elbow Method for Optimal K')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('elbow_method.png', dpi=150)
plt.show()

print("--- Optimal K Selected ---")
print(f"Best K = {best_k} (Error Rate = {min(error_rates)*100:.2f}%)\n")

# --------------- 5. THE WORKFLOW: INSTANTIATE -> FIT -> PREDICT ----
model = KNeighborsClassifier(n_neighbors=best_k)   # INSTANTIATE (Build the frame)
model.fit(X_train, y_train)                         # FIT (Memorize the map)
predictions = model.predict(X_test)                 # PREDICT (Apply logic)

# --------------- 6. OUTPUT: CONFUSION MATRIX -----------------------
cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap='Blues')
plt.title('Iris Classification - Confusion Matrix')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.show()

# --------------- 7. OUTPUT: ACCURACY, PRECISION, RECALL, F1 --------
accuracy = accuracy_score(y_test, predictions)
print("--- Output Validation ---")
print(f"Overall Accuracy: {accuracy*100:.2f}%\n")

print("Classification Report (Precision / Recall / F1-Score):")
print(classification_report(y_test, predictions, target_names=class_names))

print("Project 2 pipeline complete: Load -> Scale -> Split -> Train -> Predict -> Validate.")
