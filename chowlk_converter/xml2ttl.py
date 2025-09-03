import requests
import json

# --- User parameters ---
xml_file_path = "docs/diagrams/agrixel.drawio.xml"  # Path to input XML diagram
ttl_save_path = "ontology/agrixel_temp.ttl"                   # Path to save TTL file

# API endpoint
url = "https://chowlk.linkeddata.es/api"

# --- Send XML via POST ---
with open(xml_file_path, 'rb') as f:
    files = {'data': f}
    response = requests.post(url, files=files)

# --- Parse JSON response ---
try:
    response_data = response.json()
except json.JSONDecodeError:
    print("Error: Response is not valid JSON")
    print(response.text)
    exit(1)

# --- Save TTL file ---
ttl_content = response_data.get("ttl_data")
if ttl_content:
    with open(ttl_save_path, 'w', encoding='utf-8') as f:
        f.write(ttl_content)
    print(f"TTL ontology saved to {ttl_save_path}")
else:
    print("No TTL data found in response.")

# --- Print new namespaces ---
new_ns = response_data.get("new_namespaces", {})
if new_ns:
    print("\nNew Namespaces:")
    for prefix, ns in new_ns.items():
        print(f"  {prefix}: {ns}")

# --- Print errors ---
errors = response_data.get("errors", {})
if errors:
    print("\nErrors:")
    for category, items in errors.items():
        print(f"  {category}:")
        for err in items:
            print(f"    Shape ID {err.get('shape_id')}: {err.get('message')} (Value: {err.get('value')})")

# --- Print warnings ---
warnings = response_data.get("warnings", {})
if warnings:
    print("\nWarnings:")
    for category, items in warnings.items():
        print(f"  {category}:")
        for warn in items:
            print(f"    Shape ID {warn.get('shape_id', 'N/A')}: {warn.get('message')} (Value: {warn.get('value')})")

# --- Save error XML if generated ---
if response_data.get("xml_error_generated") and response_data.get("xml_error_file"):
    error_xml_path = "error_highlighted.xml"
    with open(error_xml_path, 'w', encoding='utf-8') as f:
        f.write(response_data["xml_error_file"])
    print(f"\nError-highlighted XML saved to {error_xml_path}")
