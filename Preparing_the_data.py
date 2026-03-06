import pandas as pd

# ===============================
# LOAD DATASET
# ===============================
df = pd.read_csv("Covid-19_cleaned_dataset.csv")



# ===============================
# SELECT IMPORTANT COLUMNS
# ===============================
df = df[[
    "Phases",
    "Enrollment",
    "Status",
    "Age",
    "Conditions",
    "Locations",
    "Start Date",
    "Completion Date"
]]

# Rename for simplicity
df.columns = [
    "Phase",
    "Patients",
    "Status",
    "Age",
    "Conditions",
    "Location",
    "Start",
    "End"
]

# Remove missing values
df = df.dropna()


# ===============================
# PHASE (TEXT → NUMBER)
# ===============================
df["Phase"] = df["Phase"].str.extract("(\d)").astype(float)


# ===============================
# OUTCOME (STATUS → SUCCESS/FAIL)
# ===============================
df["Outcome"] = df["Status"].map({
    "Completed": 1,
    "Terminated": 0,
    "Withdrawn": 0,
    "Suspended": 0
})

# Remove running/unknown trials
df = df.dropna(subset=["Outcome"])


# ===============================
# DATE → DURATION
# ===============================
df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
df["End"] = pd.to_datetime(df["End"], errors="coerce")

df = df.dropna()

df["Duration"] = (df["End"] - df["Start"]).dt.days
df = df[df["Duration"] > 0]


# ===============================
# AGE GROUP
# ===============================
def get_age_group(text):
    t = str(text).lower()

    if "child" in t or "young" in t:
        return "Young"
    elif "adult" in t and "older" not in t:
        return "Middle"
    elif "older" in t or "senior" in t:
        return "Old"
    else:
        return "Middle"


df["AgeGroup"] = df["Age"].apply(get_age_group)


# ===============================
# REGION (FROM LOCATION)
# ===============================
def get_region(loc):
    t = str(loc).lower()

    if "india" in t:
        return "India"
    elif "usa" in t or "united states" in t:
        return "USA"
    elif "uk" in t or "france" in t or "germany" in t:
        return "Europe"
    elif "china" in t or "japan" in t:
        return "Asia"
    else:
        return "Other"


df["Region"] = df["Location"].apply(get_region)


# ===============================
# COMORBIDITY (FROM CONDITIONS)
# ===============================
def get_comorbidity(cond):
    t = str(cond).lower()

    if "diabetes" in t:
        return "Diabetes"
    elif "heart" in t or "cardio" in t:
        return "Heart"
    elif "lung" in t or "asthma" in t:
        return "Lung"
    elif "hypertension" in t:
        return "BP"
    else:
        return "None"


df["Comorbidity"] = df["Conditions"].apply(get_comorbidity)


# ===============================
# ONE-HOT ENCODING
# ===============================
df = pd.get_dummies(
    df,
    columns=["AgeGroup", "Region", "Comorbidity"]
)


# ===============================
# FINAL FEATURE SELECTION
# ===============================
cols = ["Phase", "Patients", "Duration", "Outcome"]

for c in df.columns:
    if (
        c.startswith("AgeGroup_")
        or c.startswith("Region_")
        or c.startswith("Comorbidity_")
    ):
        cols.append(c)

df = df[cols]


# ===============================
# SAVE FINAL DATASET
# ===============================
df.to_csv("final_trial_risk_dataset.csv", index=False)


# ===============================
# SUMMARY
# ===============================
print("===================================")
print(" FINAL DATASET CREATED SUCCESSFULLY")
print("===================================")
print("Rows:", len(df))
print("Columns:", list(df.columns))
print("Saved as: final_trial_risk_dataset.csv")
