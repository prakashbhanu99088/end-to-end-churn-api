import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Connect and Load
conn = sqlite3.connect(r"C:\Users\bpmun\OneDrive\Desktop\churn-project\churn.db")
query = "SELECT tenure, MonthlyCharges, TotalCharges, Contract, Churn FROM customers"
df = pd.read_sql(query, conn)
conn.close()

# 2. Preprocessing
# Fix TotalCharges (convert to number)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

# Manual Encoding for 'Contract' so we can replicate it easily in the API
# Month-to-month = 0, One year = 1, Two year = 2
contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
df['Contract'] = df['Contract'].map(contract_mapping)

# 3. Split
X = df[['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract']]
y = df['Churn']
# Encode Target (Yes/No -> 1/0)
y = y.map({'Yes': 1, 'No': 0})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Save
joblib.dump(model, 'model_churn.pkl')
print("New simplified model saved!")