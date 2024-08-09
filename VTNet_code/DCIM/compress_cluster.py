import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Disable SSL warnings (due to verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Elasticsearch server URL
es_url = "https://10.254.139.167:9200"

# Authentication credentials
username = "elastic"       # Replace with your username
password = "Vtlog!@2021"   # Replace with your password

# Headers for requests
headers = {"Content-Type": "application/json"}

def get_all_indices(session):
    """Fetch the list of all indices in the cluster."""
    try:
        response = session.get(f"{es_url}/_cat/indices?h=index")
        response.raise_for_status()
        indices = response.text.strip().split("\n")
        return indices
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve indices. Error: {e}")
        return []

def close_index(session, index):
    """Close an index."""
    try:
        response = session.post(f"{es_url}/{index}/_close")
        response.raise_for_status()
        if "acknowledged" in response.json() and response.json()["acknowledged"]:
            print(f"Index '{index}' closed successfully.")
        else:
            print(f"Failed to close index '{index}'. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error closing index '{index}': {e}")

def update_index_settings(session, index):
    """Update index settings to use best_compression."""
    settings = {
        "index": {
            "codec": "best_compression"
        }
    }
    try:
        response = session.put(f"{es_url}/{index}/_settings", headers=headers, json=settings)
        response.raise_for_status()
        if "acknowledged" in response.json() and response.json()["acknowledged"]:
            print(f"Settings for index '{index}' updated successfully.")
        else:
            print(f"Failed to update settings for index '{index}'. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating settings for index '{index}': {e}")

def open_index(session, index):
    """Open an index."""
    try:
        response = session.post(f"{es_url}/{index}/_open")
        response.raise_for_status()
        if "acknowledged" in response.json() and response.json()["acknowledged"]:
            print(f"Index '{index}' opened successfully.")
        else:
            print(f"Failed to open index '{index}'. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error opening index '{index}': {e}")

def force_merge_index(session, index):
    """Force merge an index to apply compression."""
    try:
        response = session.post(f"{es_url}/{index}/_forcemerge?max_num_segments=1")
        response.raise_for_status()
        print(f"Index '{index}' force merged successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error force merging index '{index}': {e}")

def compress_indices():
    """Compress all indices in the Elasticsearch cluster."""
    # Create a session with authentication and SSL settings
    with requests.Session() as session:
        session.auth = HTTPBasicAuth(username, password)
        session.verify = False  # Disable SSL verification (not recommended for production)
        
        indices = get_all_indices(session)
        if not indices:
            print("No indices found. Exiting.")
            return
        
        print(f"Found {len(indices)} indices to process.\n")
        
        for index in indices:
            print(f"Processing index: '{index}'")
            close_index(session, index)
            update_index_settings(session, index)
            open_index(session, index)
            force_merge_index(session, index)
            print(f"Compression workflow for index '{index}' completed.\n")

if __name__ == "__main__":
    compress_indices()
