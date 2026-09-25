import joblib
from pathlib import Path
import pandas as pd


# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
SCALER_DIR = BASE_DIR / "scalers"
ENCODER_DIR = BASE_DIR / "encoders"


# Load model, scaler, encoders, and feature order
MODEL_PATH = MODEL_DIR / "gradient_boosting_model.joblib"
SCALER_PATH = SCALER_DIR / "scaler.joblib"
ENCODERS_PATH = ENCODER_DIR / "encoders.joblib"
FEATURE_ORDER_PATH = ENCODER_DIR / "feature_order.joblib"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoders = joblib.load(ENCODERS_PATH)
FEATURE_ORDER = joblib.load(FEATURE_ORDER_PATH)


RACE_CATEGORIES = [
    "Amer-Indian-Eskimo",
    "Asian-Pac-Islander",
    "Black",
    "Other",
    "White",
]

GENDER_CATEGORIES = [
    "Female",
    "Male",
]


def _encode_row(raw):

    row = {
        "age": raw["age"],
        "capital-gain": raw["capital_gain"],
        "capital-loss": raw["capital_loss"],
        "hours-per-week": raw["hours_per_week"],
    }

    workclass_enc = encoders["workclass"].transform(
        pd.DataFrame({"workclass": [raw["workclass"]]})
    )
    row.update(workclass_enc.iloc[0].to_dict())

    edu_enc = encoders["education_ordinal"].transform(
        pd.DataFrame({"education": [raw["education"]]})
    )
    row["Edu-Encoded"] = edu_enc[0][0]

    marital_enc = encoders["marital_status"].transform(
        pd.DataFrame({"marital-status": [raw["marital_status"]]})
    )
    row.update(marital_enc.iloc[0].to_dict())

    occupation_enc = encoders["occupation"].transform(
        pd.DataFrame({"occupation": [raw["occupation"]]})
    )
    row.update(occupation_enc.iloc[0].to_dict())

    relationship_enc = encoders["relationship"].transform(
        pd.DataFrame({"relationship": [raw["relationship"]]})
    )
    row.update(relationship_enc.iloc[0].to_dict())

    for cat in RACE_CATEGORIES:
        row[f"race_{cat}"] = 1 if raw["race"] == cat else 0

    for cat in GENDER_CATEGORIES:
        row[f"gender_{cat}"] = 1 if raw["gender"] == cat else 0

    country_enc = encoders["native_country"].transform(
        pd.DataFrame({"native-country": [raw["native_country"]]})
    )
    row.update(country_enc.iloc[0].to_dict())

    row_df = pd.DataFrame([row]).reindex(
        columns=FEATURE_ORDER,
        fill_value=0
    )

    return row_df


def predict(raw):
    """
    raw: dict with keys age, capital_gain, capital_loss, hours_per_week
    (numbers) and workclass, education, marital_status, occupation,
    relationship, race, gender, native_country
    (raw category strings matching the values used at training time).

    Returns:
        (prediction, probability_over_50k)
    """

    row_df = _encode_row(raw)

    scaled = scaler.transform(row_df)

    prediction = model.predict(scaled)[0]

    probability = model.predict_proba(scaled)[0][1]

    return int(prediction), float(probability)


if __name__ == "__main__":

    sample = {
        "age": 37,
        "capital_gain": 0,
        "capital_loss": 0,
        "hours_per_week": 40,
        "workclass": "Private",
        "education": "Bachelors",
        "marital_status": "Never-married",
        "occupation": "Prof-specialty",
        "relationship": "Not-in-family",
        "race": "White",
        "gender": "Male",
        "native_country": "United-States",
    }

    pred, prob = predict(sample)

    print(
        "Prediction:",
        ">50K" if pred == 1 else "<=50K",
        f"({prob:.2%})"
    )