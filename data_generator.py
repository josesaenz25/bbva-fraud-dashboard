import pandas as pd
import numpy as np

np.random.seed(42)
users = [f"user_{i}" for i in range(1, 11)]
data = []

for user in users:
    for _ in range(100):
        amount = round(np.random.exponential(scale=200), 2)
        hour = np.random.randint(0, 24)
        channel = np.random.choice(["web", "mobile", "ATM"])
        is_fraud = np.random.choice([0, 1], p=[0.95, 0.05])
        data.append([user, amount, hour, channel, is_fraud])

df = pd.DataFrame(data, columns=["user_id", "amount", "hour", "channel", "is_fraud"])
df.to_csv("data/users_transactions.csv", index=False)
print("Archivo generado correctamente.")
