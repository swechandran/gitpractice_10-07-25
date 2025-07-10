import time
from constants import ALLOWED_TYPES
from flatten.frame_processor import FrameProcessor
from flatten.rectangle_processor import RectangleProcessor
from flatten.group_processor import GroupProcessor
from flatten.ellipse_processor import EllipseProcessor
from flatten.component_processor import ComponentProcessor
from flatten.boolean_processor import BooleanProcessor

# Map node type to the appropriate processor
def process_node_by_type(node_type, node, file_id, parent_id):
    node_type = node_type.upper()
    if node_type == "FRAME":
        return FrameProcessor(node, file_id, parent_id).preprocess()
    elif node_type == "RECTANGLE":
        return RectangleProcessor(node, file_id, parent_id).preprocess()
    elif node_type == "GROUP":
        return GroupProcessor(node, file_id, parent_id).preprocess()
    elif node_type == "ELLIPSE":
        return EllipseProcessor(node, file_id, parent_id).preprocess()
    elif node_type == "COMPONENT":
        return ComponentProcessor(node, file_id, parent_id).preprocess()
    elif node_type == "BOOLEAN_OPERATION":
        return BooleanProcessor(node, file_id, parent_id).preprocess()
    else:
        return None

#  Step 1: Flatten all nodes into a CSV-structured list
def extract_all_nodes(node, node_list, file_id, parent_id=None):
    if node is None:
        return
    node_type = node.get("type", "")
    if node_type in ALLOWED_TYPES:
        flat_node = process_node_by_type(node_type, node, file_id, parent_id)
        if flat_node:
            node_list.append(flat_node)
    for child in node.get("children", []):
        extract_all_nodes(child, node_list, file_id, parent_id=node.get("id"))

#  Step 2: Build tree with processing time and real predictions
def process_node_for_tree(node, file_id, parent_id=None, prediction_lookup=None):
    node_id = node.get("id", "")
    node_type = node.get("type", "").upper()
    name = node.get("name", "")
    children_output = []

    # Time how long it takes to process this node and its children
    start_time = time.time()

    for child in node.get("children", []):
        children_output.append(
            process_node_for_tree(child, file_id, parent_id=node_id, prediction_lookup=prediction_lookup)
        )

    end_time = time.time()
    process_time = end_time - start_time

    # Use the prediction from the lookup table if available
    prediction = "unknown"  # default
    if prediction_lookup is not None and node_id in prediction_lookup:
        prediction = prediction_lookup[node_id]
    elif node_type in ALLOWED_TYPES:
        prediction = "div"

    return {
        "name": name,
        "prediction": prediction,
        "processing_time": round(process_time, 4),
        "children": children_output
    }
