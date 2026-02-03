import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# -----------------------------
# Load data
# -----------------------------
DATA_PATH = "data/db_oxygen.csv"

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Features and target
# -----------------------------
X = df[["COD", "FLOW", "TEMPERATURE"]]
y = df["AIRFLOW"]

# -----------------------------
# Train / test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

# -----------------------------
# Train
# -----------------------------
model.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
y_pred = model.predict(X_test)

print("R2 score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))

# -----------------------------
# Save model
# -----------------------------
MODEL_PATH = "models/oxygen_model.pkl"
joblib.dump(model, MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")
