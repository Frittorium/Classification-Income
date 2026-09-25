import tkinter as tk
from tkinter import ttk, messagebox

from predict import predict

WORKCLASS_OPTIONS = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov",
                      "Local-gov", "State-gov", "Without-pay", "Never-worked", "Unknown"]
EDUCATION_OPTIONS = ["Below-HS", "HS-grad", "Some-college", "Associate",
                      "Bachelors", "Masters", "Advanced Degree"]
MARITAL_OPTIONS = ["Married-civ-spouse", "Divorced", "Never-married", "Separated",
                    "Widowed", "Married-spouse-absent", "Married-AF-spouse"]
OCCUPATION_OPTIONS = ["Tech-support", "Craft-repair", "Other-service", "Sales",
                      "Exec-managerial", "Prof-specialty", "Handlers-cleaners",
                      "Machine-op-inspct", "Adm-clerical", "Farming-fishing",
                      "Transport-moving", "Priv-house-serv", "Protective-serv",
                      "Armed-Forces", "Unknown"]
RELATIONSHIP_OPTIONS = ["Wife", "Own-child", "Husband", "Not-in-family",
                         "Other-relative", "Unmarried"]
RACE_OPTIONS = ["Amer-Indian-Eskimo", "Asian-Pac-Islander", "Black", "Other", "White"]
GENDER_OPTIONS = ["Female", "Male"]
COUNTRY_OPTIONS = ["United-States", "Mexico", "Philippines", "Germany", "Puerto-Rico",
                    "Canada", "India", "England", "China", "Cuba", "South", "Jamaica",
                    "Italy", "Dominican-Republic", "Vietnam", "Guatemala", "Japan",
                    "Poland", "Columbia", "Taiwan", "Haiti", "Iran", "Portugal",
                    "Nicaragua", "Peru", "Greece", "Ecuador", "France", "Ireland",
                    "Hong", "Thailand", "Cambodia", "Trinadad&Tobago", "Laos",
                    "Yugoslavia", "Outlying-US(Guam-USVI-etc)", "Honduras", "Scotland",
                    "El-Salvador", "Hungary", "Holand-Netherlands", "Unknown"]


def make_combo_row(label, options, row):
    tk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=4)
    var = tk.StringVar(value=options[0])
    combo = ttk.Combobox(root, textvariable=var, values=options, state="readonly", width=25)
    combo.grid(row=row, column=1, padx=8, pady=4)
    return var


def make_entry_row(label, row, default="0"):
    tk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=4)
    entry = tk.Entry(root, width=27)
    entry.insert(0, default)
    entry.grid(row=row, column=1, padx=8, pady=4)
    return entry


def on_predict():
    try:
        raw = {
            "age": float(age_entry.get()),
            "capital_gain": float(capital_gain_entry.get()),
            "capital_loss": float(capital_loss_entry.get()),
            "hours_per_week": float(hours_entry.get()),
            "workclass": workclass_var.get(),
            "education": education_var.get(),
            "marital_status": marital_var.get(),
            "occupation": occupation_var.get(),
            "relationship": relationship_var.get(),
            "race": race_var.get(),
            "gender": gender_var.get(),
            "native_country": country_var.get(),
        }
    except ValueError:
        messagebox.showerror("Invalid input", "Age, capital gain/loss, and hours must be numbers.")
        return

    prediction, probability = predict(raw)
    label = ">50K" if prediction == 1 else "<=50K"
    result_var.set(f"Prediction: {label}\nProbability of >50K: {probability:.2%}")


root = tk.Tk()
root.title("Income Predictor")

age_entry = make_entry_row("Age", 0, default="37")
capital_gain_entry = make_entry_row("Capital Gain", 1)
capital_loss_entry = make_entry_row("Capital Loss", 2)
hours_entry = make_entry_row("Hours per Week", 3, default="40")

workclass_var = make_combo_row("Workclass", WORKCLASS_OPTIONS, 4)
education_var = make_combo_row("Education", EDUCATION_OPTIONS, 5)
marital_var = make_combo_row("Marital Status", MARITAL_OPTIONS, 6)
occupation_var = make_combo_row("Occupation", OCCUPATION_OPTIONS, 7)
relationship_var = make_combo_row("Relationship", RELATIONSHIP_OPTIONS, 8)
race_var = make_combo_row("Race", RACE_OPTIONS, 9)
gender_var = make_combo_row("Gender", GENDER_OPTIONS, 10)
country_var = make_combo_row("Native Country", COUNTRY_OPTIONS, 11)

tk.Button(root, text="Predict", command=on_predict).grid(row=12, column=0, columnspan=2, pady=12)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Arial", 11), justify="left").grid(
    row=13, column=0, columnspan=2, pady=8
)

root.mainloop()