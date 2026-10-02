import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

from datetime import datetime
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Ignore future warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)

# Set visual style
sns.set(color_codes=True)
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================
# 1. Load Data
# ==========================================
df = pd.read_csv('data_for_predictions.csv')

if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)

print("Dataset Shape:", df.shape)
df.head()

# ==========================================
# 2. Data Sampling (Train-Test Split)
# ==========================================
# Separate target variable (churn) from features
y = df['churn']
X = df.drop(columns=['id', 'churn'])

print("Features Shape (X):", X.shape)
print("Target Shape (y):", y.shape)

# Train-test split (75% training, 25% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("\nTrain samples:", X_train.shape[0])
print("Test samples: ", X_test.shape[0])

# ==========================================
# 3. Model Training (Random Forest)
# ==========================================
# Instantiate Random Forest Classifier
model = RandomForestClassifier(
    n_estimators=1000,
    random_state=42,
    n_jobs=-1
)

# Train the model
model.fit(X_train, y_train)
print("\nModel training complete.")

# ==========================================
# 4. Model Predictions & Evaluation
# ==========================================
# Predict test class labels and probability scores
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

# Calculate key evaluation metrics
accuracy = metrics.accuracy_score(y_test, predictions)
precision = metrics.precision_score(y_test, predictions, zero_division=0)
recall = metrics.recall_score(y_test, predictions, zero_division=0)
f1 = metrics.f1_score(y_test, predictions, zero_division=0)
roc_auc = metrics.roc_auc_score(y_test, probabilities)

print("\n--- Model Performance Metrics ---")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

print("\nClassification Report:")
print(metrics.classification_report(y_test, predictions, target_names=['Retained (0)', 'Churned (1)']))

# ==========================================
# 5. Visualizing Confusion Matrix & ROC
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Confusion Matrix Heatmap
cm = metrics.confusion_matrix(y_test, predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Retained (0)', 'Churned (1)'],
            yticklabels=['Retained (0)', 'Churned (1)'])
axes[0].set_title('Confusion Matrix', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Predicted Label')
axes[0].set_ylabel('Actual Label')

# ROC Curve
fpr, tpr, _ = metrics.roc_curve(y_test, probabilities)
axes[1].plot(fpr, tpr, color='#2b5c8f', lw=2, label=f'Random Forest (AUC = {roc_auc:.3f})')
axes[1].plot([0, 1], [0, 1], color='gray', linestyle='--')
axes[1].set_title('ROC Curve', fontsize=12, fontweight='bold')
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('True Positive Rate')
axes[1].legend(loc='lower right')

plt.tight_layout()
plt.show()

# ==========================================
# 6. Feature Importance Analysis
# ==========================================
feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importances.head(10).values, y=feature_importances.head(10).index, palette='crest')
plt.title('Top 10 Feature Importances for Churn Prediction', fontsize=12, fontweight='bold')
plt.xlabel('Gini Importance')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()

print("\nTop 10 Feature Importances:")
print(feature_importances.head(10))