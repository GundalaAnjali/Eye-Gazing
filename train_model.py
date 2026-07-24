import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# ---------------- LOAD DATA ----------------
df = pd.read_csv("eye_data.csv")

print("\nCSV Columns Found:")
print(df.columns)

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip()

# ---------------- FEATURES ----------------
X = df[[
    "Left_X",
    "Left_Y",
    "Right_X",
    "Right_Y",
    "Norm_X",
    "Norm_Y"
]]

# ---------------- LABEL ----------------
y = df["Gaze_Direction"]

# ---------------- ENCODE LABELS ----------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# ---------------- SPLIT DATA ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, pred))

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "gaze_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("\nModel saved successfully!")
