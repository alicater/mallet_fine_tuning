# colab notebook cleaning script to get the metadata to render properly for github

import json

INPUT_FILE = "Mallet_Fine_Tuning.ipynb"
OUTPUT_FILE = "Mallet_Fine_Tuning.ipynb"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    nb = json.load(f)

# delete broken notebook widget metadata
if "widgets" in nb.get("metadata", {}):
    del nb["metadata"]["widgets"]
    print("Cleaned notebook-level metadata.")

# delete specific cell-level progress bar widgets (keeps text/logs)
for cell in nb.get("cells", []):
    if "outputs" in cell:
        clean_outputs = []
        for out in cell["outputs"]:
            # If it's a widget, skip it. Otherwise, keep it.
            if out.get("output_type") == "display_data" and "application/vnd.jupyter.widget-view+json" in out.get("data", {}):
                continue 
            clean_outputs.append(out)
        cell["outputs"] = clean_outputs

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print(f" Success! {OUTPUT_FILE} is ready")