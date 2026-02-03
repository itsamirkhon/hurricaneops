import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_auth_flow():
    print("1. Testing Unauthenticated Access...")
    # Try to resolve incident without token
    try:
        res = requests.post(f"{BASE_URL}/actions/incident/test-id/resolve")
        if res.status_code == 401:
            print("SUCCESS: Access denied as expected (401)")
        else:
            print(f"FAILURE: Expected 401, got {res.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")

    print("\n2. Testing Login...")
    try:
        payload = {"username": "admin", "password": "admin"}
        res = requests.post(f"{BASE_URL}/auth/token", data=payload)
        if res.status_code == 200:
            token_data = res.json()
            token = token_data["access_token"]
            print(f"SUCCESS: Logged in. Token: {token[:10]}...")
        else:
            print(f"FAILURE: Login failed. {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n3. Testing Authenticated Access...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # We need a valid action or at least hit the endpoint. 
        # Resolving a non-existent incident might 404, but NOT 401.
        # Let's try creating an incident which should be 200/201
        
        create_payload = {
            "description": "Auth Test Incident",
            "latitude": 10.0,
            "longitude": 10.0,
            "priority": "low"
        }
        res = requests.post(
            f"{BASE_URL}/actions/incident/create", 
            json=create_payload,
            headers=headers
        )
        
        if res.status_code == 200:
            print("SUCCESS: Action executed with token")
        else:
            print(f"FAILURE: Authenticated action failed. Status: {res.status_code}, Body: {res.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_auth_flow()
