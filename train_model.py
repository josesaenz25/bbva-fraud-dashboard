import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

df = pd.read_csv("data/users_transactions.csv")
X = df[["amount", "hour"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fraud_model.pkl")
