import csv
from constants import REQUIRED_FIELDS

def write_to_csv(data, output_file):
    if not data:
        print("[INFO] No data to write.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        for row in data:
            writer.writerow({key: row.get(key, "") for key in REQUIRED_FIELDS})

    print(f"[INFO] Wrote {len(data)} nodes to {output_file}")
