import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputClassifier
import joblib

# Load and clean dataset
df = pd.read_csv("vitals_dataset.csv")
df.columns = df.columns.str.strip()

# Encode categorical columns
le_ecg = LabelEncoder()
df["ECG_Type_Encoded"] = le_ecg.fit_transform(df["ECG_Status"])

le_label = LabelEncoder()
le_disease = LabelEncoder()
le_cause = LabelEncoder()
le_symptoms = LabelEncoder()
le_solution = LabelEncoder()
le_treatment = LabelEncoder()

df["Label_Code"] = le_label.fit_transform(df["Label"])
df["Disease_Code"] = le_disease.fit_transform(df["Disease"])
df["Cause_Code"] = le_cause.fit_transform(df["Cause"])
df["Symptoms_Code"] = le_symptoms.fit_transform(df["Symptoms"])
df["Solution_Code"] = le_solution.fit_transform(df["Solution"])
df["Treatment_Code"] = le_treatment.fit_transform(df["Treatment"])

# Features and targets
X = df[["Temperature_F", "HeartRate", "SpO2", "ECG_Type_Encoded"]]
y = df[["Label_Code", "Disease_Code", "Cause_Code", "Symptoms_Code", "Solution_Code", "Treatment_Code"]]

# Train model using MultiOutputClassifier
base_model = LogisticRegression(max_iter=1000)
model = MultiOutputClassifier(base_model)
model.fit(X, y)

# Save encoders and model if needed
joblib.dump(model, "app\model\multioutput_model.pkl")
joblib.dump(le_ecg, "app\model\le_ecg.pkl")
joblib.dump(le_label, "app\model\le_label.pkl")
joblib.dump(le_disease, "app\model\le_disease.pkl")
joblib.dump(le_cause, "app\model\le_cause.pkl")
joblib.dump(le_symptoms, "app\model\le_symptoms.pkl")
joblib.dump(le_solution, "app\model\le_solution.pkl")
joblib.dump(le_treatment, "app\model\le_treatment.pkl")


# -------------------------
# Predict new input
# -------------------------
input_data = {
    "Temperature_F": 95,
    "HeartRate": 70,
    "SpO2": 97,
    "ECG_Status": "Normal"
}

encoded_ecg = le_ecg.transform([input_data["ECG_Status"]])[0]
new_data = pd.DataFrame([[input_data["Temperature_F"], input_data["HeartRate"], input_data["SpO2"], encoded_ecg]],
                        columns=["Temperature_F", "HeartRate", "SpO2", "ECG_Type_Encoded"])

predictions = model.predict(new_data)[0]

# Decode all predicted outputs
decoded_outputs = {
    "Label": le_label.inverse_transform([predictions[0]])[0],
    "Disease": le_disease.inverse_transform([predictions[1]])[0],
    "Cause": le_cause.inverse_transform([predictions[2]])[0],
    "Symptoms": le_symptoms.inverse_transform([predictions[3]])[0],
    "Solution": le_solution.inverse_transform([predictions[4]])[0],
    "Treatment": le_treatment.inverse_transform([predictions[5]])[0],
}

print("Predicted Results:")
for key, value in decoded_outputs.items():
    print(f"{key}: {value}")