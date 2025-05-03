import json

def search_json(data, target):
    """Recursively search for a text in a nested JSON-like object"""
    if isinstance(data, dict):
        for key, value in data.items():
            if target in str(key) or target in str(value):
                print(f"Found in key: {key} -> {value}")
            search_json(value, target)
    elif isinstance(data, list):
        for item in data:
            search_json(item, target)

# Load JSON
with open('debug_streetwear.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Search for text
search_text = "webapp.video-detail"  # change this to whatever you're looking for
search_json(json_data, search_text)

