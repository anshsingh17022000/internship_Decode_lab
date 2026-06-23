# Project 2: Data Classification Using AI
**DecodeLabs — Industrial Training Kit (Batch 2026)**

## 📌 Objective
Build a basic supervised learning classification model that learns patterns from
labeled data and predicts the correct category for new, unseen samples. This
project uses the **Iris flower dataset** and a **K-Nearest Neighbors (KNN)**
classifier to demonstrate the full ML pipeline: Input → Process → Output.

## 📁 Files in this Submission
| File | Description |
|------|-------------|
| `iris_knn_classification.py` | Main Python script — full pipeline |
| `Project2_Report.docx` | Formatted project report with results & graphs |
| `elbow_method.png` | Graph used to choose the optimal K value |
| `confusion_matrix.png` | Output validation — model performance |
| `console_output.txt` | Raw terminal output from running the script |

## 🧠 Dataset
- **Source:** `sklearn.datasets.load_iris()`
- **Samples:** 150 (50 per class — balanced)
- **Classes:** Setosa, Versicolor, Virginica
- **Features:** Sepal Length, Sepal Width, Petal Length, Petal Width (cm)

## ⚙️ Pipeline / Methodology
1. **Load** the Iris dataset
2. **Scale** features using `StandardScaler` (mean = 0, variance = 1)
3. **Split** data — 80% training / 20% testing (stratified, shuffled)
4. **Tune K** — tested K = 1 to 20, plotted error rate, picked the elbow point
5. **Train** the model — `KNeighborsClassifier(n_neighbors=best_k)`
6. **Predict** on the test set
7. **Validate** — Confusion Matrix, Accuracy, Precision, Recall, F1-Score

## ▶️ How to Run
```bash
pip install scikit-learn pandas numpy matplotlib seaborn
python iris_knn_classification.py
```
Running the script will print results to the console and save
`elbow_method.png` and `confusion_matrix.png` in the same folder.

## 📊 Results
| Metric | Value |
|--------|-------|
| Optimal K | 1 |
| Overall Accuracy | **96.67%** |
| Setosa F1-Score | 1.00 |
| Versicolor F1-Score | 0.95 |
| Virginica F1-Score | 0.95 |

Out of 30 test samples, **29 were classified correctly** — the model
confused only one Virginica sample with Versicolor, which is expected since
these two classes have overlapping petal measurements.

## 🛠️ Tools & Libraries
- Python 3
- scikit-learn
- pandas, numpy
- matplotlib, seaborn

## ✅ Conclusion
The KNN model successfully learned to classify Iris flowers with high
accuracy, completing the core supervised learning pipeline required for
Project 2 — Data Classification Using AI.
