"""
Sample SDK usage for Deep Work Session Tracker

Generate the SDK first:
  npx @openapitools/openapi-generator-cli generate \
    -i http://localhost:8000/openapi.json \
    -g python \
    -o deepwork_sdk

Then install it:
  cd deepwork_sdk && pip install .

Run this script to see the SDK in action.
"""

import time

# After generating the SDK, uncomment the imports below:
# from deepwork_sdk import ApiClient, Configuration
# from deepwork_sdk.api import DefaultApi
# from deepwork_sdk.models import SessionCreate, PauseRequest

def main():
    # SDK usage example (uncomment after generating)
    """
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(config)
    api = DefaultApi(client)
    
    # Create a session
    print("Creating session...")
    session = api.create_session_sessions_post(
        SessionCreate(
            title="SDK Test Session",
            goal="Test the generated Python SDK",
            duration_minutes=25
        )
    )
    print(f"Created: {session.title} (id={session.id})")
    
    # Start the session
    print("Starting session...")
    session = api.start_session_sessions_session_id_start_patch(session.id)
    print(f"Status: {session.status}")
    
    # Simulate some work
    time.sleep(2)
    
    # Pause with reason
    print("Pausing...")
    session = api.pause_session_sessions_session_id_pause_patch(
        session.id,
        PauseRequest(reason="Coffee break")
    )
    print(f"Paused. Count: {session.pause_count}")
    
    time.sleep(1)
    
    # Resume
    print("Resuming...")
    session = api.resume_session_sessions_session_id_resume_patch(session.id)
    print(f"Status: {session.status}")
    
    # Complete
    print("Completing...")
    session = api.complete_session_sessions_session_id_complete_patch(session.id)
    print(f"Final status: {session.status}")
    
    # Check history
    print("\nSession history:")
    for s in api.get_history_sessions_history_get():
        print(f"  - {s.title}: {s.status}")
    """
    
    # For now, use requests directly to demonstrate the API
    import requests
    
    BASE = "http://localhost:8000"
    
    print("=== Deep Work Session Tracker - API Demo ===\n")
    
    # Create
    print("1. Creating session...")
    resp = requests.post(f"{BASE}/sessions/", json={
        "title": "SDK Demo Session",
        "goal": "Demonstrate the API workflow",
        "duration_minutes": 25
    })
    session = resp.json()
    sid = session["id"]
    print(f"   Created: {session['title']} (id={sid})")
    
    # Start
    print("2. Starting session...")
    resp = requests.patch(f"{BASE}/sessions/{sid}/start")
    session = resp.json()
    print(f"   Status: {session['status']}")
    
    time.sleep(1)
    
    # Pause
    print("3. Pausing (need a coffee)...")
    resp = requests.patch(f"{BASE}/sessions/{sid}/pause", json={"reason": "Coffee break"})
    session = resp.json()
    print(f"   Paused. Interruptions: {session['pause_count']}")
    
    time.sleep(1)
    
    # Resume
    print("4. Resuming...")
    resp = requests.patch(f"{BASE}/sessions/{sid}/resume")
    session = resp.json()
    print(f"   Status: {session['status']}")
    
    # Complete
    print("5. Completing session...")
    resp = requests.patch(f"{BASE}/sessions/{sid}/complete")
    session = resp.json()
    print(f"   Final status: {session['status']}")
    
    # History
    print("\n6. Fetching history...")
    resp = requests.get(f"{BASE}/sessions/history")
    for s in resp.json()[:5]:
        print(f"   - {s['title']}: {s['status']} ({s['pause_count']} pauses)")
    
    print("\n=== Demo complete! ===")


if __name__ == "__main__":
    main()
