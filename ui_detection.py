import pandas as pd
import re
from Levenshtein import ratio

# Component patterns for regex-based detection
component_patterns = {
    "Button": [r"\b(Button|btn|submit|click)\b", r"^btn.*", r".*Button$"],
    "Textbox": [r"\b(Textbox|Input|text|field)\b", r"^txt.*", r".*text.*"],
    "Checkbox": [r"\b(Checkbox|chk|check box|Checkout)\b", r".*check.*box.*", r"^chk.*"],
    "RadioButton": [r"\b(Radio|option|RadioButton|StatusValues)\b", r".*radio.*", r".*radio button.*"],
    "FileUpload": [r"\b(File|Upload|browse|Disclosures)\b", r".*file.*upload.*"],
    "Dropdown": [r"\b(Dropdown|Select|Combo|DDL|ComboBox)\b", r".*dropdown.*", r".*select.*"]
}

def detect_ui(name):
    for ui_type, patterns in component_patterns.items():
        for pattern in patterns:
            if re.search(pattern, str(name), re.IGNORECASE):
                return ui_type
    return "Unmatched"

def get_match_percent(row):
    if row["detected_ui"] == "Unmatched":
        return 0.0
    return round(ratio(str(row["name"]).lower(), str(row["detected_ui"]).lower()), 2)

def run_ui_detection(input_csv: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    df["detected_ui"] = df["name"].apply(detect_ui)
    df["matching_percent"] = df.apply(get_match_percent, axis=1)
    df.to_csv(output_csv, index=False)
    print(f"[UI Detection] Processed data written to {output_csv}")
    return df  
