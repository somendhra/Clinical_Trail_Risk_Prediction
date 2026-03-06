import joblib
import pandas as pd

# Load model
model = joblib.load("trial_risk_model.pkl")

# Load training data to get feature order
train_df = pd.read_csv("final_trial_risk_dataset.csv")
features = train_df.drop("Outcome", axis=1).columns.tolist()


print("=== Clinical Trial Risk Predictor ===")

# Basic inputs
phase = int(input("Enter Phase (1-4): "))
patients = int(input("Enter No. of Patients: "))
duration = int(input("Enter Duration (days): "))


# Age
print("\nAge Group:")
print("1. Young (18-35)")
print("2. Middle (36-55)")
print("3. Old (56+)")
age_choice = int(input("Choose (1/2/3): "))


# Region (Text Input)
print("\nEnter Region (India / USA / Europe / Asia / Other):")
region_text = input("Type here: ").lower().strip()


# Comorbidity
print("\nOther Disease (Comorbidity):")
print("1. None")
print("2. Diabetes")
print("3. Heart")
print("4. Lung")
print("5. BP (Hypertension)")
com_choice = int(input("Choose (1-5): "))


# Initialize all features to 0
input_data = {col: 0 for col in features}


# Fill main values
input_data["Phase"] = phase
input_data["Patients"] = patients
input_data["Duration"] = duration


# Age mapping
if age_choice == 1:
    input_data["AgeGroup_Young"] = 1
elif age_choice == 2:
    input_data["AgeGroup_Middle"] = 1
elif age_choice == 3:
    input_data["AgeGroup_Old"] = 1


# Region mapping (Text Based)
if "india" in region_text:
    input_data["Region_India"] = 1
elif "usa" in region_text or "united states" in region_text:
    input_data["Region_USA"] = 1
elif "europe" in region_text or "uk" in region_text or "france" in region_text:
    input_data["Region_Europe"] = 1
elif "asia" in region_text or "china" in region_text or "japan" in region_text:
    input_data["Region_Asia"] = 1
else:
    input_data["Region_Other"] = 1


# Comorbidity mapping
com_map = {
    1: "Comorbidity_None",
    2: "Comorbidity_Diabetes",
    3: "Comorbidity_Heart",
    4: "Comorbidity_Lung",
    5: "Comorbidity_BP"
}

if com_choice in com_map:
    input_data[com_map[com_choice]] = 1


# Create DataFrame in correct order
data = pd.DataFrame([input_data])[features]


# Predict
prob = model.predict_proba(data)[0][1]


print("\n===================================")
print("Completion Probability:", round(prob*100, 2), "%")

if prob > 0.7:
    print("Risk Level: LOW (Likely to Complete)")
elif prob > 0.4:
    print("Risk Level: MEDIUM")
else:
    print("Risk Level: HIGH (Likely to Stop)")
print("===================================")
