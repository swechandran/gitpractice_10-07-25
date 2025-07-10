import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from xgboost import XGBClassifier

# Load preprocessed data
df = pd.read_csv("F:/Feature_Engineering_12-06-25/output/step2-Categorized_Components.csv")

# Drop rows with missing target values
df = df.dropna(subset=['ui_component'])

# Encode target column
label_encoder = LabelEncoder()
df['ui_component'] = label_encoder.fit_transform(df['ui_component'])
y = df['ui_component']

# Select only the specified features
selected_features = [
    'absoluteBoundingBox_height', 'absoluteBoundingBox_width',
    'absoluteBoundingBox_x', 'absoluteBoundingBox_y',
    'absoluteRenderBounds_height', 'absoluteRenderBounds_width',
    'absoluteRenderBounds_x', 'absoluteRenderBounds_y',
    'backgroundColor_a', 'backgroundColor_b',
    'backgroundColor_g', 'backgroundColor_r',
    'clipsContent'
]

X = df[selected_features].fillna(0)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Compute class weights for imbalance
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y), y=y)
class_weight_dict = dict(zip(np.unique(y), class_weights))
sample_weights = y_train.map(class_weight_dict)

# Initialize XGBoost model with parameters
model = XGBClassifier(
    n_estimators=50,
    max_depth=5,
    learning_rate=0.01,
    subsample=0.5,
    colsample_bytree=0.5,
    gamma=0.1,
    reg_alpha=0,
    reg_lambda=1,
    use_label_encoder=False,
    eval_metric='mlogloss'
)

# Train the model
model.fit(X_train, y_train, sample_weight=sample_weights)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}\n")

# Classification report with class names
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Confusion Matrix
plt.figure(figsize=(10, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# Show feature importance
plt.figure(figsize=(12, 6))
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)[::-1]
plt.bar(range(len(feature_importance)), feature_importance[sorted_idx], align='center')
plt.xticks(range(len(feature_importance)), X.columns[sorted_idx], rotation=90)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# Save model and label encoder
joblib.dump(model, "xgboost_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("Model and label encoder saved successfully.")
