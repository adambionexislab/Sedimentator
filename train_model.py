import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv("db_sedimentator.csv")

# Create theoretical sludge exactly as requested
df["TEORETICAL_SLUDGE"] = df["FLOCCULANT"] * df["SLUDGE"]

FEATURES = ["COD", "SVI", "SS", "FLOW"]
TARGET = "TEORETICAL_SLUDGE"

X = df[FEATURES]
y = df[TARGET]

# Time-based split
split = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = XGBRegressor(
    n_estimators=200,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)

print(f"MAE (theoretical sludge units): {mae:.2f}")

joblib.dump(model, "flocculant_model.pkl")
print("Model saved as flocculant_model.pkl")
