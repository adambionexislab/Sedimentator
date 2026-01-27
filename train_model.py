import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Load the actual data file
df = pd.read_csv("db_sedimentator.csv")

# Check that the column names match your file
print("Columns in CSV:", df.columns.tolist())

# Features and target
FEATURES = ["COD", "SVI", "SS", "FLOW", "FLOCCULANT"]
TARGET = "SLUDGE"

X = df[FEATURES]
y = df[TARGET]

# Time-based split: first 80% for training, last 20% for testing
split_index = int(len(df) * 0.8)
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Model (conservative for small dataset)
model = XGBRegressor(
    n_estimators=150,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_alpha=1.0,
    reg_lambda=5.0,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
print(f"Validation MAE: {mae:.2f} cm")

# Save model
joblib.dump(model, "flocculant_model.pkl")
print("Model saved as 'flocculant_model.pkl'")

# Compute 95th percentile dose for safety max dose
dose_95 = np.percentile(df["FLOCCULANT"], 95)
safe_max_dose = round(dose_95 * 1.5, 2)
print(f"Suggested DEFAULT_MAX_DOSE = {safe_max_dose}")
print("➡️ Copy this value into config.py")
