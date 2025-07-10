import pandas as pd

def is_div(row):
    known_ui = ["textbox", "button", "checkbox", "radiobutton", "fileupload", "dropdown"]
    name_text = str(row.get("name", "")).lower()

    if any(keyword in name_text for keyword in known_ui):
        return "no"
    
    return "yes" if (
        row.get("type_FRAME", False)
        or row.get("type_GROUP", False)
        or row.get("layoutMode_HORIZONTAL", False)
        or row.get("layoutMode_VERTICAL", False)
        or row.get("layoutWrap_NO_WRAP", False)
        or row.get("clipsContent", False)
        or row.get("itemSpacing", 0) > 0
        or row.get("paddingTop", 0) > 0
        or row.get("paddingBottom", 0) > 0
        or row.get("paddingLeft", 0) > 0
        or row.get("paddingRight", 0) > 0
    ) else "no"


def detect_div_and_add_page_width(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # Detect div
    df["div"] = df.apply(is_div, axis=1)

    # Update ui_component if div detected
    df["ui_component"] = df.apply(
        lambda row: "div" if row["div"] == "yes" else row["ui_component"],
        axis=1
    )

    # Drop helper column
    df.drop(columns=["div"], inplace=True)

    # Calculate page_width from parent_id
    df["parent_id"] = df["parent_id"].astype(str).str.strip()
    parent_widths = df.groupby("parent_id")["absoluteBoundingBox_width"].first().to_dict()
    df["page_width"] = df["parent_id"].map(parent_widths)

    # Save final output
    df.to_csv(output_path, index=False)
    print(f"[Div + Page Width] Output saved to '{output_path}'")

    return df
