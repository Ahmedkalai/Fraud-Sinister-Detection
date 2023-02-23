from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBClassifier

dataset_fraud = pd.read_csv("insurance_fraud_dataset.csv")


def preprodata(dataset):
  dataset.replace('?', np.nan, inplace=True)
  dataset = dataset.drop(columns=["_c39"])
  dataset['collision_type'] = dataset['collision_type'].fillna(dataset['collision_type'].mode()[0])
  dataset['property_damage'] = dataset['property_damage'].fillna("NO")
  dataset['police_report_available'] = dataset['police_report_available'].fillna("NO")
  dataset_clean = dataset.drop(
    columns=["incident_location", "policy_bind_date", "incident_date", "auto_model", "auto_make", "insured_occupation"])
  dataset_clean = dataset_clean.drop(columns=["policy_csl"])
  X = dataset_clean.drop(columns=["fraud_reported"])
  X = X[['policy_number', 'umbrella_limit', 'number_of_vehicles_involved', 'bodily_injuries', 'witnesses',
         'total_claim_amount', 'incident_severity', 'insured_hobbies', 'incident_type', 'authorities_contacted',
         'incident_state']]
  y = dataset_clean["fraud_reported"]
  return X, y


def feature_selection(dataset):
  X, y = preprodata(dataset)
  y = y.replace("Y", 1)
  y = y.replace("N", 0)

  numerical_cols_new = X.select_dtypes(include=['int64', 'float64']).columns
  categorical_cols_new = X.select_dtypes(include=['object']).columns

  scaler = StandardScaler()
  X[numerical_cols_new] = scaler.fit_transform(X[numerical_cols_new])
  X_clean = pd.get_dummies(X, columns=categorical_cols_new, drop_first=True)

  return X_clean, y


def prediction_fraud(policy_number,umbrella_limit,number_of_vehicles_involved,bodily_injuries,witnesses,total_claim_amount):
  X_clean, y = feature_selection(dataset_fraud)
  X_clean = X_clean[['policy_number', 'umbrella_limit', 'number_of_vehicles_involved','bodily_injuries', 'witnesses', 'total_claim_amount']]
  X_train, X_test, y_train, y_test = train_test_split(X_clean, y, test_size=0.25)
  xgb = XGBClassifier()
  xgb.fit(X_train, y_train)
  L= [policy_number, umbrella_limit, number_of_vehicles_involved,bodily_injuries, witnesses, total_claim_amount]
  X_to_predict = pd.DataFrame([L],columns=['policy_number', 'umbrella_limit', 'number_of_vehicles_involved','bodily_injuries', 'witnesses', 'total_claim_amount'])
  resultat = xgb.predict(X_to_predict)
  return resultat


app = Flask(__name__)

CORS(app)


#
#
# http://127.0.0.1:5000/fraudd/784514/50/3/2/2/1000
# prediction_knn(784514, 50, 10, 5, 1000, 0.02)
@app.get("/fraud/<int:policy_number>/<int:umbrella_limit>/<int:number_of_vehicles_involved>/<int:bodily_injuries>/<int:witnesses>/<int:total_claim_amount>")
def calcul(policy_number, umbrella_limit, number_of_vehicles_involved, bodily_injuries, witnesses, total_claim_amount):
  u = prediction_fraud(policy_number, umbrella_limit, number_of_vehicles_involved, bodily_injuries, witnesses,total_claim_amount)

  if u[0] == 0:
    p = 'No Fraud'
  else:
    p = 'Fraud detected'

  return jsonify(p)


if __name__ == "__main__":
  app.run(debug=True)
