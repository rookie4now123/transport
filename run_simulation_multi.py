# import requests
# import time
# import os
# import threading # Import the threading module

# # --- CONFIGURATION ---
# # Base URL for your Django server
# BASE_URL = "http://127.0.0.1:8000/api"
# TOKEN_ENDPOINT = "/monitor/auth/login/"

# # List of monitor credentials
# # IMPORTANT: Ensure these users exist in your Django database
# MONITOR_CREDENTIALS = [
#     {"username": "monitor001", "password": "123456"},
#     {"username": "monitor002", "password": "123456"},
#     {"username": "monitor003", "password": "123456"},
#     {"username": "monitor004", "password": "123456"},
#     {"username": "monitor005", "password": "123456"},
#     {"username": "monitor006", "password": "123456"},
#     {"username": "monitor007", "password": "123456"},
#     {"username": "monitor008", "password": "123456"},
#     {"username": "monitor009", "password": "123456"},
#     {"username": "monitor010", "password": "123456"},
# ]

# # List of Route IDs to test (you might want different ones or the same if it's a template)
# # IMPORTANT: Ensure these Route UUIDs are valid in your Django DB
# ROUTE_IDS_TO_TEST = [
#     "68ab6302-4274-4180-a3bc-545e1ae5b01d", # Example Route 1
#     "7673abb0-c965-4f50-b792-d42f3cee12d7", # Example Route 2 (change these to actual UUIDs)
#     "c449a180-e04d-4ccd-abc5-a89c784419fc", # Example Route 3
#     "8f17156d-6705-4fda-bbef-a7a7729d185d", # ...and so on for 10 routes.
#     "bbba73f4-c4a9-4286-977b-85fcbd52dec8",
#     "bc180695-e4f0-4f8b-905e-1ad5ae68d5eb",
#     "04f68462-0302-460f-8eaa-cd30fe027d97",
#     "67421cc7-4ada-4fcc-813c-a1500f162c8c",
#     "a486a1cc-fd27-41e5-ac90-bd2377e699e2",
#     "db1b7b9f-4dcc-48ec-94e2-e5d744b90a51",
# ]
# # If you want all monitors to use the same route template, you can just do:
# # ROUTE_IDS_TO_TEST = ["db1b7b9f-4dcc-48ec-94e2-e5d744b90a51"] * len(MONITOR_CREDENTIALS)


# # Base location for simulation, varied slightly for each run
# INITIAL_BASE_LAT = 33.052211
# INITIAL_BASE_LON = -112.243711
# LAT_OFFSET_PER_RUN = 0.000001 # Offset each simulation's start lat
# LON_OFFSET_PER_RUN = 0.000001 # Offset each simulation's start lon

# NUM_POINTS_PER_RUN = 10000 # Number of points to simulate per run
# POINT_UPLOAD_INTERVAL = 10 # Seconds to wait between point uploads

# # --- END CONFIGURATION ---

# def run_simulation(sim_id, username, password, route_id_to_test, base_lat, base_lon):
#     """
#     Executes the full workflow: login, start run, upload points, end run.
#     This function now accepts all necessary parameters.
#     """
#     # Use a session object to persist the Authorization header per thread
#     session = requests.Session()
#     run_id = None
    
#     # Prefix print statements with simulation ID for clarity
#     def sim_print(message):
#         print(f"[Sim {sim_id:02d} - {username}] {message}")

#     try:
#         # --- Step 1: Login and Get Authentication Token ---
#         sim_print("--- Step 1: Logging in... ---")
#         login_url = BASE_URL + TOKEN_ENDPOINT
#         login_payload = {"username": username, "password": password}
#         response = session.post(login_url, json=login_payload)
#         response.raise_for_status()

#         token = response.json().get("access")
#         if not token:
#             sim_print("ERROR: Could not get token from response.")
#             return

#         session.headers.update({"Authorization": f"Bearer {token}"})
#         sim_print(f"Login successful. Token acquired.\n")

#         # --- Step 2: Start the Route Run ---
#         sim_print("--- Step 2: Starting a new route run... ---")
#         start_run_url = f"{BASE_URL}/monitor/routeruns/"
#         start_run_payload = {"route": route_id_to_test}
#         response = session.post(start_run_url, json=start_run_payload)
#         response.raise_for_status()
        
#         run_data = response.json()
#         run_id = run_data.get("id")
#         sim_print(f"Route run started successfully. Run ID: {run_id}\n")

#         # --- Step 3: Upload Location Points ---
#         sim_print("--- Step 3: Uploading location points... ---")
#         location_url = f"{BASE_URL}/monitor/locationpoints/"
        
       
#         for i in range(NUM_POINTS_PER_RUN):
#             # Simulate movement by slightly changing coordinates
#             lat = base_lat + (i * 0.000005)
#             lon = base_lon + (i * 0.000005)
            
#             location_payload = {
#                 "run": run_id,
#                 "latitude": f"{lat:.6f}",
#                 "longitude": f"{lon:.6f}"
#             }
#             response = session.post(location_url, json=location_payload)
#             response.raise_for_status()
#             sim_print(f"  ({i+1}/{NUM_POINTS_PER_RUN}) Uploaded location: LAT={lat:.6f}, LON={lon:.6f}")
#             time.sleep(POINT_UPLOAD_INTERVAL)
        
#         sim_print("Location uploads complete.\n")

#         # --- Step 4: End the Route Run ---
#         sim_print("--- Step 4: Ending the route run... ---")
#         end_run_url = f"{start_run_url}{run_id}/"
#         end_run_payload = {"status": "COMPLETED"}
#         response = session.patch(end_run_url, json=end_run_payload)
#         response.raise_for_status()

#         final_status = response.json().get("status")
#         end_time = response.json().get("end_time")
#         sim_print(f"Route run ended successfully. Final Status: {final_status}")
#         sim_print(f"End Time: {end_time}\n")
#         sim_print("--- SIMULATION COMPLETE ---")

#     except requests.exceptions.RequestException as e:
#         sim_print(f"\nAN ERROR OCCURRED: {e}")
#         if e.response is not None:
#             sim_print(f"Response Body: {e.response.text}")
#     finally:
#         # Optional: If you want to cancel the run if the script fails midway
#         # Check if run_id exists and if it was not already completed/cancelled
#         if run_id and ('final_status' not in locals() or final_status not in ["COMPLETED", "CANCELLED"]):
#             sim_print("\n--- CLEANUP: Script interrupted or failed. Attempting to cancel run... ---")
#             try:
#                 # Need a new session for cleanup if the original session failed/closed
#                 cleanup_session = requests.Session()
#                 # Re-authenticate for cleanup if token might be expired or session broken
#                 try:
#                     login_url = BASE_URL + TOKEN_ENDPOINT
#                     login_payload = {"username": username, "password": password}
#                     response = cleanup_session.post(login_url, json=login_payload)
#                     response.raise_for_status()
#                     token = response.json().get("access")
#                     if token:
#                         cleanup_session.headers.update({"Authorization": f"Bearer {token}"})
#                 except Exception as auth_e:
#                     sim_print(f"Cleanup authentication failed: {auth_e}. Cannot cancel run.")
#                     return

#                 end_run_url = f"{BASE_URL}/monitor/routeruns/{run_id}/"
#                 cleanup_payload = {"status": "CANCELLED"}
#                 cleanup_response = cleanup_session.patch(end_run_url, json=cleanup_payload)
#                 cleanup_response.raise_for_status()
#                 sim_print(f"Run ID {run_id} has been marked as CANCELLED.")
#             except requests.exceptions.RequestException as cleanup_e:
#                 sim_print(f"Cleanup failed for run ID {run_id}: {cleanup_e}")


# if __name__ == "__main__":
#     threads = []
#     num_simulations = len(MONITOR_CREDENTIALS) # Run as many simulations as you have credentials for

#     print(f"Starting {num_simulations} parallel bus monitor simulations...")

#     for i in range(num_simulations):
#         user_info = MONITOR_CREDENTIALS[i]
        
#         # Use modulo to cycle through routes if you have fewer routes than monitors
#         # Or, ensure ROUTE_IDS_TO_TEST has at least num_simulations elements
#         route_id = ROUTE_IDS_TO_TEST[i % len(ROUTE_IDS_TO_TEST)] 

#         # Vary the starting location slightly for each simulation
#         current_lat = INITIAL_BASE_LAT + (i * LAT_OFFSET_PER_RUN)
#         current_lon = INITIAL_BASE_LON + (i * LON_OFFSET_PER_RUN)

#         thread = threading.Thread(
#             target=run_simulation,
#             args=(i + 1, user_info["username"], user_info["password"], route_id, current_lat, current_lon)
#         )
#         threads.append(thread)
#         thread.start()
#         # Optional: Add a small delay between starting threads to avoid overwhelming the server
#         # time.sleep(0.1) 

#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()

#     print("\nAll simulations finished.")

import requests
import time
import os
import threading

# --- CONFIGURATION ---
# Base URL for your Django server
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN_ENDPOINT = "/monitor/auth/login/"

# --- MODIFIED: Define all monitor configurations in one place ---
# Each dictionary now contains the username, password, and the specific
# starting latitude and longitude for that monitor.
# Fill this out with your custom locations.
MONITOR_CONFIGS = [
    {"username": "monitor001", "password": "123456", "start_lat": 33.052211, "start_lon": -112.243711},
    {"username": "monitor002", "password": "123456", "start_lat": 33.058100, "start_lon": -112.251300},
    {"username": "monitor003", "password": "123456", "start_lat": 33.049950, "start_lon": -112.239820},
    {"username": "monitor004", "password": "123456", "start_lat": 33.051500, "start_lon": -112.248700},
    {"username": "monitor005", "password": "123456", "start_lat": 33.053400, "start_lon": -112.241100},
    {"username": "monitor006", "password": "123456", "start_lat": 33.050100, "start_lon": -112.245500},
    {"username": "monitor007", "password": "123456", "start_lat": 33.056600, "start_lon": -112.249900},
    {"username": "monitor008", "password": "123456", "start_lat": 33.054200, "start_lon": -112.253200},
    # {"username": "monitor009", "password": "123456", "start_lat": 33.059300, "start_lon": -112.238500},
    # {"username": "monitor010", "password": "123456", "start_lat": 33.057800, "start_lon": -112.246800},
]

# List of Route IDs to test (you might want different ones or the same if it's a template)
# IMPORTANT: Ensure these Route UUIDs are valid in your Django DB
ROUTE_IDS_TO_TEST = [
    "68ab6302-4274-4180-a3bc-545e1ae5b01d", # Example Route 1
    "7673abb0-c965-4f50-b792-d42f3cee12d7", # Example Route 2 (change these to actual UUIDs)
    "c449a180-e04d-4ccd-abc5-a89c784419fc", # Example Route 3
    "8f17156d-6705-4fda-bbef-a7a7729d185d", # ...and so on for 10 routes.
    "bbba73f4-c4a9-4286-977b-85fcbd52dec8",
    "bc180695-e4f0-4f8b-905e-1ad5ae68d5eb",
    "04f68462-0302-460f-8eaa-cd30fe027d97",
    "67421cc7-4ada-4fcc-813c-a1500f162c8c",
    # "a486a1cc-fd27-41e5-ac90-bd2377e699e2",
    # "db1b7b9f-4dcc-48ec-94e2-e5d744b90a51",
]

# --- MODIFIED: The following variables are no longer needed ---
# INITIAL_BASE_LAT = 33.052211
# INITIAL_BASE_LON = -112.243711
# LAT_OFFSET_PER_RUN = 0.000001
# LON_OFFSET_PER_RUN = 0.000001

NUM_POINTS_PER_RUN = 10000 # Number of points to simulate per run
POINT_UPLOAD_INTERVAL = 5 # Seconds to wait between point uploads

# --- END CONFIGURATION ---

def run_simulation(sim_id, username, password, route_id_to_test, base_lat, base_lon):
    """
    Executes the full workflow: login, start run, upload points, end run.
    This function now accepts all necessary parameters.
    """
    # Use a session object to persist the Authorization header per thread
    session = requests.Session()
    run_id = None
    
    # Prefix print statements with simulation ID for clarity
    def sim_print(message):
        print(f"[Sim {sim_id:02d} - {username}] {message}")

    try:
        # --- Step 1: Login and Get Authentication Token ---
        sim_print("--- Step 1: Logging in... ---")
        login_url = BASE_URL + TOKEN_ENDPOINT
        login_payload = {"username": username, "password": password}
        response = session.post(login_url, json=login_payload)
        response.raise_for_status()

        token = response.json().get("access")
        if not token:
            sim_print("ERROR: Could not get token from response.")
            return

        session.headers.update({"Authorization": f"Bearer {token}"})
        sim_print(f"Login successful. Token acquired.\n")

        # --- Step 2: Start the Route Run ---
        sim_print("--- Step 2: Starting a new route run... ---")
        start_run_url = f"{BASE_URL}/monitor/routeruns/"
        start_run_payload = {"route": route_id_to_test}
        response = session.post(start_run_url, json=start_run_payload)
        response.raise_for_status()
        
        run_data = response.json()
        run_id = run_data.get("id")
        sim_print(f"Route run started successfully. Run ID: {run_id}\n")

        # --- Step 3: Upload Location Points ---
        sim_print("--- Step 3: Uploading location points... ---")
        location_url = f"{BASE_URL}/monitor/locationpoints/"
        
       
        for i in range(NUM_POINTS_PER_RUN):
            # Simulate movement by slightly changing coordinates
            lat = base_lat + (i * 0.00005)
            lon = base_lon + (i * 0.00005)
            
            location_payload = {
                "run": run_id,
                "latitude": f"{lat:.6f}",
                "longitude": f"{lon:.6f}"
            }
            response = session.post(location_url, json=location_payload)
            response.raise_for_status()
            sim_print(f"  ({i+1}/{NUM_POINTS_PER_RUN}) Uploaded location: LAT={lat:.6f}, LON={lon:.6f}")
            time.sleep(POINT_UPLOAD_INTERVAL)
        
        sim_print("Location uploads complete.\n")

        # --- Step 4: End the Route Run ---
        sim_print("--- Step 4: Ending the route run... ---")
        end_run_url = f"{start_run_url}{run_id}/"
        end_run_payload = {"status": "COMPLETED"}
        response = session.patch(end_run_url, json=end_run_payload)
        response.raise_for_status()

        final_status = response.json().get("status")
        end_time = response.json().get("end_time")
        sim_print(f"Route run ended successfully. Final Status: {final_status}")
        sim_print(f"End Time: {end_time}\n")
        sim_print("--- SIMULATION COMPLETE ---")

    except requests.exceptions.RequestException as e:
        sim_print(f"\nAN ERROR OCCURRED: {e}")
        if e.response is not None:
            sim_print(f"Response Body: {e.response.text}")
    finally:
        # Optional: If you want to cancel the run if the script fails midway
        # Check if run_id exists and if it was not already completed/cancelled
        if run_id and ('final_status' not in locals() or final_status not in ["COMPLETED", "CANCELLED"]):
            sim_print("\n--- CLEANUP: Script interrupted or failed. Attempting to cancel run... ---")
            try:
                # Need a new session for cleanup if the original session failed/closed
                cleanup_session = requests.Session()
                # Re-authenticate for cleanup if token might be expired or session broken
                try:
                    login_url = BASE_URL + TOKEN_ENDPOINT
                    login_payload = {"username": username, "password": password}
                    response = cleanup_session.post(login_url, json=login_payload)
                    response.raise_for_status()
                    token = response.json().get("access")
                    if token:
                        cleanup_session.headers.update({"Authorization": f"Bearer {token}"})
                except Exception as auth_e:
                    sim_print(f"Cleanup authentication failed: {auth_e}. Cannot cancel run.")
                    return

                end_run_url = f"{BASE_URL}/monitor/routeruns/{run_id}/"
                cleanup_payload = {"status": "CANCELLED"}
                cleanup_response = cleanup_session.patch(end_run_url, json=cleanup_payload)
                cleanup_response.raise_for_status()
                sim_print(f"Run ID {run_id} has been marked as CANCELLED.")
            except requests.exceptions.RequestException as cleanup_e:
                sim_print(f"Cleanup failed for run ID {run_id}: {cleanup_e}")


if __name__ == "__main__":
    threads = []
    num_simulations = len(MONITOR_CONFIGS) # Run as many simulations as you have configs for

    print(f"Starting {num_simulations} parallel bus monitor simulations...")

    for i in range(num_simulations):
        # --- MODIFIED: Get all info from the monitor's config dictionary ---
        monitor_config = MONITOR_CONFIGS[i]
        
        username = monitor_config["username"]
        password = monitor_config["password"]
        start_lat = monitor_config["start_lat"]
        start_lon = monitor_config["start_lon"]
        
        # Use modulo to cycle through routes if you have fewer routes than monitors
        route_id = ROUTE_IDS_TO_TEST[i % len(ROUTE_IDS_TO_TEST)] 

        # --- MODIFIED: Pass the specific starting location to the thread ---
        thread = threading.Thread(
            target=run_simulation,
            args=(i + 1, username, password, route_id, start_lat, start_lon)
        )
        threads.append(thread)
        thread.start()
        # Optional: Add a small delay between starting threads to avoid overwhelming the server
        # time.sleep(0.1) 

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\nAll simulations finished.")