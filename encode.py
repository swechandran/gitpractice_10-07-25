import pandas as pd
from sklearn.preprocessing import LabelEncoder

def run_data_encoding(input_csv: str, output_csv: str, id_columns=None):
    """
    - Loads the CSV
    - Converts booleans to integers (True → 1, False → 0)
    - Fills missing values
    - One-hot encodes 'Type' column (type_FRAME, type_RECTANGLE, etc.)
    - Label-encodes categorical columns (except IDs)
    - Saves processed data
    """
    if id_columns is None:
        id_columns = ['id', 'name', 'filekey', 'ui_component']

    df = pd.read_csv(input_csv)

    # Step 1: Convert boolean values to integers
    df = df.applymap(lambda x: 1 if x is True else (0 if x is False else x))

    # Step 2: Fill missing values
    for col in df.columns:
        if df[col].dtype == 'object' and col not in id_columns:
            df[col] = df[col].fillna("unknown")
        elif df[col].dtype != 'object':
            df[col] = df[col].fillna(0)

    # Step 3: One-hot encode the 'Type' column (creates type_FRAME, type_RECTANGLE, etc.)
    if 'Type' in df.columns:
        type_dummies = pd.get_dummies(df['Type'], prefix='type')
        df = pd.concat([df.drop(columns=['Type']), type_dummies], axis=1)

    # Step 4: Label encode other categorical columns (excluding ID columns and new type_* columns)
    categorical_cols = [
        col for col in df.select_dtypes(include='object').columns 
        if col not in id_columns
    ]

    label_encoders = {}
    for col in categorical_cols:
        df[col] = df[col].astype(str)
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Step 5: Report identifier columns
    print("[Encoding] Checking identifier columns:")
    for col in id_columns:
        print(f"  {col}: {'Present' if col in df.columns else 'Missing'}")

    # Step 6: Save output
    df.to_csv(output_csv, index=False)
    print(f"[Encoding] Processed data saved to '{output_csv}'")

    return df, label_encoders
