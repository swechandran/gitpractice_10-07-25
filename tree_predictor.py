import pandas as pd
import json
from node_extractor import process_node_for_tree  

def build_frame_tree_json(file_data, output_json_file="ui_tree_output.json"):
    document = file_data.get("document", {})
    top_nodes = document.get("children", [])
    tree = []

    for node in top_nodes:
        tree.append(process_node_for_tree(node, file_id="demo"))

    # Recursive function to sum processing_time from root to all descendants
    def sum_processing_time(nodes):
        total = 0.0
        for node in nodes:
            total += node.get("processing_time", 0.0)
            total += sum_processing_time(node.get("children", []))
        return total

    total_processing_time = sum_processing_time(tree)

    output = {
        "total_processing_time_sec": round(total_processing_time, 4),
        "ui_tree": tree
    }

    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
