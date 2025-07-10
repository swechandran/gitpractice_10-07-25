import pandas as pd

def categorize_ui_component(row):
    name = str(row.get('name', '')).lower()
    width = row.get('absoluteBoundingBox_width', 0)
    height = row.get('absoluteBoundingBox_height', 0)

    # Type flags (fallback to 0 if missing)
    is_frame = bool(row.get('type_FRAME', 0))
    is_group = bool(row.get('type_GROUP', 0))
    is_vector = bool(row.get('type_VECTOR', 0))
    is_component = bool(row.get('type_COMPONENT', 0))
    is_rectangle = bool(row.get('type_RECTANGLE', 0))
    is_text = bool(row.get('type_RECTANGLE', 0))
    stroke_weight = row.get('strokeWeight', 0)

    # Corner radius handling
    radius_raw = row.get('rectangleCornerRadii', 0)
    corner_radius = max(radius_raw) if isinstance(radius_raw, list) and radius_raw else radius_raw

    # Layout directions
    layout_horizontal = bool(row.get('layoutMode_HORIZONTAL', 0))
    layout_vertical = bool(row.get('layoutMode_VERTICAL', 0))

    # ----- UI Type Classification -----

    if any(k in name for k in ['image', 'img', 'logo', 'icon', 'photo', 'picture', 'mcu-logo', 'user', 'comment']) or \
       (is_vector and height > 10 and width > 10 and abs(height - width) <= max(height, width) * 0.3):
        return 'image'

    if any(k in name for k in ['checkbox', 'check', 'tick', 'select', 'option', 'choice']) or \
       ((is_frame or is_group or is_vector or is_rectangle) and
        10 <= height <= 30 and 10 <= width <= 30 and
        (corner_radius <= 2 or corner_radius >= height / 2 - 2)):
        return 'checkbox'

    if any(k in name for k in ['radio', 'option', 'circle', 'round', 'select']) or \
       ((is_frame or is_group or is_vector or is_rectangle) and
        10 <= height <= 30 and 10 <= width <= 30 and
        corner_radius >= height / 2 - 2):
        return 'radio button'

    if any(k in name for k in ['button', 'btn', 'cta', 'action', 'pagination', 'angle-']) or \
       ((is_frame or is_component or is_rectangle) and
        20 <= height <= 100 and 50 <= width <= 400 and
        (corner_radius > 0 or stroke_weight > 0)):
        return 'button'

    if any(k in name for k in ['textbox', 'input', 'field', 'textfield', 'search']) or \
       ((is_frame or is_rectangle) and
        20 <= height <= 60 and 80 <= width <= 500 and
        stroke_weight > 0):
        return 'textbox'

    if any(k in name for k in ['dropdown', 'select', 'menu', 'combobox', 'vendor']) or \
       ((is_frame or is_rectangle) and
        30 <= height <= 300 and 100 <= width <= 400 and
        layout_vertical):
        return 'dropdown'

    if any(k in name for k in ['date', 'calendar', 'picker']):
        return 'date picker'

    if any(k in name for k in ['upload', 'file', 'attach', 'clip', 'path']) or \
       ((is_frame or is_rectangle) and
        40 <= height <= 150 and 150 <= width <= 600 and
        layout_horizontal):
        return 'file upload'

    if ((is_frame or name.startswith('frame')) and width > 200 and height > 100):
        return 'div'

    if (is_frame or name.startswith('frame')) and 20 <= height <= 80 and 100 <= width <= 500:
        return 'textbox'

    if width <= 20 and height <= 20:
        return 'icon'

    if height >= 20 and width >= 50:
        return 'textbox'

    return 'other'


def run_ui_categorization(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)

    # Replace True/False with 1/0
    df = df.replace({True: 1, False: 0})

    # Required and optional columns
    required_cols = ['name', 'absoluteBoundingBox_width', 'absoluteBoundingBox_height']
    optional_cols = ['type_FRAME']

    missing_required = [col for col in required_cols if col not in df.columns]
    missing_optional = [col for col in optional_cols if col not in df.columns]

    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")
    if missing_optional:
        print(f"[Warning] Optional column(s) missing: {missing_optional}")

    df['ui_component'] = df.apply(categorize_ui_component, axis=1)
    df.to_csv(output_csv_path, index=False)
    return df

# import pandas as pd

# def categorize_ui_component(row):
#     name = str(row.get('name', '')).lower()
#     width = row.get('absoluteBoundingBox_width', 0)
#     height = row.get('absoluteBoundingBox_height', 0)
    
#     # ✅ Handle both boolean and integer values for type checks
#     is_frame = bool(row.get('type_FRAME', 0))
#     is_group = bool(row.get('type_GROUP', 0))
#     is_vector = bool(row.get('type_VECTOR', 0))
#     is_component = bool(row.get('type_COMPONENT', 0))
#     is_rectangle = bool(row.get('type_RECTANGLE', 0))
    
#     stroke_weight = row.get('strokeWeight', 0)
    
#     #  Handle corner radius - could be array or single value
#     corner_radius_raw = row.get('rectangleCornerRadii', 0)
#     if isinstance(corner_radius_raw, list):
#         corner_radius = max(corner_radius_raw) if corner_radius_raw else 0
#     else:
#         corner_radius = corner_radius_raw
    
#     #  Handle both boolean and integer values for layout modes
#     layout_mode_horizontal = bool(row.get('layoutMode_HORIZONTAL', 0))
#     layout_mode_vertical = bool(row.get('layoutMode_VERTICAL', 0))
    
#     item_spacing = row.get('itemSpacing', 0)

#     # Debug print to see what values we're getting
#     print(f"[DEBUG] Processing: {name[:20]}, width={width}, height={height}, is_frame={is_frame}, corner_radius={corner_radius}")

#     # ----- IMAGE ----- (First because it's least likely to conflict)
#     image_keywords = ['image', 'img', 'logo', 'icon', 'photo', 'picture', 'mcu-logo', 'user', 'comment']
#     if (any(x in name for x in image_keywords) or
#         (is_vector and height > 10 and width > 10 and abs(height - width) <= max(height, width)*0.3)):
#         print(f"[DEBUG] → IMAGE")
#         return 'image'

#     # ----- CHECKBOX ----- (Early as they're small distinct elements)
#     checkbox_keywords = ['checkbox', 'check', 'tick', 'select', 'option', 'choice']
#     if (any(x in name for x in checkbox_keywords) or
#         ((is_frame or is_group or is_vector or is_rectangle) and 
#          10 <= height <= 30 and 
#          10 <= width <= 30 and 
#          (corner_radius <= 2 or corner_radius >= height/2-2))):
#         print(f"[DEBUG] → CHECKBOX")
#         return 'checkbox'

#     # ----- RADIO BUTTON -----
#     radio_keywords = ['radio', 'option', 'circle', 'round', 'select']
#     if (any(x in name for x in radio_keywords) or
#         ((is_frame or is_group or is_vector or is_rectangle) and 
#          10 <= height <= 30 and 
#          10 <= width <= 30 and 
#          corner_radius >= height/2-2)):
#         print(f"[DEBUG] → RADIO BUTTON")
#         return 'radio button'

#     # ----- BUTTON -----
#     button_keywords = ['button', 'btn', 'cta', 'action', 'pagination', 'angle-']
#     if (any(x in name for x in button_keywords) or
#         ((is_frame or is_component or is_rectangle) and 
#          20 <= height <= 100 and 
#          50 <= width <= 400 and 
#          (corner_radius > 0 or stroke_weight > 0))):
#         print(f"[DEBUG] → BUTTON")
#         return 'button'

#     # ----- TEXTBOX -----
#     textbox_keywords = ['textbox', 'input', 'field', 'textfield', 'search']
#     if (any(x in name for x in textbox_keywords) or
#         ((is_frame or is_rectangle) and 20 <= height <= 60 and 80 <= width <= 500 and stroke_weight > 0)):
#         print(f"[DEBUG] → TEXTBOX")
#         return 'textbox'

#     # ----- DROPDOWN -----
#     dropdown_keywords = ['dropdown', 'select', 'menu', 'combobox', 'vendor']
#     if (any(x in name for x in dropdown_keywords) or
#         ((is_frame or is_rectangle) and 30 <= height <= 300 and 100 <= width <= 400 and layout_mode_vertical)):
#         print(f"[DEBUG] → DROPDOWN")
#         return 'dropdown'

#     # ----- DATE PICKER -----
#     datepicker_keywords = ['date', 'calendar', 'picker']
#     if any(x in name for x in datepicker_keywords):
#         print(f"[DEBUG] → DATE PICKER")
#         return 'date picker'

#     # ----- FILE UPLOAD -----
#     fileupload_keywords = ['upload', 'file', 'attach', 'clip', 'path']
#     if (any(x in name for x in fileupload_keywords) or
#         ((is_frame or is_rectangle) and 40 <= height <= 150 and 150 <= width <= 600 and layout_mode_horizontal)):
#         print(f"[DEBUG] → FILE UPLOAD")
#         return 'file upload'

#     # ----- CONTAINER/LAYOUT ELEMENTS -----
#     # Large frames that likely contain other elements
#     if ((is_frame or name.startswith('frame')) and width > 200 and height > 100):
#         print(f"[DEBUG] → DIV")
#         return 'div'
    
#     # ----- SEPARATOR/LINE -----
#     # if (height <= 2 and width > 50) or 'line' in name:
#     #     print(f"[DEBUG] → SEPARATOR")
#     #     return 'separator'
    
#     # ----- SMALL FRAMES (likely interactive elements) -----
#     # Small to medium frames that might be input fields or buttons
#     if ((is_frame or name.startswith('frame')) and 
#         20 <= height <= 80 and 100 <= width <= 500):
#         print(f"[DEBUG] → TEXTBOX (frame-based)")
#         return 'textbox'
    
#     # ----- VERY SMALL ELEMENTS -----
#     # Very small elements (likely icons or indicators)
#     if width <= 20 and height <= 20:
#         print(f"[DEBUG] → ICON")
#         return 'icon'
    
#     # ----- DEFAULT TO TEXTBOX -----
#     # Most remaining elements should be textbox (input fields, content areas)
#     if height >= 20 and width >= 50:
#         print(f"[DEBUG] → TEXTBOX (default)")
#         return 'textbox'
    
#     # Final fallback for very small or unusual elements
#     print(f"[DEBUG] → OTHER")
#     return 'other'

# def run_ui_categorization(input_csv_path, output_csv_path):
#     df = pd.read_csv(input_csv_path)
    
#     #  Convert boolean values to integers BEFORE categorization
#     df = df.applymap(lambda x: 1 if x is True else (0 if x is False else x))
    
#     print(f"[Categorization] Processing {len(df)} rows...")
#     print(f"[Categorization] Available columns: {list(df.columns)}")
    
#     # Check if we have the required columns
#     required_cols = ['name', 'absoluteBoundingBox_width', 'absoluteBoundingBox_height', 'type_FRAME']
#     missing_cols = [col for col in required_cols if col not in df.columns]
#     if missing_cols:
#         print(f"[WARNING] Missing columns: {missing_cols}")
    
#     df['ui_component'] = df.apply(categorize_ui_component, axis=1)
    
#     # Show categorization results
#     print("[Categorization] Results:")
#     print(df['ui_component'].value_counts())
    
#     df.to_csv(output_csv_path, index=False)
#     print(f"[Categorization] Written to {output_csv_path}")
#     return df