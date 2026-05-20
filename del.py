# import requests

# API_KEY = "5f5c5fc0-1dba-4efc-bde5-7c5d5c2640cf"
# BASE_URL = "https://api.vapi.ai"
# HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# def wipe_history():
#     print("Fetching call history...")
#     # 1. List calls (fetches up to 100 per page by default)
#     response = requests.get(f"{BASE_URL}/call", headers=HEADERS)
    
#     if response.status_code != 200:
#         print(f"Error fetching calls: {response.text}")
#         return

#     calls = response.json()
    
#     if not calls:
#         print("No calls found to delete.")
#         return

#     print(f"Found {len(calls)} calls. Starting deletion...")

#     # 2. Iterate and delete each call
#     for call in calls:
#         call_id = call.get('id')
#         del_resp = requests.delete(f"{BASE_URL}/call/{call_id}", headers=HEADERS)
        
#         if del_resp.status_code == 200 or del_resp.status_code == 204:
#             print(f"Successfully deleted call: {call_id}")
#         else:
#             print(f"Failed to delete {call_id}: {del_resp.text}")

#     print("Wipe complete.")

# if __name__ == "__main__":
#     wipe_history()



import requests
import time

API_KEY = "5f5c5fc0-1dba-4efc-bde5-7c5d5c2640cf"
BASE_URL = "https://api.vapi.ai"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def wipe_history():
    print("Fetching call history...")
    response = requests.get(f"{BASE_URL}/call", headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching calls: {response.text}")
        return

    calls = response.json()
    
    if not calls:
        print("No calls found to delete.")
        return

    print(f"Found {len(calls)} calls. Starting deletion...")

    for call in calls:
        call_id = call.get('id')
        del_resp = requests.delete(
            f"{BASE_URL}/call/{call_id}", 
            headers=HEADERS
        )
        
        if del_resp.status_code in [200, 204]:
            print(f"Successfully deleted call: {call_id}")
        elif del_resp.status_code == 429:
            print(f"Rate limited. Waiting 5 seconds...")
            time.sleep(5)
            # Retry once after waiting
            del_resp = requests.delete(
                f"{BASE_URL}/call/{call_id}", 
                headers=HEADERS
            )
            if del_resp.status_code in [200, 204]:
                print(f"Successfully deleted call: {call_id}")
            else:
                print(f"Failed after retry {call_id}: {del_resp.text}")
        else:
            print(f"Failed to delete {call_id}: {del_resp.text}")
        
        # Wait between each request to avoid rate limiting
        time.sleep(0.5)

    print("Wipe complete.")

if __name__ == "__main__":
    wipe_history()