import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("final_trial_risk_dataset.csv")

print("Dataset Shape:", df.shape)


# ===============================
# INPUT / OUTPUT
# ===============================
X = df.drop("Outcome", axis=1)
y = df["Outcome"]


# ===============================
# TRAIN TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y   # handles imbalance
)


# ===============================
# MODEL
# ===============================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)


# ===============================
# TRAIN
# ===============================
model.fit(X_train, y_train)


# ===============================
# TEST
# ===============================
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nModel Accuracy:", round(acc*100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, pred))


# ===============================
# SAVE MODEL
# ===============================
joblib.dump(model, "trial_risk_model.pkl")

print("\nModel saved as trial_risk_model.pkl")
