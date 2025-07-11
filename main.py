import os
import json
import pandas as pd
from file_api import get_file_data
from writer import write_to_csv
# from categorize import categorize_ui_component
from ui_detection import run_ui_detection
from encode import run_data_encoding
from div_detection import detect_div_and_add_page_width
from tree_predictor import build_frame_tree_json
from node_extractor import process_node_for_tree, extract_all_nodes
from categorize import run_ui_categorization

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_total_time(nodes, min_time=0.001):
    total = 0.0
    for node in nodes:
        time_taken = max(node.get("processing_time", 0.0), min_time)
        total += time_taken
        if "children" in node:
            total += calculate_total_time(node["children"], min_time)
    return total

def main():
    output_dir = "output"
    ensure_folder(output_dir)

    filekeys = input("Enter comma-separated Figma file keys: ").strip().split(',')
    all_nodes = []

    for file_id in filekeys:
        file_id = file_id.strip()
        print(f"[INFO] Processing file: {file_id}")
        file_data = get_file_data(file_id)

        if not file_data:
            print(f"[ERROR] Failed to fetch data for file: {file_id}")
            continue

        # Step A: Flatten nodes first (required before categorization)
        document = file_data.get("document", {})
        top_nodes = document.get("children", [])
        if not top_nodes:
            print(f"[WARN] No top-level nodes found in file {file_id}")
            continue

        for node in top_nodes:
            extract_all_nodes(node, all_nodes, file_id)

    # Step 1: Save flattened nodes
    step1_csv = os.path.join(output_dir, "step1-all_nodes_attributes.csv")
    write_to_csv(all_nodes, step1_csv)
    print(f"[INFO] Step 1 complete: {step1_csv}")

    # Step 2: Categorization
    # step2_csv = os.path.join(output_dir, "step2-Categorized_Components.csv")
    # df_categorized = run_ui_categorization(step1_csv, step2_csv)


    # print(f"[INFO] Step 2 complete: {step2_csv}")

    # # Build prediction_lookup from step2
    # prediction_lookup = dict(zip(df_categorized["id"], df_categorized["ui_component"]))

    # step3_csv = os.path.join(output_dir, "step3-attributes_regex_matchingpercent.csv")
    # df_detected = run_ui_detection(step2_csv, step3_csv)
    # print(f"[INFO] Step 3 complete: {step3_csv}")

    # step4_csv = os.path.join(output_dir, "step4-Encoded_Data.csv")
    # df_encoded, _ = run_data_encoding(step1_csv, step4_csv)
    # print(f"[INFO] Step 4 complete: {step4_csv}")

    step5_csv = os.path.join(output_dir, "step5-final_encoded_data.csv")
    df_final_encoded, _ = run_data_encoding(step1_csv, step5_csv)
    print(f"[INFO] Step 5 complete: {step5_csv}")

    step6_csv = os.path.join(output_dir, "step6-final_dataset.csv")
    df_final_dataset = detect_div_and_add_page_width(step5_csv, step6_csv)
    print(f"[INFO] Step 6 complete: {step6_csv}")

    # Step B: Build tree JSON using actual predictions
    for file_id in filekeys:
        file_id = file_id.strip()
        file_data = get_file_data(file_id)
        document = file_data.get("document", {})
        top_nodes = document.get("children", [])
        if not top_nodes:
            continue

        tree = []
        for node in top_nodes:
            tree.append(process_node_for_tree(node, file_id))

        total_time = calculate_total_time(tree)

        tree_json_path = os.path.join(output_dir, f"{file_id}_ui_tree_output.json")
        with open(tree_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "total_processing_time_sec": round(total_time, 4),
                "ui_tree": tree
            }, f, indent=4)

        print(f"[INFO] Tree JSON saved: {tree_json_path}")

    print(f"[SUCCESS] Pipeline finished. Final dataset is located at: {step6_csv}")

if __name__ == "__main__":
    main()
